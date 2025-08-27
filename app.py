from flask import Flask, request, render_template, Response
import os
import requests

app = Flask(__name__)

# ⬇️ PASTE YOUR REPLIT URL BETWEEN THE QUOTES (no trailing slash)
# Example: "https://whisperserver-yourname.repl.co"
https://e85ec01a-ea75-404c-a736-8372ffa3e0d7-00-20gzg5d16zu9e.worf.replit.dev = "https://YOUR-REPLIT-URL"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # get the uploaded file from the form
        f = request.files.get("audiofile")
        if not f:
            return "No file uploaded.", 400

        # forward the file to your Replit backend
        try:
            r = requests.post(
                f"{REPLIT_URL}/transcribe",
                files={"audio": (f.filename, f.stream, f.mimetype)}
            )
        except Exception as e:
            return f"Could not reach backend: {e}", 502

        if r.status_code != 200:
            return f"Backend error: {r.text}", 500

        text = r.json().get("text", "")
        return Response(
            text,
            headers={
                "Content-Type": "text/plain; charset=utf-8",
                "Content-Disposition": "attachment; filename=transcript.txt"
            }
        )

    # GET request -> show upload page
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

