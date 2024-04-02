# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

from pathlib import Path
import Profile
from ds_client import send
from OpenWeather import OpenWeather
from LastFM import LastFM


def c_command(file_path, new_file_name):
    my_path = Path(file_path)
    file_full_name = f'{new_file_name}.dsu'
    my_file = my_path / file_full_name
    if my_path.exists():
        try:    
            my_file.touch(exist_ok=False)
            print(f'{my_file}')
        except FileExistsError:
            print('File already existed. Loading file...')
            my_list = o_command(my_file)
            return my_list  #Stop execution if file exists and return list of profile object and current file path
    else:
        print('Directory does not exist.')
        return  #Stop execution if directory does not exist

    while True:
        print('Please enter profile info ([user_name] [password] [bio]): ', end=' ')
        profile_info = input().split(' ', 2)
        if len(profile_info) >= 2:
            if (profile_info[0] == '' or profile_info[1] == '') or (profile_info[1] == ' ' or profile_info[0] == ' '):
                print('Can\'t process empty string.')
            else:
                user_name = profile_info[0]
                pwd = profile_info[1]
                bio = profile_info[2:] if len(profile_info) >= 3 else ""

                dsu_server = input('Enter the DSP server address: ').strip()

                # Create Profile object
                my_profile = Profile.Profile(dsuserver=dsu_server, username=user_name, password=pwd, bio=bio)

                # Save Profile to the DSU file
                my_profile.save_profile(my_file)
                print(f'Profile for {user_name} saved successfully.')
                break
        else:
            print('Invalid profile information provided.')
            return

    return [my_profile, my_file]  #return a list of object my_profile and current file path


def o_command(file):
    try:
        if Path(file).exists():
            my_profile = Profile.Profile()
                
            my_profile.load_profile(Path(file))
            print(f'Profile loaded successfully from {file}.')

    except Profile.DsuFileError as e:
        print(f'Failed to open DSU file.')
    except Profile.DsuProfileError as e:
        print(f'Failed to load profile from DSU file.')
    except FileExistsError:
        print('File does not exist.')

    return [my_profile, Path(file)]  #return a list of object myProfile and current file path


def keyword_feature(message):
    if '@weather' in message['entry'] or '@location' in message['entry']:
        zipcode = "92697"
        ccode = "US"
        apikey = "0b72015c070f9952c0a1c40847ec8557"

        open_weather = OpenWeather(zipcode, ccode)
        open_weather.set_apikey(apikey)
        open_weather.load_data()
        message['entry'] = open_weather.transclude(message['entry'])

    if '@lastfm' in message['entry']:
        apikey = '024c7c1f2a5d26e35a207c6d17a44f27'

        lastfm = LastFM()

        lastfm.set_apikey(apikey)
        lastfm.load_data()
        message['entry'] = lastfm.transclude(message['entry'])
    return message


