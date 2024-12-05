from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sqlalchemy.exc import IntegrityError
import re
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/cooking_recipe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    images = db.Column(db.String(255), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    ingredients = db.relationship('Ingredient', secondary='recipe_ingredient', back_populates='recipes')
    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='recipe')

    def __repr__(self):
        return f"Recipe('{self.title}', '{self.images}')"

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(255), nullable=False)
    recipes = db.relationship('Recipe', secondary='recipe_ingredient', back_populates='ingredients')
    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='ingredient')

    def __repr__(self):
        return f"Ingredient('{self.ingredient_name}')"

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    quantity = db.Column(db.String(255))
    units = db.Column(db.String(255))

    recipe = db.relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipe_ingredients')

    def __repr__(self):
        return f"RecipeIngredient('{self.recipe_id}', '{self.ingredient_id}', '{self.quantity}', '{self.units}')"

class RecipeFavorite(db.Model):
    __tablename__ = 'recipe_favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('favorites', lazy=True))
    recipe = db.relationship('Recipe', backref=db.backref('favorited_by', lazy=True))

    def __repr__(self):
        return f"RecipeFavorite('{self.user_id}', '{self.recipe_id}')"

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=255)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=12)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_password(self, password):
        if len(password.data) < 12:
            raise ValidationError('Password must be at least 12 characters long.')
        if not re.search(r'[A-Z]', password.data):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password.data):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', password.data):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password.data):
            raise ValidationError('Password must contain at least one special character.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('recipes'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('This email is already in use. Please choose a different one.', 'danger')
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('recipes'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
              
            return redirect(url_for('recipes'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

@app.route('/recipes', methods=['GET'])
@login_required
def recipes():
    query = request.args.get('query', '')  

    if query:
        
        recipes = Recipe.query.filter(Recipe.title.ilike(f'%{query}%')).all()
    else:
        
        recipes = Recipe.query.all()

    return render_template('recipes.html', recipes=recipes, query=query)
@app.route('/recipe/<int:recipe_id>')
@login_required
def view_recipe(recipe_id):
    selected_recipe = Recipe.query.get(recipe_id)
    if selected_recipe:
        ingredients = (db.session.query(Ingredient)
                       .join(RecipeIngredient)
                       .filter(RecipeIngredient.recipe_id == recipe_id)
                       .all())
        is_favorite = RecipeFavorite.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first() is not None
        return render_template('recipe_detail.html', selected_recipe=selected_recipe, selected_ingredients=ingredients, is_favorite=is_favorite)
    else:
        flash('Recipe not found.', 'danger')
        return redirect(url_for('recipes'))

@app.route('/toggle_favorite/<int:recipe_id>', methods=['POST'])
@login_required
def toggle_favorite(recipe_id):
    user_id = current_user.id
    favorite = RecipeFavorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if favorite:
       
        db.session.delete(favorite)
        flash('Recipe removed from favorites.', 'success')
    else:
        
        new_favorite = RecipeFavorite(user_id=user_id, recipe_id=recipe_id)
        db.session.add(new_favorite)
        flash('Recipe added to favorites.', 'success')

    db.session.commit()
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/favorites')
@login_required
def favorites():
    favorites = RecipeFavorite.query.filter_by(user_id=current_user.id).all()
    recipes = [fav.recipe for fav in favorites]
    return render_template('favorite.html', recipes=recipes)

@app.context_processor
def inject_user():
    return dict(logged_in_user=current_user if current_user.is_authenticated else None)

if __name__ == '__main__':
    app.run(debug=True)
