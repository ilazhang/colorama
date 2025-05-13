from flask import Flask
from flask import render_template
from flask import request
from flask import session, redirect, url_for

app = Flask(__name__)
app.secret_key = "fashion_quiz_secret_key"  # Required for session

# Clothing items database
clothing_items = {
    1: {
        "id": 1,
        "image": "/static/blue_shirt.jpg",
        "color": "blue",
        "name": "Blue Shirt",
    },
    2: {
        "id": 2,
        "image": "/static/black_leather_jacket.webp",
        "color": "black",
        "name": "Black Leather Jacket",
    },
    3: {
        "id": 3,
        "image": "/static/carhartt_jacket.webp",
        "color": "tan",
        "name": "Tan Jacket",
    },
    4: {"id": 4, "image": "/static/jorts.jpg", "color": "denim", "name": "Blue Jorts"},
    5: {
        "id": 5,
        "image": "/static/white_pants.webp",
        "color": "white",
        "name": "White Pants",
    },
    6: {
        "id": 6,
        "image": "/static/yellow_shirt.jpg",
        "color": "yellow",
        "name": "Yellow Shirt",
    },
    7: {
        "id": 7,
        "image": "/static/terracotta_hoodie.jpg",
        "color": "terracotta",
        "name": "Terracotta Hoodie",
    },
    8: {
        "id": 8,
        "image": "/static/carhartt_pants.jpg",
        "color": "brown",
        "name": "Brown Pants",
    },
    9: {
        "id": 9,
        "image": "/static/cream_shirt.webp",
        "color": "cream",
        "name": "Cream Shirt",
    },
    10: {
        "id": 10,
        "image": "/static/grey_sweats.jpg",
        "color": "grey",
        "name": "Grey Sweatpants",
    },
    11: {
        "id": 11,
        "image": "/static/light_green_sweats.jpg",
        "color": "light-green",
        "name": "Light Green Sweatpants",
    },
    12: {
        "id": 12,
        "image": "/static/light_pink_pants.jpg",
        "color": "light-pink",
        "name": "Light Pink Pants",
    },
    13: {
        "id": 13,
        "image": "/static/maroon_scarf.jpg",
        "color": "maroon",
        "name": "Maroon Scarf",
    },
    14: {
        "id": 14,
        "image": "/static/shorts.jpg",
        "color": "black",
        "name": "Black Shorts",
    },
}

# Quiz database with multiple questions
quiz_qs = [
    {
        "id": 1,
        "mains": 2,
        "complements": 1,
        "expected_mains": {8, 3},  # Brown Pants, Tan Jacket
        "expected_complements": {7},  # Terracotta Hoodie
        "description": "Earth tones",
        "available_items": [
            3,
            7,
            8,
            9,
            10,
            13,
        ],  # Limited selection of items for this question
    },
    {
        "id": 2,
        "mains": 2,
        "complements": 1,
        "expected_mains": {1, 5},  # Blue Shirt, White Pants
        "expected_complements": {6},  # Yellow Shirt
        "description": "Cool blues with a pop of color",
        "available_items": [
            1,
            4,
            5,
            6,
            11,
            14,
        ],  # Limited selection of items for this question
    },
    {
        "id": 3,
        "mains": 2,
        "complements": 1,
        "expected_mains": {2, 5},  # Black Leather Jacket, White Pants
        "expected_complements": {1},  # Blue Shirt
        "description": "Monochrome with accent",
        "available_items": [
            1,
            2,
            5,
            10,
            14,
        ],  # Limited selection of items for this question
    },
    {
        "id": 4,
        "mains": 2,
        "complements": 1,
        "expected_mains": {9, 10},  # Cream Shirt, Grey Sweatpants
        "expected_complements": {13},  # Maroon Scarf
        "description": "Neutral base with pop of color",
        "available_items": [
            2,
            9,
            10,
            12,
            13,
        ],  # Limited selection of items for this question
    },
    {
        "id": 5,
        "mains": 2,
        "complements": 1,
        "expected_mains": {11, 14},  # Light Green Sweatpants, Black Shorts
        "expected_complements": {12},  # Light Pink Pants
        "description": "Sporty casual with pastel accent",
        "available_items": [
            6,
            11,
            12,
            14,
            4,
            10,
        ],  # Limited selection of items for this question
    },
]

# Route from palette lesson to main color lesson


