from flask import Flask
from flask import render_template
from flask import request
from flask import session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'fashion_quiz_secret_key'  # Required for session

# Clothing items database
clothing_items = {
    1: {"id": 1, "image": "/static/blue_shirt.jpg", "color": "blue", "name": "Blue Shirt"},
    2: {"id": 2, "image": "/static/black_leather_jacket.webp", "color": "black", "name": "Black Leather Jacket"},
    3: {"id": 3, "image": "/static/carhartt_jacket.webp", "color": "tan", "name": "Tan Jacket"},
    4: {"id": 4, "image": "/static/jorts.jpg", "color": "blue", "name": "Blue Jorts"},
    5: {"id": 5, "image": "/static/white_pants.webp", "color": "white", "name": "White Pants"},
    6: {"id": 6, "image": "/static/yellow_shirt.jpg", "color": "yellow", "name": "Yellow Shirt"},
    7: {"id": 7, "image": "/static/terracotta_hoodie.jpg", "color": "terracotta", "name": "Terracotta Hoodie"},
    8: {"id": 8, "image": "/static/carhartt_pants.jpg", "color": "brown", "name": "Brown Pants"},
}

# Quiz database with multiple questions
quiz_qs = [
    {
        "id": 1,
        "mains": 2,
        "complements": 1,
        "expected_mains": {8, 3},  # Brown Pants, Tan Jacket
        "expected_complements": {7},  # Terracotta Hoodie
        "description": "Earth tones palette"
    },
    {
        "id": 2,
        "mains": 2,
        "complements": 1,
        "expected_mains": {1, 5},  # Blue Shirt, White Pants
        "expected_complements": {6},  # Yellow Shirt
        "description": "Cool blues palette"
    },
    {
        "id": 3,
        "mains": 2,
        "complements": 1,
        "expected_mains": {2, 5},  # Black Leather Jacket, White Pants
        "expected_complements": {1},  # Blue Shirt
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
@app.route("/quiz/<int:question_id>")
def quiz(question_id=None):
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
    question_with_items['choices'] = list(clothing_items.values())
    
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
    
    mains = set()
    for item_id in request.args.get("mains", "").split(","):
        if item_id and item_id.isdigit():
            mains.add(int(item_id))
    
    complements = set()
    for item_id in request.args.get("complements", "").split(","):
        if item_id and item_id.isdigit():
            complements.add(int(item_id))
    
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
        description=question.get('description', ''),
        clothing_items=clothing_items
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
