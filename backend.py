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

    # Now call the appropriate function depending on which operation is requested
    return jsonify({"message": "File uploaded successfully", "file_path": filepath})

@app.route('/compiler', methods=['POST'])
def compiler():
    filepath = handle_file_upload(request)
    if not filepath:
        return jsonify({"error": "File not found"}), 400

    # Binary for the codegen.exe
    binaryPath = os.path.abspath(os.path.join('binaries', 'codegen.exe'))
    output_file = "codegen_output.s"

    if not os.path.exists(binaryPath):
        return jsonify({"error": "CodeGenerator executable not found"}), 500
    
    try:
        # Run codegen.exe with the input file
        result = subprocess.run(["binaries/codegen.exe", filepath,"-no-print"], capture_output=True, text=True, timeout=30)

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
        return jsonify({"assembly": codegen_output})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Process timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tokenizer',methods=['POST'])
def tokenizer():
    filepath = handle_file_upload(request)
    if not filepath:
        return jsonify({"error": "File not found"}), 400

    # Binary for the codegen.exe
    binaryPath = os.path.abspath(os.path.join('binaries', 'tokenizer.exe'))
    output_file = "token_output.html"

    if not os.path.exists(binaryPath):
        return jsonify({"error": "Tokenizer executable not found"}), 500
    
    try:
        # Run codegen.exe with the input file
        result = subprocess.run(["binaries/tokenizer.exe", filepath], capture_output=True, text=True, timeout=30)

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
        return jsonify({"tokens": codegen_output})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Process timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route('/parser',methods=['POST'])
def parser():
    filepath = handle_file_upload(request)
    if not filepath:
        return jsonify({"error": "File not found"}), 400

    # Binary for the codegen.exe
    binaryPath = os.path.abspath(os.path.join('binaries', 'parser.exe'))
    output_file = "ast.dot"

    if not os.path.exists(binaryPath):
        return jsonify({"error": "Parser executable not found"}), 500
    
    try:
        # Run codegen.exe with the input file
        result = subprocess.run(["binaries/parser.exe", filepath], capture_output=True, text=True, timeout=30)

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
        return jsonify({"parseTree": codegen_output})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Process timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

def handle_file_upload(request):
    """Helper function to handle file upload for all requests"""
    if 'file' not in request.files:
        return None
    
    file = request.files['file']
    if file.filename == '':
        return None
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    print(filepath)
    return filepath


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
