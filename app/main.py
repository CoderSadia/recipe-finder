import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

MEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/api/search")
def search_recipes():
    query = request.args.get("q", "")
    if not query:
        return jsonify(error="query parameter 'q' is required"), 400

    response = requests.get(f"{MEALDB_BASE_URL}/search.php", params={"s": query})
    data = response.json()

    meals = data.get("meals") or []
    results = [
        {
            "id": meal["idMeal"],
            "name": meal["strMeal"],
            "image": meal["strMealThumb"],
            "category": meal["strCategory"],
        }
        for meal in meals
    ]

    return jsonify(recipes=results), 200


@app.route("/api/recipe/<recipe_id>")
def recipe_detail(recipe_id):
    response = requests.get(f"{MEALDB_BASE_URL}/lookup.php", params={"i": recipe_id})
    data = response.json()

    meals = data.get("meals")
    if not meals:
        return jsonify(error="recipe not found"), 404

    meal = meals[0]

    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")
        if ingredient and ingredient.strip():
            ingredients.append(f"{measure.strip()} {ingredient.strip()}")

    return jsonify(
        id=meal["idMeal"],
        name=meal["strMeal"],
        image=meal["strMealThumb"],
        category=meal["strCategory"],
        area=meal["strArea"],
        instructions=meal["strInstructions"],
        ingredients=ingredients,
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
