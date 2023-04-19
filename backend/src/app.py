from flask import Flask, request, jsonify
import dotenv
import os
from src.models import db, User, Category, Password
from src.decorators import validate_password, validate_username
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager, create_refresh_token
from datetime import timedelta

dotenv.load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwordin.db'
app.config['JWT_SECRET_KEY'] = os.getenv("jwt_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)
db.init_app(app=app)


@app.route('/', methods=['GET'])
def index():
    return 'Ohkay ✅'


@app.route('/create-user', methods=["POST"])
@validate_username
@validate_password
def create_user():
    data = request.json
    username = data["username"]
    password = data['password']
    user_count = User.query.filter_by(username=username).count()
    if user_count == 0:
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Successfully created user"}), 201
    else:
        return jsonify({"message": "Username already taken"}), 409


@app.route('/login', methods=['POST'])
@validate_password
@validate_username
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify({'access_token': access_token, "refresh_token": refresh_token}), 200


@app.route('/check', methods=["GET"])
@jwt_required()
def check():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}! This endpoint is protected by JWT.'}), 200


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    username = get_jwt_identity()
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify({'access_token': access_token, "refresh_token": refresh_token}), 200


@app.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json()
    name = data.get('name')

    category = Category(name=name)

    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Category created successfully.'}), 201


@app.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        return jsonify({'message': 'Category not found.'}), 404

    data = request.get_json()
    category.name = data.get('name', category.name)

    db.session.commit()

    return jsonify({'message': 'Category updated successfully.'}), 200


@app.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        return jsonify({'message': 'Category not found.'}), 404

    # Move associated passwords to a new "uncategorized" category
    uncategorized = Category.query.filter_by(name='uncategorized').first()
    if not uncategorized:
        uncategorized = Category(name='uncategorized')
        db.session.add(uncategorized)

    for password in category.passwords:
        password.category = uncategorized

    db.session.delete(category)
    db.session.commit()

    return jsonify({'message': 'Category deleted successfully.'}), 200


@app.route('/passwords', methods=['POST'])
@jwt_required()
def create_password():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    notes = data.get('notes')
    category_id = data.get('category_id')

    password = Password(name=name, email=email, password=password,
                        notes=notes, category_id=category_id)

    db.session.add(password)
    db.session.commit()

    return jsonify({'message': 'Password created successfully.'}), 201


@app.route('/passwords/<int:password_id>', methods=['PUT'])
@jwt_required()
def update_password(password_id):
    password = Password.query.get(password_id)

    if not password:
        return jsonify({'message': 'Password not found.'}), 404

    data = request.get_json()
    password.name = data.get('name', password.name)
    password.email = data.get('email', password.email)
    password.password = data.get('password', password.password)
    password.notes = data.get('notes', password.notes)
    password.category_id = data.get('category_id', password.category_id)

    db.session.commit()

    return jsonify({'message': 'Password updated successfully.'}), 200


@app.route('/passwords/<int:password_id>', methods=['DELETE'])
@jwt_required()
def delete_password(password_id):
    password = Password.query.get(password_id)

    if not password:
        return jsonify({'message': 'Password not found.'}), 404

    db.session.delete(password)
    db.session.commit()

    return jsonify({'message': 'Password deleted successfully.'}), 200



