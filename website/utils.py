from re import match, fullmatch, compile, IGNORECASE

def is_username(string):
    return True if match('^[A-Za-z0-9]+$', string) else False

def is_email(string):
    return True if fullmatch('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', string) else False

def is_url(string):
    regex = compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', IGNORECASE)
    return regex.search(string)
