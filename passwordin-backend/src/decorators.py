from functools import wraps
from flask import request, jsonify
import re


def validate_username(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.json
        username = data["username"]
        if not username or not username.isidentifier():
            return jsonify({'message': 'Invalid username'}), 400
        if len(username) < 4 or len(username) > 10:
            return jsonify({'message': 'Username length should be between 4 and 10 characters'}), 400
        return func(*args, **kwargs)
    return wrapper


def validate_password(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.json
        password = data["password"]
        if not password:
            return jsonify({'message': 'Password is required'}), 400
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$', password):
            return jsonify({'message': 'Password should be at least 6 characters long and contain at least one letter, one number, and one special character'}), 400
        return func(*args, **kwargs)
    return wrapper
