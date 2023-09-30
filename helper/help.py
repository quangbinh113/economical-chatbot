import os


def get_file_extension(file_name):
    # Use os.path.splitext to split the file name into root and extension
    _, extension = os.path.splitext(file_name)
    # Remove the leading dot from the extension
    return extension.lstrip('.')


def GetRootDir() -> str:
    # Get the absolute path of the script
    script_path = os.path.abspath(__file__)

    # Get the directory containing the script (current script's directory)
    script_directory = os.path.dirname(script_path)

    # Navigate up to the root directory by using os.path.dirname repeatedly
    module_directory = os.path.dirname(script_directory)
    root_directory = os.path.normpath(os.path.join(module_directory, "../ticket_project"))

    print("Root directory:", root_directory)
    return root_directory


rootDir = GetRootDir()
