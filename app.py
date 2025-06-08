from flask import Flask, request, render_template, send_file
import os
import subprocess
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "transcripts"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["audiofile"]
        if file:
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            output_txt = os.path.join(OUTPUT_FOLDER, filename + ".txt")

            # Whisper.cpp example call — replace or adjust if needed
            subprocess.run([
                "./whisper/main", "-m", "models/ggml-base.en.bin",
                "-f", filepath, "-of", output_txt.replace(".txt", "")
            ])

            return send_file(output_txt, as_attachment=True)

    return render_template("index.html")

# ✅ THIS IS THE IMPORTANT PART FOR RENDER 👇
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(ho
