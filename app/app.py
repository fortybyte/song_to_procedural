from flask import Flask, request, send_file, render_template, after_this_request
from convert import convert_to_js
import os
import uuid

app = Flask(__name__)
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route("/api/convert", methods=["POST"])
def api_convert():
    audio = request.files.get("audio")
    if not audio:
        return {"error": "No file uploaded"}, 400

    uid = uuid.uuid4().hex
    input_path = os.path.join(TEMP_DIR, f"temp_{uid}")
    output_path = os.path.join(TEMP_DIR, f"temp_{uid}.js")

    audio.save(input_path)

    try:
        convert_to_js(input_path, output_path)
    except Exception as e:
        return {"error": f"Conversion failed: {e}"}, 500

    @after_this_request
    def remove_file(response):
        for path in (input_path, output_path):
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                print(f"Failed to delete {path}: {e}")
        return response

    return send_file(output_path, as_attachment=True, download_name="output.js")



@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
