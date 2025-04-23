from flask import Flask
from flask import render_template

app = Flask(__name__)

quiz_qs = [
    {
        "mains": 2,
        "complements": 1,
        "choices": [
            {"image": "/static/blue_shirt.jpg", "color": "blue"},
            {"image": "/static/black_leather_jacket.webp", "color": "black"},
            {"image": "/static/carhartt_jacket.webp", "color": "brown"},
            {"image": "/static/jorts.jpg", "color": "blue"},
            {"image": "/static/white_pants.webp", "color": "white"},
            {"image": "/static/yellow_shirt.jpg", "color": "yellow"},
        ],
    },
]


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/quiz")
def quiz():
   return render_template("quiz.html", question=quiz_qs[0])


if __name__ == "__main__":
    app.run(debug=True, port=5001)
