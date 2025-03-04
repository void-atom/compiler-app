
function handleCompilerClick() 
{
    const codeInput = document.getElementById('code-input').value.trim();
    if (codeInput === '') 
    {
        alert("Please enter some code to compile.");
        return;
    }

    // Create a FormData object and append the code as a file
    const formData = new FormData();
    const blob = new Blob([codeInput], { type: 'text/plain' });
    formData.append('file', blob, 'komp.c'); 

    // Send the form data to the backend
    fetch('http://127.0.0.1:5000/compiler', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log("Server Response: ", data); 
            if (data.assembly) {
                document.getElementById('Assembly').innerHTML = data.assembly;
                console.log(data.assembly);
            } else {
                document.getElementById('Assembly').innerHTML = 'Error generating assembly code.';
            }
        })
        .catch(error => {
            console.error('Error uploading file:', error);
            document.getElementById('Assembly').innerHTML = 'Failed to compile the code.';
        });

}
function handleTokenizerClick()
{
    const codeInput = document.getElementById('code-input').value.trim();
    if (codeInput === '') 
    {
        alert("Please enter some code to compile.");
        return;
    }

    const formData = new FormData();
    const blob = new Blob([codeInput], { type: 'text/plain' });
    formData.append('file', blob, 'code.c'); // You can change 'code.c' to any file extension

    // Send the form data to the backend
    fetch('http://127.0.0.1:5000/tokenizer', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log("Server Response: ", data); 
            if (data.tokens) {
                document.getElementById('tokenizer-output').innerHTML = data.tokens;
                console.log(data.tokens);
            } else {
                document.getElementById('tokenizer-output').innerHTML = 'Error generating tokens.';
            }
        })
        .catch(error => {
            console.error('Error uploading file:', error);
            document.getElementById('tokenizer-output').innerHTML = 'Failed to generate tokens.';
        });
}

document.getElementById('runCompiler').addEventListener('click', handleCompilerClick );
document.getElementById('runTokenizer').addEventListener('click', handleTokenizerClick );

