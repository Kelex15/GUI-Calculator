from operations import operators

ALL_OPERATORS = ["+", "÷", "x", "-", "x^2", "x^y", "!", "e", "π", "√", "%", "ln", "log", "sin", "cos", "tan", "e^x",
                 "10^x", "sin–1(", "cos–1(", "tan–1("]


class Stack:
    def __init__(self, max_size:int=1000):
        self.top = -1
        self.container = [None for _ in range(max_size)]
        self.MAX_SIZE = max_size

    def display(self):
        print(f"{self.container[:self.top + 1]} <- Top")

    def push(self, val):
        if self.is_full():
            raise Exception("Stack is full!")
        self.top += 1
        self.container[self.top] = val

    def pop(self):
        if self.is_empty():
            raise Exception("Can't pop from empty stack!")
        popped = self.container[self.top]
        self.top -= 1
        return popped

    def peek(self):
        if self.is_empty():
            raise Exception("Stack is empty!")
        return self.container[self.top]

    def is_full(self) -> bool:
        return self.top + 1 == self.MAX_SIZE

    def is_empty(self) -> bool:
        return self.top == -1

    def size(self) -> int:
        return self.top + 1


def parse(formatted_list: list) -> list:
    s = Stack()
    parenthesis = Stack()
    parsed_list = []
    for index, char in enumerate(formatted_list):
        if char == "(":
            s.push("(")
            parenthesis.push("(")
        elif char == ")":
            if parenthesis.is_empty():
                parsed_list.append("Error")
                return parsed_list

            while s.peek() != "(":
                parsed_list.append(s.pop())

            s.pop()
            parenthesis.pop()
        elif char in ALL_OPERATORS:
            while not s.is_empty() and s.peek() != "(" and operators[char]["rank"] <= operators[s.peek()]["rank"]:
                parsed_list.append(s.pop())
            s.push(char)
        else:
            parsed_list.append(char)

    while not s.is_empty():
        if s.peek() != "(":
            parsed_list.append(s.pop())
        else:
            s.pop()
    return parsed_list


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


if __name__ == '__main__':
    print(parse(["(", "5"]))
