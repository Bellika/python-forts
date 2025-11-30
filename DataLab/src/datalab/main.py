from utils import log
from processing import calculate_average_age

def run():
    log('Welcome to DataLab')

    avg_age = calculate_average_age('data/data.json')
    log(f'Avg age: {avg_age:.2f}')

if __name__ == '__main__':
    run()