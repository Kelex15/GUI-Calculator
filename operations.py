import math

with open("rad_deg.txt", "w") as f:
    f.write("1")


def read_rad_deg():
    """
    Reads the data from the rad_deg text file
    :return: int
    """
    with open("rad_deg.txt", "r") as file:
        return int(file.read())


def check_to_int(value_to_check):
    """
    Checks if a number is the form num.0 which would be converted to an int else left as it is
    :param value_to_check: int or float
    :return: int or float
    """
    try:
        if str(value_to_check)[-1] == "0" and str(value_to_check)[-2] == ".":
            return int(value_to_check)
    except IndexError:
        pass
    return value_to_check


def add(num1, num2):
    try:
        try:
            sum_ = int(num1) + int(num2)
        except ValueError:
            sum_ = float(num1) + float(num2)
        return sum_,
    except ValueError:
        if num1 == "Error" or num2 == "Error":
            return "Error",
        else:
            return


def subtract(num1, num2):
    try:
        try:
            difference = int(num1) - int(num2)
        except ValueError:
            difference = float(num1) - float(num2)
        return difference,
    except ValueError:
        if num1 == "Error" or num2 == "Error":
            return "Error",
        else:
            return


def multiply(num1, num2):
    try:
        try:
            try:
                product = int(num1) * int(num2)
            except TypeError:
                return "Error",
        except ValueError:
            try:
                product = float(num1) * float(num2)
            except TypeError:
                return "Error",
        return product,
    except ValueError:
        if num1 == "Error" or num2 == "Error":
            return "Error",
        else:
            return


def divide(num1, num2):
    try:
        try:
            quotient = int(num1) / int(num2)
        except ValueError:
            quotient = float(num1) / float(num2)
        return check_to_int(quotient),
    except ValueError:
        if num1 == "Error" or num2 == "Error":
            return "Error",
        else:
            return
    except ZeroDivisionError:
        return "Error",


def x_square(num1, num2):
    try:
        try:
            return int(num1) ** 2, 1
        except ValueError:
            return float(num1) ** 2, 1
    except ValueError:
        return "Error", 1


def x_to_power_y(num1, num2):
    try:
        try:
            return int(num1) ** int(num2),
        except ValueError:
            return float(num1) ** float(num2),
    except ValueError:
        return "Error",


def factorial(num1, num2):
    try:
        if num1.isdigit():
            fact = math.factorial(int(num1))
        else:
            return "Error", 1
        return fact, 1
    except ValueError:
        return "Error", 1


def exponent(num1, num2):
    return math.e, 0


def pi(num1, num2):
    return math.pi, 0


def percent(num1, num2):
    try:
        try:
            return int(num1)/100, 1
        except ValueError:
            return float(num1)/100, 1
    except ValueError:
        return "Error", 1


def square_root(num1, num2):
    try:
        try:
            sqrt = math.sqrt(int(num2))
        except ValueError:
            sqrt = math.sqrt(float(num2))
        return check_to_int(sqrt), -1
    except ValueError:
        return "Error", -1


def natural_log(num1, num2):
    try:
        try:
            ln = math.log(int(num2))
        except ValueError:
            ln = math.log(float(num2))
        return ln, -1
    except ValueError:
        return "Error", -1


def log(num1, num2):
    try:
        try:
            log_ = math.log10(int(num2))
        except ValueError:
            log_ = math.log10(float(num2))
        return log_, -1
    except ValueError:
        return "Error", -1


def sin(num1, num2):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                sin_ = math.sin(math.radians(int(num2)))
            else:
                sin_ = math.sin(int(num2))
        except ValueError:
            if rad_deg % 2 == 1:
                sin_ = math.sin(math.radians(float(num2)))
            else:
                sin_ = math.sin(float(num2))
        return sin_, -1
    except ValueError:
        return "Error", -1


