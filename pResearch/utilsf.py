import os


def create_directory(directory):
    """create a new directory if doesn't exists"""
    if not os.path.exists(directory):
        print('New folder created: ' + directory)
        os.makedirs(directory)


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def append_to_file(path, data):
    with open(path, 'a') as f:
        f.write(data + '\n')


def delete_file_content(path):
    with open(path, 'w') as f:
        pass


def find_phone_numbers():
    pass

def find_emails():
    pass


#ojo TwitterFollowBot
