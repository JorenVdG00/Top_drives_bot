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


def move_and_rename(src, dest, new_name=None):
    """
    Moves a file or directory to a specified destination and optionally renames it.

    Parameters:
    - src: The source file or directory path.
    - dest: The destination directory path where the file or directory should be moved.
    - new_name: The new name for the file or directory (optional).

    Returns:
    - final_dest: The final destination path with the new name if the operation is successful.
    - None: If the operation fails.
    """
    try:
        # If a new name is provided, modify the destination path to include it
        if new_name:
            final_dest = os.path.join(dest, new_name)
        else:
            # Use the original name if no new name is provided
            final_dest = os.path.join(dest, os.path.basename(src))

        # Ensure the destination directory exists
        create_dir_if_not_exists(dest)

        # Move the file or directory
        shutil.move(src, final_dest)
        print(f"Successfully moved {src} to {final_dest}")
        return final_dest
    except Exception as e:
        print(f"An error occurred while moving {src} to {final_dest}: {e}")
        return None