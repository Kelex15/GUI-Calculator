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
        return sum_
    except ValueError:
        if num1 == "Error" or num2 == "Error":
            return "Error"
        else:
            return


def subtract(num1, num2):
    try:
        try:
            difference = int(num1) - int(num2)
        except ValueError:
            difference = float(num1) - float(num2)
        return difference
    except ValueError:
        if num1 == "Error" or num2 == "Error":
            return "Error"
        else:
            return


def multiply(num1, num2):
    try:
        try:
            try:
                product = int(num1) * int(num2)
            except TypeError:
                return "Error"
        except ValueError:
            try:
                product = float(num1) * float(num2)
            except TypeError:
                return "Error"
        return product
    except ValueError:
        if num1 == "Error" or num2 == "Error":
            return "Error"
        else:
            return


def divide(num1, num2):
    try:
        try:
            quotient = int(num1) / int(num2)
        except ValueError:
            quotient = float(num1) / float(num2)
        return check_to_int(quotient)
    except ValueError:
        if num1 == "Error" or num2 == "Error":
            return "Error"
        else:
            return
    except ZeroDivisionError:
        return "Error"


def x_square(num):
    try:
        try:
            return int(num) ** 2
        except ValueError:
            return float(num) ** 2
    except ValueError:
        return "Error"


def x_to_power_y(num1, num2):
    try:
        try:
            return int(num1) ** int(num2)
        except ValueError:
            return float(num1) ** float(num2)
    except ValueError:
        return "Error"


def factorial(num):
    try:
        if num.isdigit():
            fact = math.factorial(int(num))
        else:
            return "Error"
        return fact
    except ValueError:
        return "Error"


def exponent():
    return math.e


def pi():
    return math.pi


def percent(num):
    try:
        try:
            return int(num) / 100
        except ValueError:
            return float(num) / 100
    except ValueError:
        return "Error"


def square_root(num):
    try:
        try:
            sqrt = math.sqrt(int(num))
        except ValueError:
            sqrt = math.sqrt(float(num))
        return check_to_int(sqrt)
    except ValueError:
        return "Error"


def natural_log(num):
    try:
        try:
            ln = math.log(int(num))
        except ValueError:
            ln = math.log(float(num))
        return ln
    except ValueError:
        return "Error"


def log(num):
    try:
        try:
            log_ = math.log10(int(num))
        except ValueError:
            log_ = math.log10(float(num))
        return log_
    except ValueError:
        return "Error"


def sin(num):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                sin_ = math.sin(math.radians(int(num)))
            else:
                sin_ = math.sin(int(num))
        except ValueError:
            if rad_deg % 2 == 1:
                sin_ = math.sin(math.radians(float(num)))
            else:
                sin_ = math.sin(float(num))
        return sin_
    except ValueError:
        return "Error"


def cos(num):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                cos_ = math.cos(math.radians(int(num)))
            else:
                cos_ = math.cos(int(num))
        except ValueError:
            if rad_deg % 2 == 1:
                cos_ = math.cos(math.radians(float(num)))
            else:
                cos_ = math.cos(float(num))
        return cos_
    except ValueError:
        return "Error"


def tan(num):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                tan_ = math.tan(math.radians(int(num)))
            else:
                tan_ = math.tan(int(num))
        except ValueError:
            if rad_deg % 2 == 1:
                tan_ = math.tan(math.radians(float(num)))
            else:
                tan_ = math.tan(float(num))
        return tan_
    except ValueError:
        return "Error"


def inv_natural_log(num):
    try:
        try:
            inv_natural_log_ = math.exp(int(num))
        except ValueError:
            inv_natural_log_ = math.exp(float(num))
        return inv_natural_log_
    except ValueError:
        return "Error"


def inv_log(num):
    try:
        try:
            inv_log_ = 10 ** (int(num))
        except ValueError:
            inv_log_ = 10 ** (float(num))
        return inv_log_
    except ValueError:
        return "Error"


def inv_sin(num):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                inv_sin_ = math.degrees(math.asin(int(num)))
            else:
                inv_sin_ = math.asin(int(num))
        except ValueError:
            if rad_deg % 2 == 1:
                inv_sin_ = math.degrees(math.asin(float(num)))
            else:
                inv_sin_ = math.asin(float(num))
        return inv_sin_
    except ValueError:
        return "Error"


def inv_cos(num):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                inv_cos_ = math.degrees(math.acos(int(num)))
            else:
                inv_cos_ = math.acos(int(num))
        except ValueError:
            if rad_deg % 2 == 1:
                inv_cos_ = math.degrees(math.acos(float(num)))
            else:
                inv_cos_ = math.acos(float(num))
        return inv_cos_
    except ValueError:
        return "Error"


def inv_tan(num):
    try:
        rad_deg = read_rad_deg()
        try:
            if rad_deg % 2 == 1:
                inv_tan_ = math.degrees(math.atan(int(num)))
            else:
                inv_tan_ = math.atan(int(num))
        except ValueError:
            if rad_deg % 2 == 1:
                inv_tan_ = math.degrees(math.atan(float(num)))
            else:
                inv_tan_ = math.atan(float(num))
        return inv_tan_
    except ValueError:
        return "Error"


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
