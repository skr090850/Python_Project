import os

def is_text(data):
    return isinstance(data, str)

def save_temp_file(filename, content):
    temp_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp", filename)
    with open(temp_path, 'wb') as f:
        f.write(content)
    return temp_path