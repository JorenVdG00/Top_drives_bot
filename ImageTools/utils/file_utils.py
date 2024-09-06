import os
import shutil


def create_dir_if_not_exists(parent_dir, sub_dir=None):
    if sub_dir:
        full_path = os.path.join(parent_dir, sub_dir)
    else:
        full_path = parent_dir
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return full_path


def get_directories(directory):
    return [item for item in os.listdir(directory) if os.path.isdir(os.path.join(directory, item))]


def get_files(directory):
    real_files = []
    files = os.listdir(directory)
    for file in files:
        if os.path.isdir(os.path.join(directory, file)):
            continue
        real_files.append(file)
    sorted_files = sorted(real_files)
    return sorted_files


def split_path(path):
    return os.path.split(path.rstrip('/'))


def remove_all_files_in_dir(dir):
    # Iterate over all the files in the directory
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        # Check if it's a file and remove it
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Removed {file_path}")
        # If it's a directory, you can optionally handle that too
        elif os.path.isdir(file_path):
            print(f"Skipping directory {file_path}")


def cleanup_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
        os.mkdir(dir)


def delete_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
        print(f'successfully deleted dir: {dir}')


def get_head(file):
    head = file.split('.')[0]
    return head
