from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

quiz_qs = [
    {
        "mains": 2,
        "complements": 1,
        "choices": [
            {"image": "/static/blue_shirt.jpg", "color": "blue"},
            {"image": "/static/black_leather_jacket.webp", "color": "black"},
            {"image": "/static/carhartt_jacket.webp", "color": "tan"},
            {"image": "/static/jorts.jpg", "color": "blue"},
            {"image": "/static/white_pants.webp", "color": "white"},
            {"image": "/static/yellow_shirt.jpg", "color": "yellow"},
            {"image": "/static/terracotta_hoodie.jpg", "color": "terracotta"},
            {"image": "/static/carhartt_pants.jpg", "color": "brown"},
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


@app.route("/quizanswer")
def parse():
    mains = set(request.args.get("mains", "").split(","))
    complements = set(request.args.get("complements", "").split(","))

    correct = mains == {"brown", "tan"} and complements == {"terracotta"}

    return render_template("quizanswer.html", correct=correct)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
