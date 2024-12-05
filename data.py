import mysql.connector
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/cooking_recipe'
db = SQLAlchemy(app)

# JSON data
data = {
    "recipes": [
        {
            "id": 1,
            "title": "Chicken Curry",
            "images": "images/chicken_curry.jpg",
            "instructions": "1. Heat oil in a pan. 2. Add onions and sauté until golden. 3. Add ginger-garlic paste, followed by tomatoes. 4. Cook until tomatoes are soft. 5. Add chicken and spices. 6. Cook until chicken is tender. 7. Garnish with cilantro and serve."
        },
        {
            "id": 2,
            "title": "Paneer Butter Masala",
            "images": "images/panner_butter_masala.jpg",
            "instructions": "1. Heat butter in a pan. 2. Add onions and sauté until translucent. 3. Add tomatoes and cook until soft. 4. Blend the mixture into a smooth paste. 5. Add paneer cubes and spices. 6. Cook until paneer is well-coated. 7. Garnish with cream and serve."
        },
        {
            "id": 3,
            "title": "Chole Bhature",
            "images": "images/chola_bhature.jpg",
            "instructions": "1. Soak chickpeas overnight. 2. Cook chickpeas with spices until tender. 3. Prepare bhature dough and let it rest. 4. Roll out dough and deep fry. 5. Serve bhature with chole."
        },
        {
            "id": 4,
            "title": "Aloo Gobi",
            "images": "images/aloo_gobi.jpg",
            "instructions": "1. Heat oil in a pan. 2. Add cumin seeds and let them splutter. 3. Add potatoes and cauliflower. 4. Add spices and cook until vegetables are tender. 5. Garnish with cilantro and serve."
        },
        {
            "id": 5,
            "title": "Palak Paneer",
            "images": "images/palak_panner.jpg",
            "instructions": "1. Blanch spinach leaves and blend into a paste. 2. Heat oil and add cumin seeds. 3. Add onions, tomatoes, and cook until soft. 4. Add spinach paste and paneer cubes. 5. Cook until well-mixed and serve."
        },
        {
            "id": 6,
            "title": "Rajma",
            "images": "images/rajma.jpg",
            "instructions": "1. Soak kidney beans overnight. 2. Cook beans with spices until tender. 3. Prepare a tomato-onion gravy. 4. Mix beans with gravy and cook until thickened. 5. Garnish with cilantro and serve."
        },
        {
            "id": 7,
            "title": "Dal Tadka",
            "images": "images/dal_tadka.jpg",
            "instructions": "1. Cook lentils with turmeric and salt. 2. Prepare a tempering of garlic, onions, and spices. 3. Mix tempering with cooked dal. 4. Garnish with cilantro and serve."
        },
        {
            "id": 8,
            "title": "Bhindi Masala",
            "images": "images/bhindhi_masala.jpg",
            "instructions": "1. Heat oil in a pan. 2. Add cumin seeds and let them splutter. 3. Add sliced okra and cook until tender. 4. Add spices and mix well. 5. Serve hot."
        },
        {
            "id": 9,
            "title": "Dosa",
            "images": "images/dosa.jpg",
            "instructions": "1. Soak rice and urad dal overnight. 2. Grind to a smooth batter. 3. Heat a griddle and pour batter to form a thin layer. 4. Cook until crisp and golden. 5. Serve with chutney and sambar."
        },
        {
            "id": 10,
            "title": "Pulao",
            "images": "images/pulao.jpg",
            "instructions": "1. Heat oil and sauté onions and spices. 2. Add rice and vegetables. 3. Cook with water until rice is fluffy. 4. Garnish with cilantro and serve."
        },
        {
            "id": 11,
            "title": "Chicken Fry",
            "images": "images/chicken_fry.jpg",
            "instructions": "1. Marinate chicken with spices and yogurt. 2. Heat oil in a pan. 3. Fry the marinated chicken until golden and crispy. 4. Garnish with cilantro and serve with lemon wedges."
        },
        {
            "id": 12,
            "title": "Chicken Biryani",
            "images": "images/chicken_biryani.jpg",
            "instructions": "1. Marinate chicken with spices and yogurt. 2. Cook rice with whole spices. 3. Layer chicken and rice in a pot, adding fried onions, mint, and cilantro. 4. Cook on low heat until flavors meld together. 5. Serve with raita."
        }
    ],
    "ingredients": [
        {
            "id": 1,
            "ingredient_name": "Chicken"
        },
        {
            "id": 2,
            "ingredient_name": "Paneer"
        },
        {
            "id": 3,
            "ingredient_name": "Chickpeas"
        },
        {
            "id": 4,
            "ingredient_name": "Potatoes"
        },
        {
            "id": 5,
            "ingredient_name": "Spinach"
        },
        {
            "id": 6,
            "ingredient_name": "Kidney Beans"
        },
        {
            "id": 7,
            "ingredient_name": "Lentils"
        },
        {
            "id": 8,
            "ingredient_name": "Okra"
        },
        {
            "id": 9,
            "ingredient_name": "Rice"
        },
        {
            "id": 10,
            "ingredient_name": "Vegetables"
        },
        {
            "id": 11,
            "ingredient_name": "Cilantro"
        },
        {
            "id": 12,
            "ingredient_name": "Turmeric"
        },
        {
            "id": 13,
            "ingredient_name": "Cumin Seeds"
        },
        {
            "id": 14,
            "ingredient_name": "Garam Masala"
        },
        {
            "id": 15,
            "ingredient_name": "Red Chili Powder"
        },
        {
            "id": 16,
            "ingredient_name": "Coriander Powder"
        },
        {
            "id": 17,
            "ingredient_name": "Yogurt"
        },
        {
            "id": 18,
            "ingredient_name": "Fenugreek Leaves"
        },
        {
            "id": 19,
            "ingredient_name": "Bay Leaf"
        },
        {
            "id": 20,
            "ingredient_name": "Cinnamon Stick"
        },
        {
            "id": 21,
            "ingredient_name": "Cloves"
        },
        {
            "id": 22,
            "ingredient_name": "Green Cardamom"
        },
        {
            "id": 23,
            "ingredient_name": "Mustard Seeds"
        },
        {
            "id": 24,
            "ingredient_name": "Coconut Milk"
        },
        {
            "id": 25,
            "ingredient_name": "Green Chilies"
        },
        {
            "id": 26,
            "ingredient_name": "Tamarind"
        },
        {
            "id": 27,
            "ingredient_name": "Curry Leaves"
        },
        {
            "id": 28,
            "ingredient_name": "Black Pepper"
        },
        {
            "id": 29,
            "ingredient_name": "Ghee"
        },
        {
            "id": 30,
            "ingredient_name": "Mint Leaves"
        },
        {
            "id": 31,
            "ingredient_name": "Onions"
        },
        {
            "id": 32,
            "ingredient_name": "Ginger-Garlic Paste"
        },
        {
            "id": 33,
            "ingredient_name": "Lemon"
        }
    ],
    "recipe_ingredient": [
        {
            "id": 1,
            "recipe_id": 1,
            "ingredient_id": 1,
            "quantity": 500,
            "units": "grams"
        },
        {
            "id": 2,
            "recipe_id": 1,
            "ingredient_id": 13,
            "quantity": 1,
            "units": "tsp"
        },
        {
            "id": 3,
            "recipe_id": 1,
            "ingredient_id": 12,
            "quantity": 1,
            "units": "tsp"
        },
        {
            "id": 4,
            "recipe_id": 1,
            "ingredient_id": 17,
            "quantity": 2,
            "units": "tbsp"
        },
        {
            "id": 5,
            "recipe_id": 1,
            "ingredient_id": 31,
            "quantity": 2,
            "units": "medium"
        },
        {
            "id": 6,
            "recipe_id": 2,
            "ingredient_id": 2,
            "quantity": 200,
            "units": "grams"
        },
        {
            "id": 7,
            "recipe_id": 2,
            "ingredient_id": 31,
            "quantity": 2,
            "units": "medium"
        },
        {
            "id": 8,
            "recipe_id": 2,
            "ingredient_id": 32,
            "quantity": 1,
            "units": "tbsp"
        },
        {
            "id": 9,
            "recipe_id": 3,
            "ingredient_id": 3,
            "quantity": 1,
            "units": "cup"
        },
        {
            "id": 10,
            "recipe_id": 3,
            "ingredient_id": 31,
            "quantity": 1,
            "units": "large"
        },
        {
            "id": 11,
            "recipe_id": 4,
            "ingredient_id": 4,
            "quantity": 2,
            "units": "large"
        },
        {
            "id": 12,
            "recipe_id": 4,
            "ingredient_id": 10,
            "quantity": 1,
            "units": "cup"
        },
        {
            "id": 13,
            "recipe_id": 5,
            "ingredient_id": 5,
            "quantity": 250,
            "units": "grams"
        },
        {
            "id": 14,
            "recipe_id": 5,
            "ingredient_id": 2,
            "quantity": 200,
            "units": "grams"
        },
        {
            "id": 15,
            "recipe_id": 6,
            "ingredient_id": 6,
            "quantity": 1,
            "units": "cup"
        },
        {
            "id": 16,
            "recipe_id": 6,
            "ingredient_id": 32,
            "quantity": 1,
            "units": "tbsp"
        },
        {
            "id": 17,
            "recipe_id": 7,
            "ingredient_id": 7,
            "quantity": 1,
            "units": "cup"
        },
        {
            "id": 18,
            "recipe_id": 7,
            "ingredient_id": 16,
            "quantity": 1,
            "units": "tsp"
        },
        {
            "id": 19,
            "recipe_id": 8,
            "ingredient_id": 8,
            "quantity": 300,
            "units": "grams"
        },
        {
            "id": 20,
            "recipe_id": 8,
            "ingredient_id": 13,
            "quantity": 1,
            "units": "tsp"
        },
        {
            "id": 21,
            "recipe_id": 9,
            "ingredient_id": 9,
            "quantity": 2,
            "units": "cups"
        },
        {
            "id": 22,
            "recipe_id": 9,
            "ingredient_id": 31,
            "quantity": 1,
            "units": "medium"
        },
        {
            "id": 23,
            "recipe_id": 10,
            "ingredient_id": 9,
            "quantity": 1,
            "units": "cup"
        },
        {
            "id": 24,
            "recipe_id": 10,
            "ingredient_id": 10,
            "quantity": 1,
            "units": "cup"
        },
        {
            "id": 25,
            "recipe_id": 11,
            "ingredient_id": 1,
            "quantity": 500,
            "units": "grams"
        },
        {
            "id": 26,
            "recipe_id": 11,
            "ingredient_id": 16,
            "quantity": 1,
            "units": "tbsp"
        },
        {
            "id": 27,
            "recipe_id": 12,
            "ingredient_id": 1,
            "quantity": 500,
            "units": "grams"
        },
        {
            "id": 28,
            "recipe_id": 12,
            "ingredient_id": 9,
            "quantity": 2,
            "units": "cups"
        }
    ]
}

