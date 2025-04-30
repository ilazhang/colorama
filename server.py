from flask import Flask
from flask import render_template
from flask import request
from flask import session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'fashion_quiz_secret_key'  # Required for session

# Clothing items database
clothing_items = [
    {"image": "/static/blue_shirt.jpg", "color": "blue"},
    {"image": "/static/black_leather_jacket.webp", "color": "black"},
    {"image": "/static/carhartt_jacket.webp", "color": "tan"},
    {"image": "/static/jorts.jpg", "color": "blue"},
    {"image": "/static/white_pants.webp", "color": "white"},
    {"image": "/static/yellow_shirt.jpg", "color": "yellow"},
    {"image": "/static/terracotta_hoodie.jpg", "color": "terracotta"},
    {"image": "/static/carhartt_pants.jpg", "color": "brown"},
]

# Quiz database with multiple questions
quiz_qs = [
    {
        "id": 1,
        "mains": 2,
        "complements": 1,
        "expected_mains": {"brown", "tan"},
        "expected_complements": {"terracotta"},
        "description": "Earth tones palette"
    },
    {
        "id": 2,
        "mains": 2,
        "complements": 1,
        "expected_mains": {"blue", "white"},
        "expected_complements": {"yellow"},
        "description": "Cool blues palette"
    },
    {
        "id": 3,
        "mains": 2,
        "complements": 1,
        "expected_mains": {"black", "white"},
        "expected_complements": {"blue"},
        "description": "Monochrome with accent"
    }
]

# Helper function to get question by ID
def get_question_by_id(question_id):
    for question in quiz_qs:
        if question["id"] == question_id:
            return question
    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/learn")
def learn():
    return render_template("learn.html")


@app.route("/quiz")
def quiz():
    # Initialize or reset the quiz
    question_id = request.args.get('question_id', type=int)
    
    if not question_id:
        # Start with the first question
        session['current_question'] = 1
        session['correct_answers'] = 0
        session['total_questions'] = len(quiz_qs)
        question = quiz_qs[0]
    else:
        # Get the specified question
        question = get_question_by_id(question_id)
        if not question:
            # If question doesn't exist, start over
            return redirect(url_for('quiz'))
        session['current_question'] = question_id
    
    # Add clothing items to the question
    question_with_items = question.copy()
    question_with_items['choices'] = clothing_items
    
    return render_template(
        "quiz.html", 
        question=question_with_items,
        current=session.get('current_question', 1),
        total=session.get('total_questions', len(quiz_qs))
    )


@app.route("/quizanswer")
def parse():
    question_id = session.get('current_question', 1)
    question = get_question_by_id(question_id)
    
    if not question:
        return redirect(url_for('quiz'))
    
    mains = set(request.args.get("mains", "").split(","))
    if '' in mains:
        mains.remove('')
    
    complements = set(request.args.get("complements", "").split(","))
    if '' in complements:
        complements.remove('')
    
    expected_mains = question["expected_mains"]
    expected_complements = question["expected_complements"]

    mains_correct = mains == expected_mains
    complements_correct = complements == expected_complements
    correct = mains_correct and complements_correct
    
    # Update score if correct
    if correct:
        session['correct_answers'] = session.get('correct_answers', 0) + 1
    
    # Determine if this is the last question
    is_last = question_id >= len(quiz_qs)
    next_question_id = question_id + 1 if not is_last else None
    
    # Calculate final score if last question
    final_score = None
    if is_last:
        final_score = {
            'correct': session.get('correct_answers', 0),
            'total': session.get('total_questions', len(quiz_qs))
        }

    return render_template(
        "quizanswer.html", 
        correct=correct,
        mains_correct=mains_correct,
        complements_correct=complements_correct,
        user_mains=mains,
        user_complements=complements,
        expected_mains=expected_mains,
        expected_complements=expected_complements,
        next_question_id=next_question_id,
        is_last=is_last,
        final_score=final_score,
        description=question.get('description', '')
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
