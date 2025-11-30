from module_io import load_json

def calculate_average_age(filename):
    data = load_json(filename)  
    total_age = sum(person["age"] for person in data)
    average_age = total_age / len(data)
    return average_age