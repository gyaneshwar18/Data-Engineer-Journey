# Day 1: Number Cruncher

def number_cruncher(numbers):
    total = sum(numbers)
    avg = total / len(numbers) if numbers else 0
    min_val = min(numbers) if numbers else None
    max_val = max(numbers) if numbers else None
    even_count = len([n for n in numbers if n % 2 == 0])
    odd_count = len([n for n in numbers if n % 2 != 0])

    return {
        "numbers": numbers,
        "sum": total,
        "average": avg,
        "min": min_val,
        "max": max_val,
        "even_count": even_count,
        "odd_count": odd_count
    }


if __name__ == "__main__":
    nums = [10, 21, 32, 43, 54, 65]  # you can change this list
    results = number_cruncher(nums)

    print("Input Numbers:", results["numbers"])
    print("Sum:", results["sum"])
    print("Average:", results["average"])
    print("Min:", results["min"])
    print("Max:", results["max"])
    print("Even Count:", results["even_count"])
    print("Odd Count:", results["odd_count"])


# def factorial(n):
#     if n == 0 or n == 1:
#         return 1
#     return n * factorial(n-1)

# print(factorial(5))  # 120


# def gcd(a, b):
#     while b:
#         a, b = b, a % b
#     return a

# print(gcd(48, 18))  # 6



# def Calculator(a,b,op):
    
#     try:
#         if op == '+':
#             return a + b
#         elif op == '-':
#             return a - b
#         elif op == '*':
#             return a * b
#         elif op == '/':
#             return a / b
#     except ZeroDivisionError:
#             return "cannot divide by zero"
    
# print(Calculator(2,5,'+'))