def cos(num1, num2):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                cos_ = math.cos(math.radians(int(num2)))
            else:
                cos_ = math.cos(int(num2))
        except ValueError:
            if rad_deg % 2 == 1:
                cos_ = math.cos(math.radians(float(num2)))
            else:
                cos_ = math.cos(float(num2))
        return cos_, -1
    except ValueError:
        return "Error", -1


def tan(num1, num2):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                tan_ = math.tan(math.radians(int(num2)))
            else:
                tan_ = math.tan(int(num2))
        except ValueError:
            if rad_deg % 2 == 1:
                tan_ = math.tan(math.radians(float(num2)))
            else:
                tan_ = math.tan(float(num2))
        return tan_, -1
    except ValueError:
        return "Error", -1


def inv_natural_log(num1, num2):
    try:
        try:
            inv_natural_log_ = math.exp(int(num2))
        except ValueError:
            inv_natural_log_ = math.exp(float(num2))
        return inv_natural_log_, -1
    except ValueError:
        return "Error", -1


def inv_log(num1, num2):
    try:
        try:
            inv_log_ = 10 ** (int(num2))
        except ValueError:
            inv_log_ = 10 ** (float(num2))
        return inv_log_, -1
    except ValueError:
        return "Error", -1


def inv_sin(num1, num2):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                inv_sin_ = math.degrees(math.asin(int(num2)))
            else:
                inv_sin_ = math.asin(int(num2))
        except ValueError:
            if rad_deg % 2 == 1:
                inv_sin_ = math.degrees(math.asin(float(num2)))
            else:
                inv_sin_ = math.asin(float(num2))
        return inv_sin_, -1
    except ValueError:
        return "Error", -1


def inv_cos(num1, num2):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                inv_cos_ = math.degrees(math.acos(int(num2)))
            else:
                inv_cos_ = math.acos(int(num2))
        except ValueError:
            if rad_deg % 2 == 1:
                inv_cos_ = math.degrees(math.acos(float(num2)))
            else:
                inv_cos_ = math.acos(float(num2))
        return inv_cos_, -1
    except ValueError:
        return "Error", -1


def inv_tan(num1, num2):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                inv_tan_ = math.degrees(math.atan(int(num2)))
            else:
                inv_tan_ = math.atan(int(num2))
        except ValueError:
            if rad_deg % 2 == 1:
                inv_tan_ = math.degrees(math.atan(float(num2)))
            else:
                inv_tan_ = math.atan(float(num2))
        return inv_tan_, -1
    except ValueError:
        return "Error", -1


# Dictionary of all the signs and their various operations and ranks
operators = {
    "+": {"operation": add, "rank": 1},
    "-": {"operation": subtract, "rank": 1},
    "x": {"operation": multiply, "rank": 2},
    "÷": {"operation": divide, "rank": 2},
    "e": {"operation": exponent, "rank": 3.5},
    "π": {"operation": pi, "rank": 3.5},
    "√": {"operation": square_root, "rank": 3},
    "%": {"operation": percent, "rank": 3},
    "!": {"operation": factorial, "rank": 3},
    "x^2": {"operation": x_square, "rank": 3},
    "x^y": {"operation": x_to_power_y, "rank": 3},
    "ln": {"operation": natural_log, "rank": 3},
    "log": {"operation": log, "rank": 3},
    "sin": {"operation": sin, "rank": 3},
    "cos": {"operation": cos, "rank": 3},
    "tan": {"operation": tan, "rank": 3},
    "e^x": {"operation": inv_natural_log, "rank": 3},
    "10^x": {"operation": inv_log, "rank": 3},
    "sin–1(": {"operation": inv_sin, "rank": 3},
    "cos–1(": {"operation": inv_cos, "rank": 3},
    "tan–1(": {"operation": inv_tan, "rank": 3},
}


# Kept for later analysis

# class BasicOperation:
#     def __init__(self, sign, rank):
#         self.sign = sign
#         self.rank = rank
#
#     def perform_operation(self, num_before, num_after, operation):
#         return operation(num_before, num_after)
#
#
# class OtherOperations:
#     def __init__(self, sign, rank):
#         self.sign = sign
#         self.rank = rank
