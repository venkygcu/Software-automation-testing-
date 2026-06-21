def divide(numerator, denominator):
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    return numerator / denominator


try:
    num1 = float(input("Enter numerator: "))
    num2 = float(input("Enter denominator: "))
    print("Result:", divide(num1, num2))
except ValueError as e:
    print("Error:", e)
