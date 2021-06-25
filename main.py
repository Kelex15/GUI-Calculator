from tkinter import *
from operations import operators

BUTTON_WIDTH = 6
BUTTON_HEIGHT = 2
DISPLAY_LIST = []
SOLVE_LIST = []
with open("rad_deg.txt", "r") as f:
    RAD_DEG = int(f.read())
INV = 0

answer = ""

all_operators = ["+", "÷", "x", "-", "x^2", "x^y", "!", "e", "π", "√", "%", "ln", "log", "sin", "cos", "tan", "e^x", "10^x", "sin–1(", "cos–1(", "tan–1("]
basic_operators = ["+", "÷", "x", "-"]
x_both = ["e", "π"]
x_right = ["!", ")", "x^2", "%"]
x_left = ["√", "(", "ln", "log", "sin", "cos", "tan", "e^x", "10^x", "sin–1(", "cos–1(", "tan–1("]
no_x = ["x^y"]
with_open_bracket = ["ln", "log", "sin", "cos", "tan", "e^x", "10^x", "sin–1(", "cos–1(", "tan–1(", "x^y"]
# if the length of the answer is longer than 20 characters then it should be converted to standard form


def format_list(solving_list):
    for index, char in enumerate(solving_list):
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
        # maybe you should consider using elif for cases that are not mutually exclusive (cant occur at the same time)
        if "-" in char:
            try:
                while True:
                    if solving_list[index + 1] not in all_operators and (index == 0 or solving_list[index-1] in basic_operators):
                        solving_list[index] = solving_list[index] + solving_list[index + 1]
                        solving_list.pop(index + 1)
                    else:
                        break
            except IndexError:
                pass
        if char in x_both:
            try:
                poss = [solving_list[index-1] not in basic_operators, index != 0, solving_list[index-1] not in x_left]
                if all(poss):
                    solving_list.insert(index, "x")
                    index += 1
                    continue
            except IndexError:
                pass
            try:
                poss = [solving_list[index+1] not in basic_operators, solving_list[index+1] not in x_right]
                if all(poss):
                    solving_list.insert(index + 1, "x")
                    # index -= 1  # don't think it has any use
            except IndexError:
                pass
        if char in x_left:
            try:
                poss = [solving_list[index-1] not in basic_operators, index != 0, solving_list[index-1] not in x_left,
                        solving_list[index-1] not in no_x]
                if all(poss):
                    solving_list.insert(index, "x")
                    index += 1
                    continue
            except IndexError:
                pass
        if char in x_right:
            try:
                if solving_list[index+1] not in basic_operators and solving_list[index+1] not in x_right:
                    solving_list.insert(index+1, "x")
                    index -= 1
            except IndexError:
                pass
        if char in with_open_bracket:
            solving_list.insert(index+1, "(")


solving = SOLVE_LIST.copy()
format_list(solving)


def solve(solving_):
    global answer
    # for handling brackets once an open bracket is spotted then everything after it is in the bracket and must be treated first
    max_rank = 0
    open_bracket_index = None
    close_bracket_index = None
    after_bracket = []
    for index, char in enumerate(solving_):
        if char in all_operators:
            if operators[char]["rank"] > max_rank:
                max_rank = operators[char]["rank"]
        elif char == "(":
            open_bracket_index = index
        elif char == ")":
            close_bracket_index = index

    bracket_answer = ""
    if open_bracket_index is not None:
        if close_bracket_index is not None:
            for char in solving_[open_bracket_index+1:close_bracket_index]:
                after_bracket.append(char)
            bracket_answer = solve(after_bracket)
            if bracket_answer is None:
                try:
                    bracket_answer = after_bracket[0]
                except IndexError:
                    pass
            for _ in range(open_bracket_index+1, close_bracket_index+1):
                try:
                    solving_.pop(open_bracket_index+1)
                except IndexError:
                    pass
            solving_[open_bracket_index] = bracket_answer
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
                solving_[open_bracket_index] = bracket_answer
            solving_[open_bracket_index] = bracket_answer
    else:
        if close_bracket_index is not None:
            bracket_answer = "Error"
            solving_[close_bracket_index] = bracket_answer

    solving_label.config(text=str(bracket_answer))

    max_operation_tup = []
    for index, char in enumerate(solving_):
        if char in all_operators:
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
        print(num_before, "before", num_after, "after")

        # if the answer is not None then the operation is not a basic operation
        if answer_tup is not None:
            answer_ = answer_tup[0]
            # check the tuple returned to know if it was the num before or num after that was used for the operation
            # 1 means that the num before the sign was used while -1 means that the num after the sign was used
            if len(answer_tup) == 1:
                solving_[index] = str(answer_)
                try:
                    solving_.pop(index + 1)
                except IndexError:
                    pass
                solving_.pop(index - 1)
            else:  # in case of a bug i changed all the 0 for errors to the num used
                if answer_tup[-1] == 0:
                    solving_[index] = str(answer_)
                elif answer_tup[-1] == 1:
                    solving_[index] = str(answer_)
                    if len(solving_) > 0:
                        solving_.pop(index - 1)
                else:
                    solving_[index] = str(answer_)
                    if len(solving_) > 1:
                        solving_.pop(index + 1)

        # it has to remove the sign from
        else:
            answer_ = num_before   # here in case of answer bug
            if num_after == "" or num_after == "-":
                solving_.pop(index)

        num_of_operations = [operator for operator in solving_ if operator in all_operators]
        # if there are still any more operations repeat the solving process
        if len(num_of_operations) > 0:
            solve(solving_)
        else:
            # if it is not an error the previous answer should be displayed when it is a basic operation
            answer = answer_
            print(answer_, "answer")
            # if answer_ != "Error":
            #     answer = answer_
            solving_label.config(text=str(answer_))
            return answer_


