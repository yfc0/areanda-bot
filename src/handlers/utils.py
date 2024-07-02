def check_literal_int(arg):
    try:
        int(arg)
        return True
    except ValueError:
        return False
