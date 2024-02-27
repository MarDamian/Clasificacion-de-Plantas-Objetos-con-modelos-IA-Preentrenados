// Escucha el evento click en el botón de envío
document.getElementById('submitBtn').addEventListener('click', async () => {
    // Obtiene el elemento de entrada de archivo y el archivo seleccionado
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];

    // Verifica si se ha seleccionado un archivo
    if (!file) {
        // Si no, muestra una alerta y regresa temprano
        alert('Por favor, selecciona una imagen antes de hacer clic en "Resultados".');
        return;
    }

    // Crea un objeto FormData y agrega el archivo
    const formData = new FormData();
    formData.append('file', file);

    try {
        // Envía una solicitud POST al servidor con el archivo
        const response = await fetch('http://127.0.0.1:8000/predict/image', {
            method: 'POST',
            body: formData,
        });

        // Si la respuesta es exitosa
        if (response.ok) {
            // Obtiene las predicciones de la respuesta
            const predictions = await response.json();
            // Actualiza el elemento de respuesta con las predicciones
            displayResults(predictions);
        } else {
            // Si la respuesta no es exitosa, registra un error
            console.error('Error al enviar la imagen.');
        }
    } catch (error) {
        // Si hay un error, registralo
        console.error('Error de red:', error);
    }
});

// Función para mostrar los resultados
function displayResults(results) {
    // Obtiene el elemento de respuesta
    const responseElement = document.getElementById('response');

    // Limpia el contenido anterior del elemento de respuesta
    responseElement.innerHTML = '';

    // Recorre los resultados y los muestra
    results.forEach(result => {
        const div = document.createElement('div');
        div.innerHTML = `<strong>${result.label}</strong>: ${result.probability}`;
        responseElement.appendChild(div);
    });
}

document.getElementById('imageInput').addEventListener('change', (event) => {
    // Obtiene el elemento de vista previa de la imagen
    const imagePreviewElement = document.getElementById('imagePreview');

    // Limpia el contenido anterior de la vista previa de la imagen
    imagePreviewElement.innerHTML = '';

    // Obtiene el archivo seleccionado
    const file = event.target.files[0];

    // Crea un objeto FileReader
    const reader = new FileReader();

    // Agrega un controlador para el evento load
    reader.onload = (event) => {
        // Crea una etiqueta de imagen
        const img = new Image();

        // Establece la fuente de la imagen
        img.src = event.target.result;

        // Agrega un controlador para el evento load de la imagen
        img.onload = () => {
            // Agrega la imagen a la vista previa
            imagePreviewElement.appendChild(img);
        };
    };

    // Lee el archivo como una URL de datos
    reader.readAsDataURL(file);
});