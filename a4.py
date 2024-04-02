# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

import ui

current_profile = None


def main():
    print('Welcome to my Assignment 4!')

    while True:
        mode = input('''
----------Option Menu----------
C: Create a file
O: Load a file
E: Edit a file
P: Print data in a file
G: Go online and publish your entries
admin: Enter admin mode
Q: Quit

Choose an option from menu above: ''')
        if mode.upper() == 'C':
            print('\n----------Creating Files----------')
            try:
                file_path = input('Great! Please specify the directory you would like to create your file: ')
                file_name = input('Please specify the name of the file you would like to create: ')
                profile_list = ui.c_command(file_path, file_name)
                current_profile, file_path = profile_list[0], profile_list[1]
            except TypeError as e:
                print('Profile not saved. Please try again!\n')
                print('\nAn error occured: ', e)
        elif mode.upper() == 'O':
            print('\n----------Loading Files--------------')
            file_name = input('Great! Please specify the file name you would like to load: ')
            profile_list = ui.o_command(file_name)
            current_profile, file_path = profile_list[0], profile_list[1]
        elif mode.upper() == 'E':
            try:
                if current_profile is None:
                    print("No profile is currently loaded.\n")
                else:
                    options = input('''
----------EDIT MENU OPTION----------
Username: '-usr [USERNAME]'
Password: '-pwd [PASSWORD]'
Bio:      '-bio [BIO]'
New post: '-addpost'
Delete post: '-delpost [ID]'

Choose an option: ''').split(' ')
                    ui.e_command(current_profile, options, file_path)
            except Exception as e:
                print(f'ERROR {e}. Please try again!')
        elif mode.upper() == 'P':
            if current_profile is None:
                print("No profile is currently loaded.\n")
            else:
                options = input('''
----------PRINT MENU OPTION----------
Print all username: '-usr'
Print all password: '-pwd'
Print all bio:      '-bio'
Print all posts:    '-posts'
Print post by ID:   '-post [ID]'
Print all content:  '-all'

Choose an option: ''').split(' ')
                ui.p_command(current_profile, options)
        elif mode.upper() == 'G':
            if current_profile is None:
                print("No profile is currently loaded.\n")
            else:
                options = input('''
----------ENTRY-PUBLISHING MENU OPTION----------
Publish new entry:     '-new'
Publish current entry: '-curr'

Choose an option: ''')
                ui.go_online(current_profile, options)

        elif mode.lower() == 'admin':
            print('admin mode is not supported in this assignment :)')
        elif mode.upper() == 'Q':
            exit()
        else:
            print('Invalid input! Please try again.')


if __name__ == "__main__":
    main()
