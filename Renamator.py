# from os import listdir
# from os.path import isFile, join

import os
from pathlib import Path
from email.parser import Parser
from email.policy import default

def renamator(absolute_directory_path):
    files, sub_directories = split_dirs_n_files(absolute_directory_path)
    if len(files) > 0:
        for file in files:
            content = ''
            with open(file, mode='r', encoding='utf-8') as f:
                content = f.read()
            email = Parser(policy=default).parsestr(content)
            email_subject = windows_file_system_friendly_filename(email['subject'])
            if email_subject != file.name:
                old_name = file.name
                file_extension = file.suffix
                new_name = "{}{}".format(email_subject, file_extension)
                os.rename(file, Path(file.parent.absolute(), new_name))
                print("'{}' -> '{}'".format(old_name, new_name))
    if len(sub_directories) > 0:
        for directory in sub_directories:
            renamator(directory)
    print("All done for this level: '{}'".format(absolute_directory_path))
   
    

# Build directories and files list at the current directory level only
def split_dirs_n_files(root_directory):
    for root_dir, sub_dirs, current_dir_files in os.walk(root_directory):
        absolute_sub_dirs = list()
        for sub_dir in sub_dirs:
            absolute_sub_dirs.append(Path(root_dir, sub_dir))
        absolute_current_dir_files = list()
        for cfile in current_dir_files:
            absolute_current_dir_files.append(Path(root_dir, cfile))
        return (absolute_current_dir_files, absolute_sub_dirs)

def windows_file_system_friendly_filename(your_unsanitized_file_name):
    name_without_suffix = your_unsanitized_file_name.split('.')[0] # Very lazy check, be careful!
    splitted_text = list(your_unsanitized_file_name)
    sanitized_text = ''
    for character in splitted_text:
        if there_is_punctuation(character):
            continue
        else:
            sanitized_text += character
    return sanitized_text
    

def there_is_punctuation(your_string):
    import string
    return any(punctuation_character in your_string for punctuation_character in string.punctuation)

