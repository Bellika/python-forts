import json

def load_json(filename):
    """
    Reads a JSON file and returns it as a Python dict.
    """
    with open(filename, "r") as f:
        return json.load(f)
    
def save_json(data, filename):
    """
    Saves a Python dict to a JSON file.
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
