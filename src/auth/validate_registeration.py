"""This module contains registration validations """
def validate_registration(username, password):
    errors = []

    if not username.strip():
        errors.append("Username cannot be empty. Please try again.")

    if not password:
        errors.append("Please provide a password.")
    elif len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    elif not any(char.isalpha() for char in password):
        errors.append("Password must contain at least one letter.")
    elif not any(char.isdigit() for char in password):
        errors.append("Password must contain at least one digit.")
    elif not any(char in "!@#$%^&*(),.?\":{}|<>" for char in password):
        errors.append("Password must contain at least one special character.")
    elif ' ' in password:
        errors.append("Password cannot contain whitespaces.")

    return errors
