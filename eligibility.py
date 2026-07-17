def check_eligibility(age):
    return 18 <= age <= 60


age = int(input("Enter your age: "))
if check_eligibility(age):
    print("Eligible")
else:
    print("Not eligible")
