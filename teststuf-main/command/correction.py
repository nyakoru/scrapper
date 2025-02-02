def correction(filename):
    forbidden_map = {
        '<': '__lt__',
        '>': '__gt__',
        ':': '__colon__',
        '"': '__quote__',
        '/': '__slash__',
        '\\': '__backslash__',
        '|': '__pipe__',
        '?': '__question__',
        '*': '__asterisk__'
    }
    sanitized = filename
    for char, placeholder in forbidden_map.items():
        sanitized = sanitized.replace(char, placeholder)
    return sanitized

def reverse_correction(corrected_filename):
    placeholder_map = {
        '__lt__': '<',
        '__gt__': '>',
        '__colon__': ':',
        '__quote__': '"',
        '__slash__': '/',
        '__backslash__': '\\',
        '__pipe__': '|',
        '__question__': '?',
        '__asterisk__': '*'
    }
    
    original = corrected_filename
    for placeholder, char in placeholder_map.items():
        original = original.replace(placeholder, char)
    return original
