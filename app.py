
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_from_directory
)

import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Upload folder
app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# HOME PAGE
@app.route("/")
def home():

    files = os.listdir(app.config["UPLOAD_FOLDER"])

    movies = [
        f for f in files
        if f.lower().endswith(
            (".mp4", ".mkv", ".avi", ".mov")
        )
    ]

    pdfs = [
        f for f in files
        if f.lower().endswith(".pdf")
    ]

    return render_template(
        "index.html",
        movies=movies,
        pdfs=pdfs
    )


# TELUGU MOVIES PAGE
@app.route("/telugu_movies")
def telugu_movies():

    movies = [
        "Ramayana",
        "Devara",
        "Telakagitham",
        "Jailer 2",
        "Aadarsha Kutumbam",
        "Sigma",
        "Comrade Kalyan",
        "Paradise",
        "Anakapalli",
        "Peddi",
        "Manasankaravaraprasad Garu",
        "Edumudi",
        "The Raja Saab",
        "Maa Inti Bangaram",
        "Anaganaga Oka Roju",
        "Ustaad Bhagat Singh",
        "Ranabali",
        "Lenin",
        "A Love Story",
        "Couple Friendly",
        "Deewaan",
        "Bhogi",
        "Jananayukudu",
        "Summer Holidays",
        "Donga Naa Koduku",
        "Dragon",
        "LIK",
        "Rakasa",
        "Shambala Part 1",
        "Shambala Part 2"
    ]

    return render_template(
        "telugu_movies.html",
        movies=movies
    )


# INTERNET MOVIES PAGE
@app.route("/internet_movies")
def internet_movies():

    try:
        url = "https://archive.org/advancedsearch.php"

        params = {
            "q": "mediatype:movies",
            "fl[]": ["identifier", "title", "year"],
            "rows": 10,
            "output": "json"
        }

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        movies = data.get(
            "response", {}
        ).get("docs", [])

        return render_template(
            "internet_movies.html",
            movies=movies
        )

    except requests.RequestException:
        return "Internet movie search is temporarily unavailable."


# UPLOAD MULTIPLE MOVIES
@app.route("/upload", methods=["POST"])
def upload():

    files = request.files.getlist("movie")

    for file in files:

        if file and file.filename:

            filename = secure_filename(file.filename)

            if filename:
                file.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )

    return redirect("/")


# UPLOAD PDF
@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():

    file = request.files.get("pdf")

    if file and file.filename.lower().endswith(".pdf"):

        filename = secure_filename(file.filename)

        if filename:
            file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

    return redirect("/")


# PLAY / OPEN UPLOADED FILE
@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# DOWNLOAD UPLOADED FILE
@app.route("/download/<filename>")
def download_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )


# RUN SERVER
if __name__ == "__main__":

    app.run(debug=True)
