 # Clasificación de Plantas con FastAPI y TensorFlow

Este proyecto consiste en una API para la clasificación de imágenes de plantas utilizando un modelo preentrenado (MobileNetV2) en TensorFlow. La API permite a los usuarios cargar una imagen y obtener la clase de la planta junto con el nivel de confianza asociado.

## Instalación

Para ejecutar este proyecto localmente, sigue estos pasos:

1. Clona este repositorio en tu máquina local.

2. Instala las dependencias utilizando pip:
```
   pip install -r requirements.txt
```

3. Ejecuta la aplicación utilizando Uvicorn(Backend):

```
cd .\Backend\
uvicorn main:app --reload
```
4. Live Server para el Frontend:


Aclaracion:Se uso el modelo base, sin ningun entrenamiento adicional para la clasificacion de plantar, esto queta pendiente como trabajo futuro.

   Referencias:
https://keras.io/api/applications/#usage-examples-for-image-classification-models
https://es.mathworks.com/help/deeplearning/ref/mobilenetv2.htm
