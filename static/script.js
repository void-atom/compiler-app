
document.getElementById('runCompiler').addEventListener('click', function() {
    const codeInput = document.getElementById('code-input').value;
    if (codeInput.trim() === '') {
      alert("Please enter some code to compile.");
      return;
    }

    // Create a FormData object and append the code as a file
    const formData = new FormData();
    const blob = new Blob([codeInput], { type: 'text/plain' });
    formData.append('file', blob, 'code.c'); // You can change 'code.c' to any file extension

    // Send the form data to the backend
    fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server Response: ", data); // Log the server response for debugging
        if (data.output) {  // Look for 'output' instead of 'assembly'
          // If the response contains Assembly code, update the Assembly section
          document.getElementById('Assembly').innerHTML = data.output;
          console.log(data.output);
        } else {
          // If there is no assembly code in the response
          document.getElementById('Assembly').innerHTML = 'Error generating assembly code.';
        }
      })
      .catch(error => {
        console.error('Error uploading file:', error);
        document.getElementById('Assembly').innerHTML = 'Failed to compile the code.';
      });
    });