from tkinter import *
from operations import operators

# Constants
BUTTON_WIDTH = 6
BUTTON_HEIGHT = 2
ALL_OPERATORS = ["+", "÷", "x", "-", "x^2", "x^y", "!", "e", "π", "√", "%", "ln", "log", "sin", "cos", "tan", "e^x",
                 "10^x", "sin–1(", "cos–1(", "tan–1("]
BASIC_OPERATORS = ["+", "÷", "x", "-"]
X_BOTH = ["e", "π"]
X_RIGHT = ["!", ")", "x^2", "%"]
X_LEFT = ["√", "(", "ln", "log", "sin", "cos", "tan", "e^x", "10^x", "sin–1(", "cos–1(", "tan–1("]
NO_X = ["x^y"]
WITH_OPEN_BRACKETS = ["ln", "log", "sin", "cos", "tan", "e^x", "10^x", "sin–1(", "cos–1(", "tan–1(", "x^y"]
MAX_ANSWER_LENGTH = 10
DISPLAY_FORMAT = "{:,.10g}"

# Global Variables
DISPLAY_LIST = []
SOLVE_LIST = []
with open("rad_deg.txt", "r") as f:
    RAD_DEG = int(f.read())
INV = 0
answer = ""


def to_standard_form(num_to_convert) -> str:
    """
    Converts the number to standard form
    :param num_to_convert: int or float
    :return: str
    """
    try:
        return "{:,.5g}".format(num_to_convert)
    except OverflowError:
        return "Error Too Large"


def format_list(solving_list: list):
    """
    Formats the solving_list in place to a format executable by the solve function.
    :param solving_list: List to be formatted.
    :return: None
    """
    for index, char in enumerate(solving_list):
        # Digits should be joined together with other digits or a single decimal point
        if char.isdigit() or "." in char:
            try:
                while True:
                    poss = [solving_list[index+1].isdigit(), solving_list[index+1] == "."]
                    if any(poss):
                        solving_list[index] = solving_list[index] + solving_list[index+1]
                        solving_list.pop(index+1)
                    else:
                        break
            except IndexError:
                pass
        if "-" in char:
            try:
                while True:
                    poss = [index == 0, solving_list[index - 1] in BASIC_OPERATORS]
                    if solving_list[index + 1] not in ALL_OPERATORS and any(poss):
                        solving_list[index] = solving_list[index] + solving_list[index + 1]
                        solving_list.pop(index + 1)
                    else:
                        break
            except IndexError:
                pass
        if char in X_BOTH:
            try:
                poss = [solving_list[index-1] not in BASIC_OPERATORS, index != 0, solving_list[index - 1] not in X_LEFT]
                if all(poss):
                    solving_list.insert(index, "x")
                    index += 1
                    continue
            except IndexError:
                pass
            try:
                poss = [solving_list[index+1] not in BASIC_OPERATORS, solving_list[index + 1] not in X_RIGHT]
                if all(poss):
                    solving_list.insert(index + 1, "x")
            except IndexError:
                pass
        if char in X_LEFT:
            try:
                poss = [solving_list[index-1] not in BASIC_OPERATORS, index != 0, solving_list[index - 1] not in X_LEFT,
                        solving_list[index-1] not in NO_X]
                if all(poss):
                    solving_list.insert(index, "x")
                    index += 1
                    continue
            except IndexError:
                pass
        if char in X_RIGHT:
            try:
                if solving_list[index+1] not in BASIC_OPERATORS and solving_list[index + 1] not in X_RIGHT:
                    solving_list.insert(index+1, "x")
                    index -= 1
            except IndexError:
                pass
        if char in WITH_OPEN_BRACKETS:
            solving_list.insert(index+1, "(")


solving = SOLVE_LIST.copy()
format_list(solving)


