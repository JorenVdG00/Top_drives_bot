import os
def show_project_structure(path="."):
    # Define image file extensions to exclude
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.tiff', '.webp', 'pyc')

    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            # Only show files that are not images
            if not f.lower().endswith(image_extensions):
                print(f"{sub_indent}{f}")

# Replace '.' with the root of your project if needed
show_project_structure()