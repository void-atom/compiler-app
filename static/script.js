document.getElementById("uploadForm").onsubmit = async function (event) {
    event.preventDefault();
    
    const outputDiv = document.getElementById("output");
    const codeEditor = document.getElementById("codeEditor").value.trim();
    // let filename = document.getElementById("filename").value.trim() || "code.c";
    let filename = 'kelp.c'

    if (!codeEditor) {
        alert("Please enter some C code.");
        return;
    }

    outputDiv.innerHTML = '<span class="loading">Processing file, please wait...</span>';

    let formData = new FormData();
    const fileBlob = new Blob([codeEditor], { type: "text/plain" });
    formData.append("file", fileBlob, filename);

    try {
        console.log("Uploading code as file:", filename);

        let response = await fetch("http://127.0.0.1:5000/upload", { 
            method: "POST", 
            body: formData,
            headers: { 'Accept': 'application/json' }
        });

        console.log("Response status:", response.status);

        if (!response.ok) {
            outputDiv.innerHTML = `<span class="error">Server error: ${response.status} ${response.statusText}</span>`;
            console.error("Server returned error:", response.status, response.statusText);

            try {
                const errorText = await response.text();
                console.error("Error details:", errorText);
            } catch (e) {
                console.error("Couldn't read error details");
            }
            return;
        }

        let result;
        try {
            result = await response.json();
            console.log("Response received:", result);
        } catch (jsonError) {
            console.error("JSON parsing error:", jsonError);
            const rawText = await response.text();
            console.log("Raw response:", rawText);
            outputDiv.innerHTML = `<span class="error">Server returned invalid JSON. Raw response: ${rawText || 'empty response'}</span>`;
            return;
        }

        if (result.error && result.error.trim() !== "") {
            outputDiv.innerHTML = `<span class="error">Error: ${result.error}</span>`;
        } else if (result.output) {
            outputDiv.innerText = result.output;
        } else {
            outputDiv.innerText = "No output received from tokenizer";
        }
    } catch (error) {
        console.error("Fetch error:", error);
        outputDiv.innerHTML = `<span class="error">Network error: ${error.message}</span>`;
    }
};