@app.route("/color-detail")
def color_detail():
    palette = request.args.get("palette", "")
    color = request.args.get("color", "")
    color_name = request.args.get("name", "")

    back_url = url_for("learn") + "?lesson=1"

    if palette == "earth":
        back_url = url_for("learn") + "?lesson=1"
        palette_title = "Earth Tones"
    elif palette == "pastel":
        back_url = url_for("learn") + "?lesson=2"
        palette_title = "Pastel Colors"
    elif palette == "monochrome":
        back_url = url_for("learn") + "?lesson=3"
        palette_title = "Monochrome Colors"
    elif palette == "jewel":
        back_url = url_for("learn") + "?lesson=4"
        palette_title = "Jewel Tones"
    else:
        palette_title = "Color Detail"

    # descriptions - optional?
    color_descriptions = {
        "olive": "A muted green with hints of brown, perfect for creating a natural look.",
        "tan": "A light brown shade that evokes sand and natural fibers, versatile for earth toned palettes and more.",
        "brown": "A rich, deep brown reminiscent of wood and leather, creates a strong foundation for outfits.",
        "dark-green": "A deep forest green that adds richness and depth to earth tone palettes.",
        "rose": "A soft, muted pink that adds warmth and subtle contrast to earth tones.",
        "terracotta": "A warm, reddish-brown inspired by clay pottery, creates a rustic accent.",
        "pink": "A soft, delicate pink that adds a gentle touch of color to any outfit.",
        "baby-blue": "A light, airy blue that evokes calm and serenity, perfect for spring and summer.",
        "light-yellow": "A soft, buttery yellow that brings warmth and cheerfulness to your wardrobe.",
        "lavender": "A gentle purple that adds a relaxed, romantic quality to pastel palettes.",
        "white": "A clean neutral that brightens and freshens pastel color combinations.",
        "light-green": "A soft mint green that adds a refreshing, natural element to pastel looks.",
        "pure-white": "The brightest white, forming the foundation of monochrome palettes with clean lines.",
        "light-gray": "A subtle gray that adds dimension without overwhelming a monochrome look.",
        "medium-gray": "A balanced neutral that bridges between darker and lighter monochrome elements.",
        "dark-gray": "A deep gray that adds drama and contrast to monochrome palettes.",
        "pure-black": "The absence of color, creating sharp contrast and bold definition.",
        "charcoal": "A rich, deep gray with subtle warmth, softer than pure black but equally sophisticated.",
        "ruby": "A deep, rich red inspired by the precious gemstone, adds luxury and warmth.",
        "emerald": "A vibrant green with depth and richness, creating a bold statement in any outfit.",
        "sapphire": "A deep, royal blue that conveys elegance and timeless sophistication.",
        "plum": "A rich purple with depth and complexity, balancing between red and blue undertones.",
        "dark-gold": "A deep, burnished gold that adds rich warmth and luxury without being flashy.",
        "deep-teal": "A rich blue-green that combines the depth of blue with the vibrancy of green.",
    }

    color_description = color_descriptions.get(
        color, "A versatile color that works well in many combinations."
    )

    next_colors = {
        "earth": {
            "olive": {"color": "tan", "name": "Tan"},
            "tan": {"color": "brown", "name": "Brown"},
            "brown": {"color": "olive", "name": "Olive"},
            "dark-green": {"color": "rose", "name": "Rose"},
            "rose": {"color": "terracotta", "name": "Terracotta"},
            "terracotta": {"color": "dark-green", "name": "Dark Green"},
        },
        "pastel": {
            "pink": {"color": "baby-blue", "name": "Baby Blue"},
            "baby-blue": {"color": "light-yellow", "name": "Light Yellow"},
            "light-yellow": {"color": "pink", "name": "Pink"},
            "lavender": {"color": "white", "name": "White"},
            "white": {"color": "light-green", "name": "Light Green"},
            "light-green": {"color": "lavender", "name": "Lavender"},
        },
        "monochrome": {
            "pure-white": {"color": "medium-gray", "name": "Gray"},
            "medium-gray": {"color": "pure-black", "name": "Black"},
            "pure-black": {"color": "pure-white", "name": "White"},
            "light-gray": {"color": "dark-gray", "name": "Dark Gray"},
            "dark-gray": {"color": "charcoal", "name": "Charcoal"},
            "charcoal": {"color": "light-gray", "name": "Light Gray"},
        },
        "jewel": {
            "ruby": {"color": "emerald", "name": "Emerald"},
            "emerald": {"color": "sapphire", "name": "Sapphire"},
            "sapphire": {"color": "ruby", "name": "Ruby"},
            "plum": {"color": "dark-gold", "name": "Dark Gold"},
            "dark-gold": {"color": "deep-teal", "name": "Deep Teal"},
            "deep-teal": {"color": "plum", "name": "Plum"},
        },
    }

    # next color
    next_color_info = next_colors.get(palette, {}).get(color, None)
    next_color = None
    next_url = None

    if next_color_info:
        next_color = next_color_info["name"]
        next_url = (
            url_for("color_detail")
            + f'?palette={palette}&color={next_color_info["color"]}&name={next_color}'
        )
    print("palette:", palette)
    print("color:", color)
    print("color_name:", color_name)
    print("palette_title:", palette_title)
    print("color_description:", color_description)
    print("next_url:", next_url)

    # Get example images based on palette and color
    images = []
    
    # Earth tones
    if palette == "earth":
        if color == "olive":
            images = [
                "/static/lesson1/olive/olive-brown-outfit-01.jpg",
                "/static/lesson1/olive/olive-brown-outfit-02.jpg",
                "/static/lesson1/olive/olive-red-outfit-01.jpg",
                "/static/lesson1/olive/olive-pants-01.jpg",
                "/static/lesson1/olive/olive-pocket-tee-01.jpg",
                "/static/lesson1/olive/olive-shirt-01.jpg"
            ]
        elif color == "tan":
            images = [
                "/static/lesson1/tan/tan-bike-outfit-01.jpg",
                "/static/lesson1/tan/tan-cardigan-outfit-01.jpg",
                "/static/lesson1/tan/tan-on-tan-outfit-01.jpg",
                "/static/lesson1/tan/tan-cap-01.jpg",
                "/static/lesson1/tan/tan-sweater-01.jpg",
                "/static/lesson1/tan/tan-work-pants-01.jpg"
            ]
        elif color == "brown":
            images = [
                "/static/lesson1/brown/brown-formal-outfit-01.jpg",
                "/static/lesson1/brown/brown-outfit-01.jpg",
                "/static/lesson1/brown/brown-suit-01.jpg",
                "/static/lesson1/brown/brown-belt-01.jpg",
                "/static/lesson1/brown/brown-pants-01.jpg",
                "/static/lesson1/brown/brown-shoes-01.jpg"
            ]
        elif color == "dark-green":
            images = [
                "/static/lesson1/green/green-army-outfit-01.jpg",
                "/static/lesson1/green/green-workwear-outfit-01.jpg",
                "/static/lesson1/green/green-baggy-outfit-01.jpg",
                "/static/lesson1/green/green-corduroy-pants-01.jpg",
                "/static/lesson1/green/green-work-jacket-01.jpg",
                "/static/lesson1/green/green-zoomer-fit-01.jpg"
            ]
        elif color == "rose":
            images = [
                "/static/lesson1/rose/rose-accessories-outfit-01.jpg",
                "/static/lesson1/rose/rose-pants-outfit-01.jpg",
                "/static/lesson1/rose/rose-shirt-outfit-01.jpg",
                "/static/lesson1/rose/rose-beanies-01.jpg",
                "/static/lesson1/rose/rose-glasses-01.jpg",
                "/static/lesson1/rose/rose-jeans-01.jpg"
            ]
        elif color == "terracotta":
            images = [
                "/static/lesson1/terracotta/terracotta-jacket-outfit-01.jpg",
                "/static/lesson1/terracotta/terracotta-pants-outfit-01.jpg",
                "/static/lesson1/terracotta/terracotta-shirt-fit-01.jpg",
                "/static/lesson1/terracotta/terracotta-hat-01.jpg",
                "/static/lesson1/terracotta/terracotta-hoodie-01.jpg",
                "/static/lesson1/terracotta/terracotta-socks-01.jpg"
            ]
    
    return render_template(
        "color-detail.html",
        palette_title=palette_title,
        color_name=color_name,
        color_class=color,
        color_description=color_description,
        back_url=back_url,
        next_color=next_color,
        next_url=next_url,
        images=images
    )


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
        session["current_question"] = 1
        session["correct_answers"] = 0
        session["total_questions"] = len(quiz_qs)
        question = quiz_qs[0]
    else:
        # Get the specified question
        question = get_question_by_id(question_id)
        if not question:
            # If question doesn't exist, start over
            return redirect(url_for("quiz"))
        session["current_question"] = question_id

    # Add only the specified clothing items to the question
    question_with_items = question.copy()
    available_item_ids = question.get("available_items", list(clothing_items.keys()))
    question_with_items["choices"] = [
        clothing_items[item_id]
        for item_id in available_item_ids
        if item_id in clothing_items
    ]

    return render_template(
        "quiz.html",
        question=question_with_items,
        description=question_with_items["description"],
        current=session.get("current_question", 1),
        total=session.get("total_questions", len(quiz_qs)),
    )


@app.route("/quizanswer")
def parse():
    question_id = session.get("current_question", 1)
    question = get_question_by_id(question_id)

    if not question:
        return redirect(url_for("quiz"))

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
        session["correct_answers"] = session.get("correct_answers", 0) + 1

    # Determine if this is the last question
    is_last = question_id >= len(quiz_qs)
    next_question_id = question_id + 1 if not is_last else None

    # Calculate final score if last question
    final_score = None
    if is_last:
        final_score = {
            "correct": session.get("correct_answers", 0),
            "total": session.get("total_questions", len(quiz_qs)),
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
        description=question.get("description", ""),
        clothing_items=clothing_items,
        current_score=session.get("correct_answers", 0),
        total_questions=session.get("total_questions", len(quiz_qs)),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
