from neo4j.v1 import GraphDatabase, basic_auth


COUNTRY_CODES = {
    'México': 'MX',
    'USA': 'US',
    'Francia': 'FR',
    'Reino Unido': 'GB',
    'Alemania': 'DE',
    'Colombia': 'CO',
    'Argentina': 'AR',
    'Australia': 'AU',
    'Japón': 'JP',
    'Sur Korea': 'SK',
}


driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
session = driver.session()


## Manifest constants

PROMPT = 'music explorer> '
QUIT = 'quit'
QUERY_HOTTEST_GENRES = 'hottest genres'


## Main command loop
while True:
    user_input = input(PROMPT)

    if user_input.lower() == QUIT:
        break
    elif user_input.lower() == QUERY_HOTTEST_GENRES:
        print('Type the number of results you want')
        print('Afterwards type the countries you want to consider separated by spaces')
        print('Available countries are: ' + ' '.join(COUNTRY_CODES.values()))
        print('Example: 5 MX CO AR')
        query_str = ('  query>')
        query_data = query_str.split(' ')
    else:
        print('I don\'t understand that command.')

print('Goodbye.')
