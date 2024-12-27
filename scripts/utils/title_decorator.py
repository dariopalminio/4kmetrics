def print_decorated_title(title):
    width = len(title) + 10  # Adjusts the width of the frame based on the length of the title.
    print('*' * width)       # Print the top of the frame
    print('*' + ' ' * (width - 2) + '*')  # Print the sides of the frame
    print(f'*{title.center(width - 2)}*')  # Center the title within the frame
    print('*' + ' ' * (width - 2) + '*')  # Print the sides of the frame
    print('*' * width)       # Print the bottom of the frame

    