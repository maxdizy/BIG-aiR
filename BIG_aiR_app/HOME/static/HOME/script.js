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
    // Replace URL with Django backend endpoint
    let serverUrl = 'https://yourdomain.com/api/upload/';

    // Create a new FormData object
    let formData = new FormData();

    // Append the file to the FormData object
    // Replace 'fileFieldName' with the field name expected by Django backend
    formData.append('fileFieldName', file);

    fetch(serverUrl, {
        method: 'POST', // Use POST method for file upload
        body: formData,  // Attach the FormData object
        // headers: {},  // If needed, add headers here
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Handle success 
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle errors 
    });
}