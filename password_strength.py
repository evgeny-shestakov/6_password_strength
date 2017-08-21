import sys
import re
import os.path
import argparse
import string


def load_file(filepath):
    if not os.path.exists(filepath):
        return None    
    with open(filepath, 'r') as file_handler:              
        return file_handler.read()
       
        
def convert_text_to_words(raw_text):
    if raw_text is None:
        return []
    return [word for word in raw_text.split('\n') if word]


def check_special_characters(password):
    return set(password).intersection(string.punctuation) != set()
    
    
def check_substrings_containing(password, substrings):
    return any(word in password for word in substrings)  

 
def check_digits_and_strings(password):
    return (any(symbol.isdigit() for symbol in password) and 
        any(not symbol.isdigit() for symbol in password))


def check_upper_lower(password):
    if password.isnumeric():
        return False
    return not password.islower() and not password.isupper()
    

def check_standard_formats(password):
    formats = ['^[\+]?[a-z0-9]{3}-[a-z0-9]{3}-[a-z0-9]{4}$',
                '^[\+]?[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{3}$'
                '^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$']
    for format in formats:
        if bool(re.search(format, password)):
            return True    
    return False
    

def get_checks(user_account, abbreviations):
    return [(check_upper_lower, 2, 0, None),
        (check_digits_and_strings, 1, 0, None),
        (check_special_characters, 1, 0, None), 
        (check_substrings_containing, -2, 1, user_account),
        (check_substrings_containing, -2, 1, abbreviations),
        (check_standard_formats, -2, 1, None),
    ]   


def get_password_strength(password, blacklist, 
                        user_account, abbreviations):
    strength = 1
    if len(password) <= 3 or password in blacklist:
        return strength
    elif len(password) > 8:
        strength += 2
    elif len(password) > 6:
        strength += 1
    
    checks = get_checks(user_account, abbreviations)
    for (ckeck_function, check_ok_score, check_fail_score, 
        add_params) in checks:
        
        check_done = (ckeck_function(password) if add_params is None else
            ckeck_function(password, add_params))
        
        score = check_ok_score if check_done else check_fail_score    
        strength = 1 if strength + score < 1 else strength + score
    
    return strength
    
    
def get_argvs():
    parser = argparse.ArgumentParser(prog='Password strength')
    parser.add_argument('--password', '-p', type=str, required=True, 
                      help="please add password as --password='SomePassword'")
    parser.add_argument('--blacklist_filepath', '-b', type=str,
                      help="please add blacklist file as" +
                      "--blacklist_filepath='some_file.txt'")
    parser.add_argument('--user_account_filepath', '-u', type=str,
                      help="please add file with user account data as" +
                      "--user_account_filepath='some_file.txt'")
    parser.add_argument('--abbreviations_filepath', '-a', type=str,
                      help="please add file with abbreviations data as" +
                      "--abbreviations_filepath='some_file.txt'")                  
        
    return vars(parser.parse_args())
    
    
def load_filedata_to_words(args, file_type):
    return ([] if args[file_type] is None else 
        convert_text_to_words(load_file(args[file_type])))


if __name__ == '__main__':
    args = get_argvs()
    
    blacklist = load_filedata_to_words(args, 'blacklist_filepath')
    user_account = load_filedata_to_words(args, 'user_account_filepath')
    abbreviations = load_filedata_to_words(args, 'abbreviations_filepath')
   
    password_strength = get_password_strength(args['password'], blacklist,
                                                user_account, abbreviations)
    print('password strength is {0} of 10'.format(password_strength))
          
