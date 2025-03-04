from flask import Flask, request, jsonify
import subprocess
import os
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

# A dir to store all the c source files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    binaryPath = os.path.abspath(os.path.join('binaries', 'codegen.exe'))
    output_file = "codegen_output.s"

    if not os.path.exists(binaryPath):
        return jsonify({"error": "Tokenizer executable not found"}), 500
    
    try:
        # Run codegen.exe with the input file
        result = subprocess.run(["binaries/codegen.exe", filepath], capture_output=True, text=True, timeout=30)

        # Check if the process ran successfully
        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500
        
        # Check if output file exists after execution
        if not os.path.exists(output_file):
            return jsonify({"error": "Output file not found"}), 500

        # Read the content of the output file
        with open(output_file, "r") as file:
            codegen_output = file.read()
        
        os.remove(output_file)
        return jsonify({"output": codegen_output})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Process timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