def solve(solving_: list):
    """
    Executes the list and returns the result.
    :param solving_: a formatted list of operations to be executed.
    :return: the answer after executing the formatted list.
    """

    global answer
    # For handling brackets once an open bracket is spotted then everything after it is in the bracket and must be
    # treated first
    # Also get the highest rank
    open_bracket_index = None
    close_bracket_index = None
    after_bracket = []
    for index, char in enumerate(solving_):
        if char == "(":
            open_bracket_index = index
        elif char == ")":
            close_bracket_index = index

    bracket_answer = ""
    if open_bracket_index is not None:
        if close_bracket_index is not None:
            for char in solving_[open_bracket_index+1:close_bracket_index]:
                after_bracket.append(char)
            bracket_answer = solve(after_bracket)
            # if the bracket answer is none it is probably because there is only one item in the after bracket
            # (which is probably a number)> The bracket answer should be replaced by the item
            if bracket_answer is None:
                try:
                    bracket_answer = after_bracket[0]
                except IndexError:
                    pass
            # remove everything after the open bracket to the close bracket inclusive and replace the open bracket with
            # the bracket answer
            for _ in range(open_bracket_index+1, close_bracket_index+1):
                try:
                    solving_.pop(open_bracket_index+1)
                except IndexError:
                    pass
            solving_[open_bracket_index] = str(bracket_answer)
        else:
            for char in solving_[open_bracket_index + 1:]:
                after_bracket.append(char)
            bracket_answer = solve(after_bracket)
            if bracket_answer is None:
                if len(after_bracket) > 0:
                    bracket_answer = after_bracket[0]
            for _ in solving_[open_bracket_index + 1:]:
                solving_.pop()
            if len(after_bracket) == 0:
                bracket_answer = "Error"
                solving_[open_bracket_index] = str(bracket_answer)
            solving_[open_bracket_index] = str(bracket_answer)
    else:
        if close_bracket_index is not None:
            bracket_answer = "Error"
            solving_[close_bracket_index] = bracket_answer

    try:
        poss = [len(bracket_answer) > MAX_ANSWER_LENGTH, bracket_answer is not None]
    except TypeError:
        try:
            poss = [bracket_answer > MAX_ANSWER_LENGTH, bracket_answer is not None]
        except TypeError:
            poss = [bracket_answer is not None]
    if all(poss):
        try:
            solving_label.config(text=str(to_standard_form(int(bracket_answer))))
        except ValueError:
            solving_label.config(text=str(to_standard_form(float(bracket_answer))))
    else:
        try:
            solving_label.config(text=DISPLAY_FORMAT.format(int(bracket_answer)))
        except ValueError:
            try:
                solving_label.config(text=DISPLAY_FORMAT.format(float(bracket_answer)))
            except ValueError:
                solving_label.config(text=str(bracket_answer))

    max_rank = 0
    for index, char in enumerate(solving_):
        if char in ALL_OPERATORS:
            if operators[char]["rank"] > max_rank:
                max_rank = operators[char]["rank"]
    # Get the operation with the max rank and it's index (The list is going to contain only one item)
    max_operation_tup = []
    for index, char in enumerate(solving_):
        if char in ALL_OPERATORS:
            if operators[char]["rank"] == max_rank:
                max_operation_tup.append((index, char))
                break

    for tup in max_operation_tup:
        index, operation_sign = tup
        operation = operators[operation_sign]["operation"]
        try:
            if index == 0:
                num_before = ""
            else:
                num_before = solving_[index - 1]
        except IndexError:
            num_before = ""
        try:
            num_after = solving_[index + 1]
        except IndexError:
            num_after = ""
        answer_tup = operation(num1=num_before, num2=num_after)

        # if the answer is not None then the operation is not a basic operation
        if answer_tup is not None:
            answer_ = answer_tup[0]
            # check the tuple returned to know if it was the num before or num after that was used for the operation
            # 1 means that the num before the sign was used while -1 means that the num after the sign was used
            # 0 means that neither num before or num after was used. If the length is 1 then both num before and num
            # after were used
            if len(answer_tup) == 1:
                solving_[index] = str(answer_)
                try:
                    solving_.pop(index + 1)
                except IndexError:
                    pass
                solving_.pop(index - 1)
            else:
                if answer_tup[-1] == 0:
                    solving_[index] = str(answer_)
                elif answer_tup[-1] == 1:
                    solving_[index] = str(answer_)
                    if len(solving_) > 0:
                        try:
                            solving_.pop(index - 1)
                        except IndexError:
                            pass
                else:
                    solving_[index] = str(answer_)
                    if len(solving_) > 1:
                        solving_.pop(index + 1)

        # it has to remove the sign (it is a basic operator) from the solving list to prevent recursion
        else:
            try:
                answer_ = int(num_before)
            except ValueError:
                answer_ = float(num_before)
            if num_after == "" or num_after == "-":
                solving_.pop(index)

        num_of_operations = [operator for operator in solving_ if operator in ALL_OPERATORS]
        # if there are still any more operations repeat the solving process
        if len(num_of_operations) > 0:
            solve(solving_)
        else:
            # if it is not an error the previous answer should be displayed when it is a basic operation
            answer = answer_
            if len(str(answer_)) > MAX_ANSWER_LENGTH and answer_ != "Error":
                solving_label.config(text=str(to_standard_form(answer_)))
            else:
                try:
                    solving_label.config(text=DISPLAY_FORMAT.format(int(str(answer_))))
                except ValueError:
                    try:
                        solving_label.config(text=DISPLAY_FORMAT.format(float(str(answer_))))
                    except ValueError:
                        solving_label.config(text=str(answer_))
                # solving_label.config(text=str(answer_))
            return answer_


