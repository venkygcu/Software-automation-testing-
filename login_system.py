registered_username = "admin"
registered_password = "password123"

username = input("Enter username: ")
password = input("Enter password: ")

if username == registered_username and password == registered_password:
    print("Login successful")
else:
    print("Invalid username or password")
