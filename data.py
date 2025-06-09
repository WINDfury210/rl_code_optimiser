def sum_squares(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total

def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def calculate_discount(price, discount_rate):
    discounted_price = price * (1 - discount_rate)
    final_price = discounted_price + 10
    return final_price

def concat_words(words):
    result = ""
    for word in words:
        result += word + " "
    return result.strip()

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def get_positive_numbers(numbers):
    result = []
    for num in numbers:
        if num > 0:
            result.append(num)
    return result

def sum_to_n(n):
    total = 0
    for i in range(1, n+1):
        total += i
    return total

def circle_area(radius):
    return 3.14 * radius * radius

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True

def average(nums):
    total = 0
    count = 0
    for num in nums:
        total += num
        count += 1
    return total / count

def reverse_string(s):
    result = ""
    for char in s:
        result = char + result
    return result

def count_vowels(text):
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count

def merge_dicts(dict1, dict2):
    result = dict1.copy()
    for key in dict2:
        result[key] = dict2[key]
    return result

def flatten_list(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quadratic_formula(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    x1 = (-b + discriminant**0.5) / (2*a)
    x2 = (-b - discriminant**0.5) / (2*a)
    return (x1, x2)


def get_all_functions():
    import inspect
    return [inspect.getsource(func) for name, func in globals().items() 
            if inspect.isfunction(func) and not name.startswith('_')]


if __name__ == "__main__":
    samples = get_all_functions()
    print(f"{len(samples)} function samples loaded")