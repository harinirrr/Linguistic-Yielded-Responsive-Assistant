# app.py
import os
from flask import Flask, render_template, request, jsonify
from lyra_core import process_audio, supported_langs

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html", supported_langs=supported_langs)

@app.route("/process_audio", methods=["POST"])
def process_audio_route():
    # language choice from form
    lang = request.form.get("lang", "en")
    audio = request.files.get("audio")
    if not audio:
        return jsonify({"ok": False, "error": "No audio file uploaded."}), 400

    # save file
    filename = os.path.join(app.config["UPLOAD_FOLDER"], f"rec_{int(os.times()[4]*1000)}.wav")
    audio.save(filename)

    try:
        response_text = process_audio(filename, lang)
        return jsonify({"ok": True, "response": response_text})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    finally:
        # optional: keep or remove file; uncomment to delete
        try:
            os.remove(filename)
        except Exception:
            pass

if __name__ == "__main__":
    app.run(debug=True, port=5000)
