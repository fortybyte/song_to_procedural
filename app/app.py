from flask import Flask, request, send_file, render_template, after_this_request
from convert import convert_to_js
import os
import uuid

app = Flask(__name__)


@app.route("/api/convert", methods=["POST"])
def api_convert():
    audio = request.files.get("audio")
    if not audio:
        return {"error": "No file uploaded"}, 400
    uid = uuid.uuid4().hex
    input_path = f"temp_{uid}"
    output_path = f"temp_{uid}.js"
    audio.save(input_path)
    convert_to_js(input_path, output_path)
    os.remove(input_path)

    @after_this_request
    def remove_file(response):
        if os.path.exists(output_path):
            os.remove(output_path)
        return response

    return send_file(output_path, as_attachment=True, download_name="output.js")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
