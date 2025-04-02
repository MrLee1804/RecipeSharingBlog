from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import os
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# CSV file paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
RECIPES_FILE = os.path.join(BASE_DIR, 'data', 'recipes.csv')
USERS_FILE = os.path.join(BASE_DIR, 'data', 'users.csv')
CATEGORIES_FILE = os.path.join(BASE_DIR, 'data', 'categories.csv')
COMMENTS_FILE = os.path.join(BASE_DIR, 'data', 'comments.csv')
RATINGS_FILE = os.path.join(BASE_DIR, 'data', 'ratings.csv')
FAVORITES_FILE = os.path.join(BASE_DIR, 'data', 'favorites.csv')

# Ensure data directory exists
os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)

# Initialize CSV files if they don't exist
def init_csv_files():
    """Initialize CSV files with default data if they don't exist"""
    # Initialize users.csv
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password_hash', 'email', 'bio', 'join_date'])
            # Add default admin user
            writer.writerow(['admin', generate_password_hash('admin123'), 'admin@example.com', 'Admin User', datetime.now().strftime('%Y-%m-%d')])
    
    # Initialize recipes.csv
    if not os.path.exists(RECIPES_FILE):
        with open(RECIPES_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'description', 'ingredients', 'instructions', 'author', 'image_url', 'category', 'prep_time', 'cook_time', 'servings', 'date'])
            # Add some default recipes
            default_recipes = [
                {
                    'id': 1,
                    'title': 'Classic Chocolate Cake',
                    'description': 'A moist and rich chocolate cake that\'s perfect for any occasion.',
                    'ingredients': '2 cups flour\n2 cups sugar\n3/4 cup cocoa powder\n2 eggs\n1 cup milk\n1/2 cup vegetable oil\n2 tsp vanilla extract\n1 tsp baking soda\n1/2 tsp salt',
                    'instructions': '1. Preheat oven to 350°F\n2. Mix dry ingredients\n3. Add wet ingredients\n4. Bake for 30-35 minutes',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Desserts',
                    'prep_time': 20,
                    'cook_time': 35,
                    'servings': 12,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 2,
                    'title': 'Spaghetti Carbonara',
                    'description': 'Classic Italian pasta dish with eggs, cheese, and pancetta.',
                    'ingredients': '400g spaghetti\n200g pancetta\n4 large eggs\n100g Pecorino Romano\n100g Parmigiano Reggiano\nBlack pepper\nSalt',
                    'instructions': '1. Cook pasta\n2. Fry pancetta\n3. Mix eggs and cheese\n4. Combine all ingredients',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1612874742237-6526221588e3?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Main Course',
                    'prep_time': 15,
                    'cook_time': 20,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 3,
                    'title': 'Caesar Salad',
                    'description': 'Fresh and crispy Caesar salad with homemade dressing.',
                    'ingredients': '1 head romaine lettuce\n1 cup croutons\n1/2 cup parmesan cheese\n1/4 cup olive oil\n2 tbsp lemon juice\n1 egg yolk\n2 cloves garlic\nSalt and pepper',
                    'instructions': '1. Chop lettuce\n2. Make dressing\n3. Toss ingredients\n4. Add cheese and croutons',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1546793665-c74683f339c1?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Salads',
                    'prep_time': 15,
                    'cook_time': 0,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 4,
                    'title': 'Chicken Stir-Fry',
                    'description': 'Quick and healthy Asian-style chicken stir-fry with vegetables.',
                    'ingredients': '500g chicken breast\n2 bell peppers\n1 onion\n2 carrots\n3 tbsp soy sauce\n2 cloves garlic\n1 tbsp ginger\n2 tbsp oil',
                    'instructions': '1. Cut chicken and vegetables\n2. Heat oil\n3. Stir-fry chicken\n4. Add vegetables and sauce',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Quick Meals',
                    'prep_time': 20,
                    'cook_time': 15,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 5,
                    'title': 'Apple Pie',
                    'description': 'Classic American apple pie with cinnamon and nutmeg.',
                    'ingredients': '6 apples\n1 cup sugar\n1 tsp cinnamon\n1/4 tsp nutmeg\n2 pie crusts\n2 tbsp butter',
                    'instructions': '1. Peel and slice apples\n2. Mix with spices\n3. Fill pie crust\n4. Bake for 45 minutes',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1571115177098-24ec42ed204d?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Baking',
                    'prep_time': 30,
                    'cook_time': 45,
                    'servings': 8,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 6,
                    'title': 'Minestrone Soup',
                    'description': 'Hearty Italian vegetable soup with pasta and beans.',
                    'ingredients': '2 carrots\n2 celery stalks\n1 onion\n2 cloves garlic\n1 can tomatoes\n1 can beans\n1 cup pasta\nVegetable broth',
                    'instructions': '1. Chop vegetables\n2. Sauté aromatics\n3. Add broth and vegetables\n4. Simmer for 30 minutes',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Soups',
                    'prep_time': 20,
                    'cook_time': 30,
                    'servings': 6,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 7,
                    'title': 'Greek Salad',
                    'description': 'Fresh Mediterranean salad with feta cheese and olives.',
                    'ingredients': '2 tomatoes\n1 cucumber\n1 red onion\n1 cup olives\n200g feta cheese\nExtra virgin olive oil\nOregano',
                    'instructions': '1. Chop vegetables\n2. Add olives and feta\n3. Dress with oil\n4. Sprinkle oregano',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Salads',
                    'prep_time': 15,
                    'cook_time': 0,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 8,
                    'title': 'Beef Tacos',
                    'description': 'Mexican-style beef tacos with fresh toppings.',
                    'ingredients': '500g ground beef\nTaco seasoning\nTortillas\nLettuce\nTomatoes\nOnion\nCheese\nSour cream',
                    'instructions': '1. Brown beef\n2. Add seasoning\n3. Warm tortillas\n4. Assemble tacos',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Main Course',
                    'prep_time': 20,
                    'cook_time': 15,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 9,
                    'title': 'Chocolate Chip Cookies',
                    'description': 'Classic homemade chocolate chip cookies.',
                    'ingredients': '2 1/4 cups flour\n1 cup butter\n3/4 cup sugar\n2 eggs\n2 cups chocolate chips\n1 tsp vanilla\n1 tsp baking soda',
                    'instructions': '1. Mix ingredients\n2. Form cookies\n3. Bake for 10 minutes\n4. Cool on rack',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Baking',
                    'prep_time': 15,
                    'cook_time': 10,
                    'servings': 24,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 10,
                    'title': 'Tomato Basil Soup',
                    'description': 'Creamy tomato soup with fresh basil.',
                    'ingredients': '2 cans tomatoes\n1 onion\n2 cloves garlic\nFresh basil\nHeavy cream\nButter\nSalt and pepper',
                    'instructions': '1. Sauté vegetables\n2. Add tomatoes\n3. Simmer\n4. Blend and add cream',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Soups',
                    'prep_time': 15,
                    'cook_time': 25,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 11,
                    'title': 'Breakfast Burrito',
                    'description': 'Hearty breakfast burrito with eggs, potatoes, and sausage.',
                    'ingredients': '4 eggs\n2 potatoes\n200g sausage\nTortillas\nCheese\nBell peppers\nOnion',
                    'instructions': '1. Cook potatoes\n2. Fry sausage\n3. Scramble eggs\n4. Assemble burrito',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1551788038-d6bb94b5b9f9?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Breakfast',
                    'prep_time': 15,
                    'cook_time': 20,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 12,
                    'title': 'Vegetable Curry',
                    'description': 'Spicy vegetable curry with coconut milk.',
                    'ingredients': 'Mixed vegetables\nCoconut milk\nCurry powder\nGinger\nGarlic\nOnion\nRice',
                    'instructions': '1. Sauté aromatics\n2. Add vegetables\n3. Add coconut milk\n4. Simmer until tender',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Vegetarian',
                    'prep_time': 20,
                    'cook_time': 30,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 13,
                    'title': 'Smoothie Bowl',
                    'description': 'Healthy smoothie bowl with fresh fruits and granola.',
                    'ingredients': 'Banana\nMixed berries\nSpinach\nAlmond milk\nGranola\nChia seeds\nHoney',
                    'instructions': '1. Blend fruits\n2. Pour in bowl\n3. Top with granola\n4. Add toppings',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Breakfast',
                    'prep_time': 10,
                    'cook_time': 0,
                    'servings': 2,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 14,
                    'title': 'Homemade Pizza',
                    'description': 'Classic homemade pizza with fresh toppings.',
                    'ingredients': 'Pizza dough\nTomato sauce\nMozzarella\nFresh basil\nOlive oil\nToppings of choice',
                    'instructions': '1. Roll out dough\n2. Add sauce\n3. Add toppings\n4. Bake at high heat',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Main Course',
                    'prep_time': 30,
                    'cook_time': 15,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 15,
                    'title': 'Mango Sorbet',
                    'description': 'Refreshing mango sorbet with lime.',
                    'ingredients': '3 ripe mangoes\nSugar\nLime juice\nWater',
                    'instructions': '1. Blend mangoes\n2. Add sugar\n3. Freeze\n4. Stir occasionally',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1501446529957-6226bd3c01d3?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Desserts',
                    'prep_time': 15,
                    'cook_time': 0,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 16,
                    'title': 'Quinoa Buddha Bowl',
                    'description': 'Healthy quinoa bowl with roasted vegetables.',
                    'ingredients': 'Quinoa\nMixed vegetables\nChickpeas\nTahini dressing\nAvocado\nKale',
                    'instructions': '1. Cook quinoa\n2. Roast vegetables\n3. Make dressing\n4. Assemble bowl',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Vegetarian',
                    'prep_time': 20,
                    'cook_time': 25,
                    'servings': 2,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 17,
                    'title': 'Lemonade',
                    'description': 'Fresh homemade lemonade with mint.',
                    'ingredients': 'Lemons\nSugar\nWater\nFresh mint\nIce',
                    'instructions': '1. Juice lemons\n2. Make simple syrup\n3. Mix ingredients\n4. Add mint',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1622493576007-d4a9f24c0b60?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Beverages',
                    'prep_time': 10,
                    'cook_time': 0,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 18,
                    'title': 'Trail Mix',
                    'description': 'Healthy homemade trail mix with nuts and dried fruits.',
                    'ingredients': 'Mixed nuts\nDried fruits\nDark chocolate\nSeeds\nCoconut flakes',
                    'instructions': '1. Mix ingredients\n2. Store in airtight container',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Snacks',
                    'prep_time': 10,
                    'cook_time': 0,
                    'servings': 8,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 19,
                    'title': 'Sourdough Bread',
                    'description': 'Classic sourdough bread with crispy crust.',
                    'ingredients': 'Sourdough starter\nFlour\nWater\nSalt',
                    'instructions': '1. Feed starter\n2. Mix dough\n3. Ferment\n4. Bake',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Baking',
                    'prep_time': 30,
                    'cook_time': 45,
                    'servings': 12,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 20,
                    'title': '15-Minute Pasta',
                    'description': 'Quick and easy pasta dish with fresh ingredients.',
                    'ingredients': 'Pasta\nCherry tomatoes\nGarlic\nBasil\nOlive oil\nParmesan',
                    'instructions': '1. Cook pasta\n2. Sauté garlic\n3. Add tomatoes\n4. Toss with basil',
                    'author': 'admin',
                    'image_url': 'https://images.unsplash.com/photo-1612874742237-6526221588e3?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    'category': 'Quick Meals',
                    'prep_time': 5,
                    'cook_time': 10,
                    'servings': 4,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
            for recipe in default_recipes:
                writer.writerow([
                    recipe['id'],
                    recipe['title'],
                    recipe['description'],
                    recipe['ingredients'],
                    recipe['instructions'],
                    recipe['author'],
                    recipe['image_url'],
                    recipe['category'],
                    recipe['prep_time'],
                    recipe['cook_time'],
                    recipe['servings'],
                    recipe['date']
                ])
    
    # Initialize categories.csv
    if not os.path.exists(CATEGORIES_FILE):
        with open(CATEGORIES_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'description'])
            default_categories = [
                [1, 'Main Course', 'Hearty main dishes'],
                [2, 'Desserts', 'Sweet treats and desserts'],
                [3, 'Salads', 'Fresh and healthy salads'],
                [4, 'Soups', 'Warm and comforting soups'],
                [5, 'Breakfast', 'Morning meals and brunch'],
                [6, 'Snacks', 'Quick and easy snacks'],
                [7, 'Beverages', 'Refreshing drinks'],
                [8, 'Vegetarian', 'Meat-free recipes'],
                [9, 'Quick Meals', '30 minutes or less'],
                [10, 'Baking', 'Bread and baked goods']
            ]
            writer.writerows(default_categories)
    
    # Initialize comments.csv
    if not os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'recipe_id', 'user', 'comment', 'date'])
    
    # Initialize favorites.csv
    if not os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user', 'recipe_id'])

