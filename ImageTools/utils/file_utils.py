import os


def create_dir_if_not_exists(parent_dir, sub_dir=None):
    full_path = os.path.join(parent_dir, sub_dir)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return full_path


def get_directories(directory):
    return [item for item in os.listdir(directory) if os.path.isdir(os.path.join(directory, item))]


def split_path(path):
    return os.path.split(path.rstrip('/'))