def e_command(current_profile, options, file):
    try:
        i = 0
        while i < len(options):
            option = options[i]

            if option in ['-usr', '-pwd', '-bio', '-addpost']:
                # Find the index of the next command (if any)
                next_cmd_index = i + 2  #Start looking after the current option's value
                while next_cmd_index < len(options) and not options[next_cmd_index].startswith('-'):
                    next_cmd_index += 1

                # Extract the value(s) for the current command
                value = ' '.join(options[i + 1:next_cmd_index])

                if option == '-usr' and ' ' not in value:
                    if "\'" in value:
                        value = value.replace("\'", '')
                        current_profile.username = value
                    elif '"' in value:
                        value = value.replace('"', '')
                        current_profile.username = value
                elif option == '-pwd' and ' ' not in value:
                    if "\'" in value:
                        value = value.replace("\'", '')
                        current_profile.password = value
                    elif '"' in value:
                        value = value.replace('"', '')
                        current_profile.password = value
                elif option == '-bio':
                    if "\'" in value:
                        value = value.replace("\'", '')
                    elif '"' in value:
                        value = value.replace('"', '')

                    if value.isspace() is False:
                        current_profile.bio = value
                        option = input('\nDo you want to change your bio online? y/n: ')
                        if option == 'y':
                            send(current_profile.dsuserver, 3021, current_profile.username, current_profile.password, '', value)

                elif option == '-addpost':
                    print('''----------KEYWORDS----------
    @weather: real-time weather description
    @location: real-time location
    @lastfm: top artist''')
                    value = input('Enter post content: ')
                    if "\'" in value:
                        value = value.replace("\'", '')
                        new_post = Profile.Post(value)
                        current_profile.add_post(new_post)
                    elif '"' in value:
                        value = value.replace('"', '')
                        current_profile.add_post(new_post)

                    new_post = keyword_feature(new_post)
                    
                    go_online_option = input('\nDo you want to post this entry online? (y/n): ')
                    if go_online_option == 'y':
                        current_profile.save_profile(file)
                        if not new_post.get('entry').isspace():
                            send(current_profile.dsuserver, 3021, current_profile.username, current_profile.password, new_post.get('entry'), '')
                        else:
                            print('Post should not be empty!')
                else:
                    print('Invalid input, username and password must be non-empty')
                    return
                i = next_cmd_index
            elif option == '-delpost' and i + 1 < len(options):
                try:
                    post_id = int(options[i + 1])
                    if not current_profile.del_post(post_id):
                        print(f"Failed to delete post at index {post_id}.")
                except ValueError:
                    print("Invalid post ID for deletion.")
                i += 2
            else:
                print(f"Unknown or invalid option: {option}")
                break
    except UnboundLocalError as e:
        print(f'Error: {e}')

    try:
        current_profile.save_profile(file)
        print('-' * 30)
        print("Profile updated successfully.")
    except Exception as e:
        print(e)


def p_command(current_profile, options):
    try:
        for index, i in enumerate(options):
            if i == '-usr':
                print(f"Username: {current_profile.username}")
            elif i == '-pwd':
                print(f"Password: {current_profile.password}")
            elif i == '-bio':
                print(f"Bio: {current_profile.bio}")
            elif i == '-posts':
                if current_profile._posts:
                    for i, post in enumerate(current_profile.get_posts()):
                        print(f"Post {i}: {post.entry}")
                else:
                    print("No posts available.")
                return True
            elif i.startswith('-post'):
                id = options[index+1]
                try:
                    post_id = int(id)
                    post = current_profile.get_posts()[post_id]
                    print(f"Post ID {post_id}: {post.entry}")
                except (ValueError, IndexError):
                    print(f"Invalid Post ID: {id}")
            elif i == '-all':
                print(f"Username: {current_profile.username}")
                print(f"Password: {current_profile.password}")
                print(f"Bio: {current_profile.bio}")
                print('------------POST----------')
                if current_profile._posts:
                    for i, post in enumerate(current_profile.get_posts()):
                        print(f"Post {i}: {post.entry}")
                    
                    return True
                else:
                    print("No posts available.")
                    return False
    except UnboundLocalError as e:
        print(f'Error: {e}')


def go_online(current_profile, options):
    try:
        print('''----------KEYWORDS----------
    @weather: real-time weather description
    @location: real-time location
    @lastfm: top artist''')
        try:
            if options == '-new':
                value = input('Enter your new entry: ')
                new_post = (keyword_feature(Profile.Post(value))['entry']).replace("\'", '')
                if not new_post.isspace() or new_post != '':
                    send(current_profile.dsuserver, 3021, current_profile.username, current_profile.password, new_post, '')
                else:
                    print('\nPost should not be empty!')
            elif options == '-curr':
                post = p_command(current_profile, ['-posts']) # print all current entry
                if post:
                    post_id = int(input('Enter the ID of the entry you want to publish: '))
                    new_post = current_profile.get_posts()[post_id]
                    if not new_post.entry.isspace() or new_post != '':
                        send(current_profile.dsuserver, 3021, current_profile.username, current_profile.password, new_post.entry, '')
                    else:
                        print('\nPost should not be empty!')
                else:
                    print("There are no entries to be published.")
                    return None
        except ValueError as e:
            print('An error occured: ',  e)
            return None
    except UnboundLocalError as e:
        print(f'Error: {e}')