def num_command_holder(n: int):
    """
    Decorator that creates a command for a number button
    :param n: The number
    :return: The command function for the number
    """
    def command_():
        global SOLVE_LIST, DISPLAY_LIST, solving
        SOLVE_LIST.append(str(n))
        DISPLAY_LIST.append(str(n))
        user_input.config(text="".join(DISPLAY_LIST))
        solving = SOLVE_LIST.copy()
        format_list(solving)
        solve(solving)
    return command_


num_buttons_command = []
for num in range(10):
    num_buttons_command.append(num_command_holder(num))


def command(solve_sign: str, display_sign: str):
    """
    Performs the command of a given sign
    :param solve_sign: A str of the sign that would be in the SOLVE list
    :param display_sign: A str of the sign that would be in the Display list
    :return: None
    """
    global SOLVE_LIST, DISPLAY_LIST, solving
    DISPLAY_LIST.append(display_sign)
    SOLVE_LIST.append(solve_sign)
    solving = SOLVE_LIST.copy()
    format_list(solving)
    user_input.config(text="".join(DISPLAY_LIST))
    solve(solving)


def add_command():
    if len(SOLVE_LIST) != 0:
        if SOLVE_LIST[-1] in BASIC_OPERATORS:
            SOLVE_LIST.pop()
            DISPLAY_LIST.pop()
        command("+", "+")


def subtract_command():
    if len(SOLVE_LIST) == 0 or SOLVE_LIST[-1] != "-":
        try:
            if SOLVE_LIST[-1] in BASIC_OPERATORS and SOLVE_LIST[-1] != "x" and SOLVE_LIST[-1] != "÷":
                SOLVE_LIST.pop()
                DISPLAY_LIST.pop()
        except IndexError:
            pass
        command("-", "-")


def multiply_command():
    if len(SOLVE_LIST) != 0:
        if SOLVE_LIST[-1] in BASIC_OPERATORS:
            SOLVE_LIST.pop()
            DISPLAY_LIST.pop()
        command("x", "x")


def divide_command():
    if len(SOLVE_LIST) != 0:
        if SOLVE_LIST[-1] in BASIC_OPERATORS:
            SOLVE_LIST.pop()
            DISPLAY_LIST.pop()
        command("÷", "÷")


def factorial_command():
    command("!", "!")


