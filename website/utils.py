from re import match, fullmatch

def is_username(string):
    return True if match('^[A-Za-z0-9]+$', string) else False

def is_email(string):
    return True if fullmatch('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', string) else False
