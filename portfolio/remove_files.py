import os

cwd = os.getcwd()


def remove_files(dir=cwd + '/media/Files'):
    for root, dirs, files in os.walk(dir):
        print('files removing')
        for file in files:
            path = os.path.join(dir, file)
            os.remove(path)
        else:
            print('All files removed')