def exponent_command():
    command("e", "e")


def percent_command():
    command("%", "%")


def pi_command():
    command("π", "π")


def decimal_point_command():
    try:
        check = SOLVE_LIST.copy()
        format_list(check)
        if "." not in check[-1]:
            command(".", ".")
    except IndexError:
        command(".", ".")


def open_bracket_command():
    command("(", "(")


def close_bracket_command():
    command(")", ")")


def square_root_command():
    command("√", "√")


def x_square_command():
    command("x^2", "^(2)")


def x_to_power_y_command():
    command("x^y", "^(")


def natural_log_command():
    command("ln", "ln(")


def log_command():
    command("log", "log(")


def sin_command():
    command("sin", "sin(")


def cos_command():
    command("cos", "cos(")


def tan_command():
    command("tan", "tan(")


def inv_natural_log_command():
    command("e^x", "e^(")


def inv_log_command():
    command("10^x", "10^(")


def inv_sin_command():
    command("sin–1(", "sin-1(")


def inv_cos_command():
    command("cos–1(", "cos–1(")


def inv_tan_command():
    command("tan–1(", "tan–1(")


def rad_deg_command():
    """
    Handles the radians an degree button/functionality. If the RAD_DEG value is odd the command is for radians else
     degree
    :return:
    """
    global RAD_DEG

    RAD_DEG += 1
    if RAD_DEG % 2 == 1:
        rad_or_deg_button.config(text="Rad")
    else:
        rad_or_deg_button.config(text="Deg")

    with open("rad_deg.txt", "w") as file:
        file.write(str(RAD_DEG))


def inv_command():
    """
    Handles the inverse button/functionality. If the INV value is odd the command is inverses else it stays the same
    :return: None
    """
    global INV
    INV += 1
    if INV % 2 == 1:
        natural_log_button.config(text="e^x", command=inv_natural_log_command)
        log_button.config(text="10^x", command=inv_log_command)
        sin_button.config(text="sin–1(", command=inv_sin_command)
        cos_button.config(text="cos–1(", command=inv_cos_command)
        tan_button.config(text="tan–1(", command=inv_tan_command)
    else:
        natural_log_button.config(text="ln", command=natural_log_command)
        log_button.config(text="log", command=log_command)
        sin_button.config(text="sin", command=sin_command)
        cos_button.config(text="cos", command=cos_command)
        tan_button.config(text="tan", command=tan_command)


def equals_command():
    """
    Replaces the SOLVE, DISPLAY list with the answer and clears the answer
    :return: None
    """
    global SOLVE_LIST, DISPLAY_LIST, answer
    if answer != "Error" and answer != "":
        DISPLAY_LIST.clear()
        DISPLAY_LIST.append(str(answer))
        SOLVE_LIST.clear()
        SOLVE_LIST.append(str(answer))
        solving_label.config(text="")
        user_input.config(text="".join(DISPLAY_LIST))
        answer = ""


def clear_command():
    """
    Clears the SOLVE, DISPLAY list the answer
    :return: None
    """
    global DISPLAY_LIST, SOLVE_LIST, answer

    DISPLAY_LIST.clear()
    SOLVE_LIST.clear()
    answer = ""
    solving_label.config(text="")
    user_input.config(text="".join(DISPLAY_LIST))


def delete_command():
    """
    Removes the last item from the SOLVE, DISPLAY list
    :return:
    """
    global DISPLAY_LIST, SOLVE_LIST, solving

    if len(SOLVE_LIST) > 0:
        SOLVE_LIST.pop()
        DISPLAY_LIST.pop()
        solving = SOLVE_LIST.copy()
        format_list(solving)
        user_input.config(text="".join(DISPLAY_LIST))
        solving_label.config(text="")
        solve(solving)


# ----------------GUI Setup----------------------- #
window = Tk()
window.title("Calculator")
window.config(padx=20, pady=20)