def add_data_to_db():
    with app.app_context():
        
        for recipe in data['recipes']:
            db.session.execute(
                text("""
                    INSERT INTO recipes (id, title, images, instructions)
                    VALUES (:id, :title, :images, :instructions)
                    ON DUPLICATE KEY UPDATE
                    title = VALUES(title), images = VALUES(images), instructions = VALUES(instructions)
                """), recipe
            )
        print("Recipes inserted/updated successfully.")
        
        
        for ingredient in data['ingredients']:
            db.session.execute(
                text("""
                    INSERT INTO ingredients (id, ingredient_name)
                    VALUES (:id, :ingredient_name)
                    ON DUPLICATE KEY UPDATE
                    ingredient_name = VALUES(ingredient_name)
                """), ingredient
            )
        print("Ingredients inserted/updated successfully.")

        
        for ri in data['recipe_ingredient']:
            db.session.execute(
                text("""
                    INSERT INTO recipe_ingredient (id, recipe_id, ingredient_id, quantity, units)
                    VALUES (:id, :recipe_id, :ingredient_id, :quantity, :units)
                    ON DUPLICATE KEY UPDATE
                    recipe_id = VALUES(recipe_id), ingredient_id = VALUES(ingredient_id), 
                    quantity = VALUES(quantity), units = VALUES(units)
                """), ri
            )
        print("Recipe ingredients inserted/updated successfully.")

        db.session.commit()
        print("All data inserted/updated successfully and committed to the database.")

if __name__ == "__main__":
    add_data_to_db()

