# Uses
- sys
- re


# Password Strength Calculator

Calculate password strength and return score: from 1 (very bad password) to 10 (very good password) uses rules:

- the use of both upper-case and lower-case letters (case sensitivity)
- inclusion of one or more numerical digits
- inclusion of special characters, such as @, #, $
- prohibition of words found in a password blacklist
- prohibition of words found in the user's personal information
- prohibition of use of company name or an abbreviation
- prohibition of passwords that match the format of calendar dates, license plate numbers, telephone numbers, or other common numbers

functions:

- load_file(filepath):
  load file as text
        
        
- convert_text_to_words(raw_text):
  convert text to separete words dictionary


- check_special_characters(password):
   check special characters as "$", "#", "@", "!" in password string
    
    
- check_substrings_containing(password, user_info =[]):
  check password is containing some substrings     

 
- check_digits_and_strings(password):
  check digits and char symbols containing


- check_upper_lower(password):
    check upper and lower symbols containing

- check_standard_formats(password):
  check password is in some standard formats


- get_password_strength(password, blacklist = [], 
                        user_info = [], abbreviations = [])
  main function for calculating score  

# How to use

launch: ./python password_strength.py 'some password' [blacklist file] [user personal info file] [abbreviations file]

```#!bash

python password_strength.py 'bad' blacklist.txt userpersonal.txt abbreviations.txt                                                                                 
password strength is 1 of 10


python password_strength.py 'Better' blacklist.txt userpersonal.txt abbreviations.txt                                                                              
password strength is 6 of 10


python password_strength.py 'VeryGood!1' blacklist.txt userpersonal.txt abbreviations.txt                                                                          
password strength is 10 of 10                         

```

blacklist file for exmple "blacklist.txt":

test
12345
54321
1234567890
0987654321
poiuy
qwerty
asdf
zxcvb
password
password1
Password1

user personal info file for exmple "userpersonal.txt":

name
surname
email@mail.ru

abbreviations file for exmple "abbreviations.txt":

someCompany1
SomeNane2
Test&Company25
 
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
