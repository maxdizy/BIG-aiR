const dragArea = document.querySelector('.drag_area');
const dragText = document.querySelector('.header');

let file;

// when file is inside the drag area
dragArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    dragText.textContent = "Release to Upload";
    dragArea.classList.add('active');
});

// when file leaves the drag area
dragArea.addEventListener('dragleave', () => {
    dragText.textContent = "Drag and Drop";
    dragArea.classList.remove('active');
});

// when the file is dropped in the drag area
dragArea.addEventListener('drop', (event) => {
    event.preventDefault();
    dragArea.classList.remove('active');

    file = event.dataTransfer.files[0];
    let fileType = file.type;

    let validExtensions = ['text/csv'];

    if(validExtensions.includes(fileType)){
        sendFileToServer(file);
    } else {
        alert('Invalid file type. Please upload a CSV file.');
    }
});

function sendFileToServer(file) {
    // Replace with backend server endpoint
    let serverUrl = 'BACKEND_SERVER_ENDPOINT_HERE';

    let formData = new FormData();
    formData.append('file', file);

    fetch(serverUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
