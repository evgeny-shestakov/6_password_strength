import sys
import re


def load_file(filepath):
    try:
        with open(filepath, 'r') as file_handler:              
            return file_handler.read()
    except FileNotFoundError:
        print('file {0} not found'.format(filepath))
        sys.exit(1)
        
        
def convert_text_to_words(raw_text):
    return [word for word in raw_text.split('\n') if len(word) > 0]


def check_special_characters(password):
    return bool(re.search('[$,#,@,\!]', password))
    
    
def check_substrings_containing(password, user_info =[]):
    for info in user_info:
        if password in info:
            return True
    return False    

 
def check_digits_and_strings(password):
    return (bool(re.search('\d+', password)) and
        bool(re.search('\w+', password)))


def check_upper_lower(password):
    if password.isnumeric():
        return False
    elif bool(re.search('\d+', password)):
        return True
    return not password.islower() and not password.isupper()
    

def check_standard_formats(password):
    expressions = ['^[\+]?[a-z0-9]{3}-[a-z0-9]{3}-[a-z0-9]{4}$',
                '^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$']
    for expr in expressions:
        if bool(re.search(expr, password)):
            return True    
    return False


def get_password_strength(password, blacklist = [], 
                        user_info = [], abbreviations = []):
    strength = 1
    if len(password) <= 3 or password in blacklist:
        return strength;
    elif len(password) > 8:
        strength += 2
    elif len(password) > 6:
        strength += 1    
        
    if check_upper_lower(password): 
        strength += 2
    
    if check_digits_and_strings(password):
        strength += 1
    
    if check_special_characters(password):
        strength += 1
        
    # check personal info
    if check_substrings_containing(password, user_info):
        strength = (1 if strength < 4 else strength - 3)
    else:
        strength += 1
        
    # check abbreviations
    if check_substrings_containing(password, abbreviations):
        strength = (1 if strength < 3 else strength - 2)
    else:
        strength += 1
        
    if check_standard_formats(password):
        strength = (1 if strength < 3 else strength - 2)
    else:
        strength += 1
    
    return strength 


if __name__ == '__main__':
    if len(sys.argv) > 1:
        blacklist = ([] if len(sys.argv) <= 2 else 
            convert_text_to_words(load_file(sys.argv[2])))
            
        user_info = ([] if len(sys.argv) <= 3 else 
            convert_text_to_words(load_file(sys.argv[3])))
            
        abbreviations = ([] if len(sys.argv) <= 4 else 
            convert_text_to_words(load_file(sys.argv[4])))
   
        password_strength = get_password_strength(sys.argv[1], blacklist,
                                                user_info, abbreviations)
        print('password strength is {0} of 10'.format(password_strength))
        sys.exit(0)
    else:
        print('please add password as argument: ' + 
            './python password_strength.py some_password')
        sys.exit(1)    
