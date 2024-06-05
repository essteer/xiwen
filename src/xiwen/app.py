from config import WELCOME_MESSAGE, MENU_OPTIONS
from utils.commands import cmd_demo, cmd_url


def xiwen():
    """
    Xiwen main menu loop
    """
    print(WELCOME_MESSAGE)

    while True:
        # Main menu - get user command
        print(MENU_OPTIONS)
        command = input().upper()

        if command not in ["D", "U", "Q"]:
            continue  # Invalid command - repeat options

        elif command == "Q":  # Quit command
            break

        elif command == "D":  # Demo command
            cmd_demo()
            continue

        elif command == "U":  # URL command
            cmd_url()
            continue


# Run program
xiwen()
