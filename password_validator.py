def is_valid_password(password):
    return 18 <= len(password) <= 60


password = input("Enter your password: ")
if is_valid_password(password):
    print("Valid password")
else:
    print("Invalid password. Length must be between 18 and 60 characters")
