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
    
    
def check_substrings_containing(password, user_account =[]):
    for word in user_account:
        if password in word:
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
    

def get_checks():
    return [(check_upper_lower, 2, 0), (check_digits_and_strings, 1, 0),
        (check_special_characters, 1, 0), 
        (check_substrings_containing, 1, -2, user_account),
        (check_substrings_containing, 1, -2, abbreviations),
        (check_standard_formats, 1, -2),
    ]   


def get_password_strength(password, blacklist = [], 
                        user_account = [], abbreviations = []):
    strength = 1
    if len(password) <= 3 or password in blacklist:
        return strength
    elif len(password) > 8:
        strength += 2
    elif len(password) > 6:
        strength += 1
    
    for check in get_checks():
        
        check_done = (check[0](password) if len(check) <= 3 else
            check[0](password, check[3]))
            
        if check_done:
            strength = (1 if strength <= abs(check[2]) else strength + check[2])
        else:
            strength += check[1]
    
    return strength 


if __name__ == '__main__':
    if len(sys.argv) > 1:
        blacklist = ([] if len(sys.argv) <= 2 else 
            convert_text_to_words(load_file(sys.argv[2])))
            
        user_account = ([] if len(sys.argv) <= 3 else 
            convert_text_to_words(load_file(sys.argv[3])))
            
        abbreviations = ([] if len(sys.argv) <= 4 else 
            convert_text_to_words(load_file(sys.argv[4])))
   
        password_strength = get_password_strength(sys.argv[1], blacklist,
                                                user_account, abbreviations)
        print('password strength is {0} of 10'.format(password_strength))
        sys.exit(0)
    else:
        print('please add password as argument: ' + 
            './python password_strength.py some_password')
        sys.exit(1)    