init_csv_files()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    recipes = []
    categories = []
    search_query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    # Get all categories
    with open(CATEGORIES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        categories = list(reader)
    
    # Get recipes with optional filtering
    with open(RECIPES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        recipes = list(reader)
        
        # Apply search filter
        if search_query:
            recipes = [r for r in recipes if search_query.lower() in r['title'].lower() or 
                      search_query.lower() in r['description'].lower()]
        
        # Apply category filter
        if category:
            recipes = [r for r in recipes if r.get('category', '').lower() == category.lower()]
    
    return render_template('index.html', recipes=recipes, categories=categories, 
                         search_query=search_query, selected_category=category)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = None
    comments = []
    rating = 0
    user_rating = 0
    is_favorite = False
    
    # Get recipe details
    with open(RECIPES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if int(r['id']) == recipe_id:
                recipe = r
                break
    
    if not recipe:
        flash('Recipe not found.', 'error')
        return redirect(url_for('index'))
    
    # Get comments
    with open(COMMENTS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        comments = [c for c in reader if int(c['recipe_id']) == recipe_id]
    
    # Get average rating
    with open(RATINGS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        ratings = [int(r['rating']) for r in reader if int(r['recipe_id']) == recipe_id]
        if ratings:
            rating = sum(ratings) / len(ratings)
    
    # Get user's rating if logged in
    if 'username' in session:
        with open(RATINGS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                if int(r['recipe_id']) == recipe_id and r['user'] == session['username']:
                    user_rating = int(r['rating'])
                    break
        
        # Check if recipe is in user's favorites
        with open(FAVORITES_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for fave in reader:
                if int(fave['recipe_id']) == recipe_id and fave['user'] == session['username']:
                    is_favorite = True
                    break
    
    return render_template('recipe_detail.html', recipe=recipe, comments=comments,
                         rating=rating, user_rating=user_rating, is_favorite=is_favorite)

@app.route('/profile/<username>')
def user_profile(username):
    user = None
    user_recipes = []
    favorite_recipes = []
    
    # Get user details
    with open(USERS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for u in reader:
            if u['username'] == username:
                user = {
                    'username': u['username'],
                    'email': u.get('email', ''),
                    'bio': u.get('bio', ''),
                    'join_date': u.get('join_date', 'Unknown')
                }
                break
    
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('index'))
    
    # Get user's recipes
    with open(RECIPES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        user_recipes = [r for r in reader if r['author'] == username]
    
    # Get user's favorite recipes
    with open(FAVORITES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        favorite_ids = [int(f['recipe_id']) for f in reader if f['user'] == username]
        
        with open(RECIPES_FILE, 'r') as f:
            reader = csv.DictReader(f)
            favorite_recipes = [r for r in reader if int(r['id']) in favorite_ids]
    
    return render_template('user_profile.html', user=user, recipes=user_recipes,
                         favorite_recipes=favorite_recipes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with open(USERS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for user in reader:
                if user['username'] == username and check_password_hash(user['password_hash'], password):
                    session['username'] = username
                    flash('Logged in successfully!', 'success')
                    return redirect(url_for('index'))
        
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        with open(USERS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for user in reader:
                if user['username'] == username:
                    flash('Username already exists.', 'error')
                    return redirect(url_for('register'))
        
        # Add new user
        with open(USERS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, generate_password_hash(password)])
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        description = request.form['description']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        image_url = request.form['image_url']
        category = request.form['category']
        prep_time = request.form['prep_time']
        cook_time = request.form['cook_time']
        servings = request.form['servings']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get the next recipe ID
        with open(RECIPES_FILE, 'r') as f:
            reader = csv.DictReader(f)
            recipes = list(reader)
            next_id = len(recipes) + 1
        
        # Add the new recipe
        with open(RECIPES_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                next_id,
                title,
                description,
                ingredients,
                instructions,
                session['username'],
                image_url,
                category,
                prep_time,
                cook_time,
                servings,
                date
            ])
        
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=next_id))
    
    # Get categories for the form
    with open(CATEGORIES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        categories = list(reader)
    
    return render_template('add_recipe.html', categories=categories)

@app.route('/add_comment/<int:recipe_id>', methods=['POST'])
@login_required
def add_comment(recipe_id):
    comment = request.form.get('comment')
    if comment:
        # Get the next available comment ID
        with open(COMMENTS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            comment_id = max([int(c['id']) for c in reader]) + 1 if reader else 1
        
        # Add new comment
        with open(COMMENTS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                comment_id,
                recipe_id,
                session['username'],
                comment,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        flash('Comment added successfully!', 'success')
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))

@app.route('/rate_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    rating = int(request.form.get('rating', 0))
    if 1 <= rating <= 5:
        # Remove existing rating if any
        with open(RATINGS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            ratings = [r for r in reader if not (int(r['recipe_id']) == recipe_id and r['user'] == session['username'])]
        
        # Add new rating
        with open(RATINGS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['recipe_id', 'user', 'rating'])
            for r in ratings:
                writer.writerow([r['recipe_id'], r['user'], r['rating']])
            writer.writerow([recipe_id, session['username'], rating])
        
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/toggle_favorite/<int:recipe_id>', methods=['POST'])
@login_required
def toggle_favorite(recipe_id):
    # Check if recipe is in favorites
    with open(FAVORITES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        favorites = [f for f in reader if not (int(f['recipe_id']) == recipe_id and f['user'] == session['username'])]
    
    # Toggle favorite status
    with open(FAVORITES_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user', 'recipe_id'])
        for fav in favorites:
            writer.writerow([fav['user'], fav['recipe_id']])
    
    return jsonify({'success': True})

@app.route('/dashboard')
@login_required
def dashboard():
    user = None
    recipes = []
    favorite_recipes = []
    comments = []
    
    # Get user details
    with open(USERS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for u in reader:
            if u['username'] == session['username']:
                user = {
                    'username': u['username'],
                    'email': u.get('email', ''),
                    'bio': u.get('bio', ''),
                    'join_date': u.get('join_date', 'Unknown')
                }
                break
    
    # Get user's recipes
    with open(RECIPES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        recipes = [r for r in reader if r['author'] == session['username']]
    
    # Get user's favorite recipes
    with open(FAVORITES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        favorite_ids = [int(f['recipe_id']) for f in reader if f['user'] == session['username']]
        
        with open(RECIPES_FILE, 'r') as f:
            reader = csv.DictReader(f)
            favorite_recipes = [r for r in reader if int(r['id']) in favorite_ids]
    
    # Get user's comments
    with open(COMMENTS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        comments = [c for c in reader if c['user'] == session['username']]
    
    return render_template('dashboard.html', user=user, recipes=recipes,
                         favorite_recipes=favorite_recipes, comments=comments)

@app.route('/edit_profile/<username>', methods=['POST'])
@login_required
def edit_profile(username):
    if username != session['username']:
        flash('You can only edit your own profile.', 'error')
        return redirect(url_for('dashboard'))
    
    email = request.form.get('email', '')
    bio = request.form.get('bio', '')
    
    # Read all users
    with open(USERS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        users = list(reader)
    
    # Update user's information
    with open(USERS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'password_hash', 'email', 'bio', 'join_date'])
        for user in users:
            if user['username'] == username:
                writer.writerow([
                    user['username'],
                    user['password_hash'],
                    email,
                    bio,
                    user.get('join_date', datetime.now().strftime('%Y-%m-%d'))
                ])
            else:
                writer.writerow([
                    user['username'],
                    user['password_hash'],
                    user.get('email', ''),
                    user.get('bio', ''),
                    user.get('join_date', datetime.now().strftime('%Y-%m-%d'))
                ])
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