user_input = Label(height=1, width=30, bd=0, font="Helvetica 20 bold", anchor=E, text="0")
user_input.grid(row=0, column=0, columnspan=7, sticky=W + E)

solving_label = Label(height=1, width=30, bd=0, font=30, anchor=E, text="")
solving_label.grid(row=1, column=0, columnspan=7, sticky=W + E)

number_buttons = []
row_num = 5
column_num = 0


# Setup the number buttons from 0 to 9 and their commands
for num in range(10):
    num_button_command = num_buttons_command[num]
    num_button = Button(text=str(num), height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=num_button_command)
    number_buttons.append(num_button)
    if num == 0:
        num_button.grid(row=6, column=1, sticky=W + E)
    elif column_num != 0 and column_num % 3 == 0:
        row_num -= 1
        column_num = 0
        num_button.grid(row=row_num, column=column_num, sticky=W + E)
        column_num += 1
    else:
        num_button.grid(row=row_num, column=column_num, sticky=W + E)
        column_num += 1

clear_button = Button(text="Clear", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=clear_command)
clear_button.grid(row=2, column=0, sticky=W + E)

divide_button = Button(text="÷", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, comman=divide_command)
divide_button.grid(row=2, column=1, sticky=W + E)

multiply_button = Button(text="x", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=multiply_command)
multiply_button.grid(row=2, column=2, sticky=W + E)

delete_button = Button(text="Delete", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=delete_command)
delete_button.grid(row=2, column=3, sticky=W + E)

subtract_button = Button(text="-", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=subtract_command)
subtract_button.grid(row=3, column=3, sticky=W + E)

add_button = Button(text="+", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=add_command)
add_button.grid(row=4, column=3, sticky=W + E)

equals_button = Button(text="=", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=equals_command)
equals_button.grid(row=5, column=3, rowspan=2, sticky=N+S+W+E)

percent_button = Button(text="%", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=percent_command)
percent_button.grid(row=6, column=0, sticky=W + E)

point_button = Button(text=".", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=decimal_point_command)
point_button.grid(row=6, column=2, sticky=W + E)

squared_button = Button(text="x^2", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=x_square_command)
squared_button.grid(row=2, column=4, sticky=W + E)

open_bracket_button = Button(text="(", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=open_bracket_command)
open_bracket_button.grid(row=2, column=5, sticky=W + E)

close_bracket_button = Button(text=")", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=close_bracket_command)
close_bracket_button.grid(row=2, column=6, sticky=W + E)

factorial_button = Button(text="x!", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=factorial_command)
factorial_button.grid(row=3, column=4, sticky=W + E)

square_root_button = Button(text="√", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=square_root_command)
square_root_button.grid(row=3, column=5, sticky=W + E)

power_button = Button(text="x^y", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=x_to_power_y_command)
power_button.grid(row=3, column=6, sticky=W + E)

exponent_button = Button(text="e", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=exponent_command)
exponent_button.grid(row=4, column=4, sticky=W + E)

natural_log_button = Button(text="ln", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=natural_log_command)
natural_log_button.grid(row=4, column=5, sticky=W + E)

log_button = Button(text="log", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=log_command)
log_button.grid(row=4, column=6, sticky=W + E)

sin_button = Button(text="sin", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=sin_command)
sin_button.grid(row=5, column=4, sticky=W + E)

cos_button = Button(text="cos", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=cos_command)
cos_button.grid(row=5, column=5, sticky=W + E)

tan_button = Button(text="tan", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=tan_command)
tan_button.grid(row=5, column=6, sticky=W + E)

inverse_button = Button(text="inv", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=inv_command)
inverse_button.grid(row=6, column=4, sticky=W + E)

rad_or_deg_button = Button(text="Rad", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=rad_deg_command)
rad_or_deg_button.grid(row=6, column=5, sticky=W + E)

pi_button = Button(text="π", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=pi_command)
pi_button.grid(row=6, column=6, sticky=W + E)

window.mainloop()
