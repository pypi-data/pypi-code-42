import os


def print_color(message, color):
    """
    Print a message to the screen in the given color.
    Does not log the message
        message: The message/text to display to the user
        color: The color to print in (must exist in color dict)
        end_char: character to print at the end of the message
              - default is a newline character
              - to continue printing on the same line (i.e. in a different color), pass in an empty string
    """
    # Make sure color is lowercase, and use default if None is given
    color_key = color.lower().strip() if color is not None else 'default'

    color_dict = {
        "gray": '\033[1;30m',
        "red": '\033[1;31m',
        "green": '\033[1;32m',
        "yellow": '\033[1;33m',
        "blue": '\033[1;34m',
        "magenta": '\033[1;35m',
        "cyan": '\033[1;36m',
        "white": '\033[1;37m',
        "crimson": '\033[1;38m',
        "red_h": '\033[1;41m',
        "green_h": '\033[1;42m',
        "gold_h": '\033[1;43m',
        "blue_h": '\033[1;44m',
        "magenta_h": '\033[1;45m',
        "cyan_h": '\033[1;46m',
        "gray_h": '\033[1;47m',
        "crimson_h": '\033[1;48m',
        "reset": '\033[1;m',
    }

    try:
        # Print the message to the screen
        print("{0}{1}{2}".format(color_dict[color_key], message, color_dict["reset"]))
    except KeyError:
        print(message)
        print_color(f"{color} is not a configured color.", 'gray')


def prompt(message, response_list=None, default_answer=None, make_uppercase=None):
    """Prompt the user for input"""
    # If make uppercase was not specified, determine T/F based on response_list
    if make_uppercase is None:
        # If a list of allowed responses was provided, assume they are uppercase
        make_uppercase = response_list is not None

    answer = None
    err = False

    try:
        while answer is None:
            answer = input("{0}:  ".format(message.strip(': ')))

            if make_uppercase:
                answer = answer.upper()

            if response_list is not None and type(response_list) is list:
                if answer not in response_list:
                    print_color(f"{answer} is not a valid response.", 'red')
                    print_color("Valid answers are: {0}".format(response_list), 'gray')
                    print("\n\n")
                    answer = None

    except KeyboardInterrupt:
        print_color("\n\nUser canceled request for input", 'blue')
        err = True

    if err:
        return default_answer
    else:
        return answer
