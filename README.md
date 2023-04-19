## Passwordin

## Introduction
An open source project for password management that allows users to store their passwords securely in a centralized location. The project provides an intuitive interface for managing and organizing passwords into categories. The stored passwords are encrypted and can only be accessed by the user with the correct credentials. The project also includes features like two-factor authentication and automatic password generation to enhance the security of the user's passwords. Additionally, the project allows for easy backup and restoration of password data, and it can be easily customized and extended by developers.

## Our goal
The goals of the open source password storage project could include:

1. **Security:** The project should prioritize the security of users' passwords, using industry-standard encryption and hashing algorithms to prevent unauthorized access.

2. **User-friendly interface:** The project should aim to provide a user-friendly interface that makes it easy for users to store and retrieve their passwords.

3. **Flexibility:** The project should allow users to store passwords for different accounts and services, and to organize them in a way that makes sense for them.

4. **Accessibility:** The project should be accessible to users with different levels of technical expertise, from novice users to advanced users.

5. **Privacy:** The project should prioritize user privacy by not collecting unnecessary user data and providing users with the ability to delete their data if desired.

6. **Collaboration:** The project should encourage collaboration and contributions from the open source community, allowing developers to improve the project and add new features over time.

The goal of the project is to create an independent password management system that allows each user to store their passwords securely and easily. This system will be open source, meaning that anyone can use and modify the code to fit their specific needs. The aim is to provide a simple, user-friendly interface that can be accessed from any device and to ensure that all passwords are encrypted and kept safe. By creating an independent password system, users will have greater control over their passwords and be able to manage them in a way that is tailored to their specific needs.



### Backend

This is a Python Flask web application with a backend API to manage passwords. It has routes to create and manage users, categories and passwords. It also uses JWT tokens for authentication and authorization.

The main dependencies are Flask, Flask-JWT-Extended, Flask SQLAlchemy and Werkzeug.

There are five main routes:

1. `/create-user`: accepts a POST request to create a new user. It requires a JSON payload with a username and a password. It uses two decorator functions to validate the inputs before creating the user.

2. `/login`: accepts a POST request to authenticate a user. It requires a JSON payload with a username and a password. It uses the check_password_hash() function to verify the password, and if successful, it creates an access token and a refresh token using the create_access_token() and create_refresh_token() functions.

3. `/check`: accepts a GET request to test if the JWT token is working correctly. It uses the jwt_required() decorator to protect the route and the get_jwt_identity() function to get the current user.

4. `/refresh`: accepts a POST request to refresh the JWT access token. It requires a refresh token, and it uses the jwt_required(refresh=True) decorator to protect the route.

5. `/categories`: accepts a POST request to create a new category. It requires a JSON payload with a name field. It uses the jwt_required() decorator to protect the route.

6. `/categories/<int:category_id>`: accepts PUT and DELETE requests to update and delete categories, respectively. It uses the jwt_required() decorator to protect the routes.

7. `/passwords`: accepts a POST request to create a new password. It requires a JSON payload with a name, email, password, and an optional notes field. It also accepts an optional category_id field to associate the password with a category. It uses the jwt_required() decorator to protect the route.

8. `/passwords/<int:password_id>`: accepts PUT and DELETE requests to update and delete passwords, respectively. It uses the jwt_required() decorator to protect the routes.




