'''Connect to jokes api and fetch the joke'''

import requests
from collections import namedtuple

INFO_URL = 'https://sv443.net/jokeapi/v2/info?format=json'
CATEGORIES_URL = 'https://sv443.net/jokeapi/v2/categories'
FLAGS_URL = 'https://sv443.net/jokeapi/v2/flags'
ENDPOINT_URL = 'https://sv443.net/jokeapi/v2/endpoints'

FORMAT_PRINT = namedtuple('FORMAT_PRINT', 'YELLOW, GREEN, RED, BOLD, UNDERLINE, END')
Color = FORMAT_PRINT(YELLOW = '\033[93m',
                     GREEN = '\033[92m',
                     RED = '\033[91m',
                     BOLD = '\033[1m',
                     UNDERLINE = '\033[4m',
                     END = '\033[0m'
                    )


def api_info():
    '''
    Display the information about the API and it's contents
    :return: Tuple of list of categories and flags
    '''
    r_info = requests.get(INFO_URL).json()
    categories = r_info['jokes']['categories']
    flags = r_info['jokes']['flags']
    number_of_jokes = r_info['jokes']['totalCount']
    types = ['single', 'twopart']
    print()
    print('Number of jokes:', number_of_jokes)
    print('Available jokes categories:', categories)
    print()

    return categories, flags, types

def joke_api():
    '''
    Connects to API and fetches the joke based on user input
    :return: Response object
    '''

    categories, flags, types = api_info()
    print(categories)
    category = input('Enter category from above list (Use comma without space for multiple) ' \
                     '(Enter for `Any`): ').title()
    if not category:
        category = 'Any'
    print()

    print(flags)
    blacklist = input('Enter flags to blacklist from above list'\
                      '(Use comma without space for multiple) (optional): ')
    if not blacklist:
        print(Color.YELLOW, Color.BOLD)
        print("Warning: Joke may be 'nsfw', 'religious'," \
              "'political', 'racist', 'sexist'", Color.END)

        blacklist = input('Hit enter to continue or input a category to blacklist: ')
    print()

    print(types)
    select_type = input('Enter at least one type from above list (skip for both): ')
    if not select_type:
        select_type = 'single,twopart'
    print()

    search = input('Search a joke that contains (optional): ')
    print()

    joke_url = 'https://sv443.net/jokeapi/v2/joke/'
    joke_url = joke_url + category
    r_obj = requests.get(joke_url, params={'blacklistFlags': blacklist,
                                           'contains': search, 'type': select_type})
    return r_obj

if __name__ == '__main__':
    print(Color.BOLD, '-------------- Jokes API --------------\n', Color.END)
    print('Documentation link: https://sv443.net/jokeapi/v2')

    try:
        R = joke_api()
        if R.json()['type'] == 'twopart' and R.status_code == 200:
            print(Color.BOLD, Color.GREEN)
            print(R.json()['setup'])
            print('.\n' * 5)
            print(R.json()['delivery'], Color.END)

        elif R.json()['type'] == 'single' and R.status_code == 200:
            print(Color.BOLD, Color.GREEN)
            print(R.json()['joke'])
            print(Color.END)

    except KeyError:
        print(Color.RED)
        print(*R.json()['causedBy'])
        print(R.json()['additionalInfo'])
        print(Color.END)

    except (ConnectionError, requests.exceptions.ConnectionError):
        print(Color.RED)
        print('Failed to establish a new connection. Please check your internet connection')
        print(Color.END)
