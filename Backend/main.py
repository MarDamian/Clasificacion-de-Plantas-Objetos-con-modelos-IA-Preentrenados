from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
import tensorflow as tf
from keras.applications.imagenet_utils import decode_predictions
from keras.models import load_model
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Clasificación de Imágenes')

# Carga el modelo preentrenado (MobileNetV2 en este caso)
def load_model():
    model = tf.keras.applications.MobileNetV2(weights="imagenet")
    print("Modelo cargado")
    return model

model = load_model()

# Función para predecir la clase de una imagen
def predict(image: Image.Image) -> list:
    """
    Realiza una predicción de la clase de una imagen utilizando un modelo preentrenado.

    Parámetros:
        image (PIL.Image): La imagen de entrada.

    Retorna:
        list: Una lista de diccionarios, donde cada diccionario contiene la clase predicha
              y su nivel de confianza.
    """
    # Redimensionar la imagen a 224x224 píxeles y convertirla en un array numpy
    image = np.asarray(image.resize((224, 224)))[..., :3]

    # Expandir las dimensiones del array para que coincida con la forma esperada por el modelo
    image = np.expand_dims(image, 0)

    # Normalizar los valores de píxeles para que estén en el rango [-1, 1]
    image = image / 127.5 - 1.0

    # Realizar la predicción utilizando el modelo
    result = decode_predictions(model.predict(image), 2)[0]

    # Procesar los resultados de la predicción y construir la respuesta
    response = []
    for i, res in enumerate(result):
        resp = {"class": res[1], "confidence": f"{res[2]*100:.2f}%"}
        response.append(resp)

    return response
# Carga la imagen enviada por el frontend
def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

@app.post("/predict/image")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1].lower()
    if extension not in ("jpg", "jpeg", "png"):
        return "¡La imagen debe estar en formato jpg o png!"
    image = read_imagefile(await file.read())
    prediction = predict(image)
    print(prediction)
    return prediction

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",  # Agrega aquí el origen de tu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