def num_command_holder(n):
    def command_():
        global SOLVE_LIST, DISPLAY_LIST, solving
        SOLVE_LIST.append(str(n))
        DISPLAY_LIST += str(n)
        user_input.config(text="".join(DISPLAY_LIST))
        solving = SOLVE_LIST.copy()
        print(solving, "copy")
        format_list(solving)
        print(solving, "formatted")
        solve(solving)
    return command_


num_buttons_command = []
for num in range(10):
    num_buttons_command.append(num_command_holder(num))


def command(solve_sign, display_sign):
    global SOLVE_LIST, DISPLAY_LIST, solving
    DISPLAY_LIST.append(display_sign)
    SOLVE_LIST.append(solve_sign)
    solving = SOLVE_LIST.copy()
    print(solving, "copy")
    format_list(solving)
    print(solving, "formatted")
    user_input.config(text="".join(DISPLAY_LIST))
    solve(solving)


def add_command():
    if len(SOLVE_LIST) != 0:
        if SOLVE_LIST[-1] in basic_operators:
            SOLVE_LIST.pop()
            DISPLAY_LIST.pop()
        command("+", "+")


def subtract_command():
    if len(SOLVE_LIST) == 0 or SOLVE_LIST[-1] != "-":  # changed form or to and
        try:
            if SOLVE_LIST[-1] in basic_operators and SOLVE_LIST[-1] != "x" and SOLVE_LIST[-1] != "÷":
                SOLVE_LIST.pop()
                DISPLAY_LIST.pop()
        except IndexError:
            pass
        command("-", "-")


def multiply_command():
    if len(SOLVE_LIST) != 0:
        if SOLVE_LIST[-1] in basic_operators:
            SOLVE_LIST.pop()
            DISPLAY_LIST.pop()
        command("x", "x")


def divide_command():
    if len(SOLVE_LIST) != 0:
        if SOLVE_LIST[-1] in basic_operators:
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
    # format the solving list first and check if there is a decimal point in the last item of the list if there is then
    # there should not be any other decimal point
    command(".", ".")


def open_bracket_command():
    command("(", "(")


def close_bracket_command():
    command(")", ")")


def square_root_command():
    command("√", "√")


def x_square_command():
    command("x^2", "^(2)")
    print(DISPLAY_LIST)


def x_to_power_y_command():
    command("x^y", "^(")  # bug detected, would be solved after figuring out the brackets


def natural_log_command():
    command("ln", "ln(")


def log_command():
    command("log", "log(")


def sin_command():
    command("sin", "sin(")


def cos_command():
    command("cos", "cos(")


def tan_command():
    command("tan", "tan(")  # in the format function a bracket should be placed immediately after


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
    global RAD_DEG
    RAD_DEG += 1
    if RAD_DEG % 2 == 1:
        rad_or_deg_button.config(text="Rad")
    else:
        rad_or_deg_button.config(text="Deg")

    with open("rad_deg.txt", "w") as file:
        file.write(str(RAD_DEG))


def inv_command():
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
    global DISPLAY_LIST, SOLVE_LIST, answer

    DISPLAY_LIST.clear()
    SOLVE_LIST.clear()
    answer = ""
    solving_label.config(text="")
    user_input.config(text="".join(DISPLAY_LIST))


def delete_command():
    global DISPLAY_LIST, SOLVE_LIST, solving

    if len(SOLVE_LIST) > 0:
        SOLVE_LIST.pop()
        DISPLAY_LIST.pop()
        solving = SOLVE_LIST.copy()
        print(solving, "copy")
        format_list(solving)
        print(solving, "formatted")
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


for num in range(10):
    num_button_command = num_buttons_command[num]
    num_button = Button(text=f"{num}", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=num_button_command)
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
