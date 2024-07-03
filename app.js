 document.getElementById('reportButton').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const email = document.getElementById('email').value;
    const fileInput = document.getElementById('dogPhoto');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();

        showLoadingMessage();
        
        // Read file as data URL
        reader.readAsDataURL(file);

         setTimeout(() => {
            sendMessage(email, file);
        }, 5000);
    }  else {
        alert('Please upload a photo of the dog.');
    }
});

function locateMe() {
    if (!navigator.geolocation) {
        alert('Geolocation is not supported by your browser');
    } else {
        navigator.geolocation.getCurrentPosition(function(position) {
            alert('Location: ' + position.coords.latitude + ', ' + position.coords.longitude);
            // Optionally, store these values in localStorage or use them in your form
        }, function() {
            alert('Unable to retrieve your location');
        });
    }
}


function sendMessage(email,file) {

    const formData = new FormData();
    formData.append('email', email); // Add other form data if needed
    formData.append('image', file);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to send message');
        }
        console.log('Message sent successfully');
        showNotification(); // Show the "Congratulations" block
    })
    .catch(error => {
        console.error('Error sending message:', error.message);
    });
     
}


function showNotification() {
    //hideLoadingMessage();
    const notification = document.getElementById('notification');
    notification.style.display = 'block';
}


function showLoadingMessage() {
    const loadingMessage = document.getElementById('loadingMessage');
    loadingMessage.style.display = 'block';
}

function hideLoadingMessage() {
    const loadingMessage = document.getElementById('loadingMessage');
    loadingMessage.style.display = 'none';
}