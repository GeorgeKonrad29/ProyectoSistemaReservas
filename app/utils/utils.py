from ttkbootstrap.dialogs import Messagebox


def read_archive(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file: # Try UTF-8 first
            content = file.read()
        return content
    except UnicodeDecodeError:
        # If UTF-8 fails, try another common encoding like 'latin-1'
        with open(filepath, 'r', encoding='latin-1') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return ""
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return ""
