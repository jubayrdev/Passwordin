import json
from src.app import app
from src.models import User, Category, Password,db
from werkzeug.security import generate_password_hash

def register(client, username, password):
    data = {
        'username': username,
        'password': password
    }
    return client.post(f'create-user', json=data)

def login(client, username, password):
    data = {
        'username': username,
        'password': password
    }
    return client.post(f'login', json=data)

def create_category(client, name, token):
    data = {
        'name': name
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return client.post(f'categories', json=data, headers=headers)

def create_password(client, name, email, password, notes, category_id, token):
    data = {
        'name': name,
        'email': email,
        'password': password,
        'notes': notes,
        'category_id': category_id
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return client.post(f'passwords', json=data, headers=headers)

def test_index():
    client = app.test_client()
    response = client.get(f'/')
    assert response.status_code == 200
    assert b'Ohkay' in response.data

def test_register_login():
    with app.app_context():
        db.drop_all()
        db.create_all()

    client = app.test_client()
    # Test user registration
    response = register(client, 'testuser', 'testpard%$3')
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == 'Successfully created user'

    # Test user login with correct credentials
    response = login(client, 'testuser', 'testpard%$3')
    assert response.status_code == 200
    assert 'access_token' in json.loads(response.data)
    assert 'refresh_token' in json.loads(response.data)

    # Test user login with incorrect credentials
    response = login(client, 'testuser', 'wrongpasswo3r&d')
    assert response.status_code == 401
    assert json.loads(response.data)['message'] == 'Invalid username or password'

    # Test user login with bad credentials
    response = login(client,'testuser','wrong')
    assert response.status_code == 400
    assert json.loads(response.data)['message'] == 'Password should be at least 6 characters long and contain at least one letter, one number, and one special character'

def test_create_category():
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(username='testuser', password=generate_password_hash('valid123#', method='sha256'))
        db.session.add(user)
        db.session.commit()

    client = app.test_client()

    # Test creating a category with a valid access token
    response = login(client,"testuser","valid123#")
    access_token = json.loads(response.data)['access_token']
    response = create_category(client, 'Test Category', access_token)
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == 'Category created successfully.'

    # Test creating a category with an invalid access token
    response = create_category(client, 'Test Category', 'invalidtoken')
    assert response.status_code == 422
    assert json.loads(response.data)['msg'] == 'Not enough segments'

def test_create_password():
    client = app.test_client()

    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(username='testuser', password=generate_password_hash('valid123#', method='sha256'))
        db.session.add(user)
        db.session.commit()

        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()


    client = app.test_client()
    response = login(client,"testuser","valid123#")
    access_token = json.loads(response.data)['access_token']

    # Test creating a password with a valid access token and valid category ID
    response = create_password(client, 'Test Password', 'test@example.com', 'testpassword', 'Test Notes', 1, access_token)
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == "Password created successfully."
    # Test creating a password with an invalid access token
    response = create_password(client, 'Test Password', 'test@example.com', 'testpassword', 'Test Notes', 1, 'invalidtoken')
    assert response.status_code == 422
    assert json.loads(response.data)['msg'] == 'Not enough segments'

    # # Test creating a password with an invalid category ID
    # response = create_password(client, 'Test Password', 'test@example.com', 'testpassword', 'Test Notes', 2, access_token)
    # assert response.status_code == 400
    # assert json.loads(response.data)['msg'] == 'Invalid category ID'
