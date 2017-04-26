# -*- encoding: utf-8 -*-
import requests
import base64
import json as jsonlib

# cuenta edgardo5gtz@gmail.com
# password PabloSpotify

API_ROOT = 'https://api.spotify.com/v1'

CLIENT_ID = '92a5fbece3794dddbc09f5250a89d228'
CLIENT_SECRET = '51fb871d646b41ffb8edc8f43c88519d'


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


headers = {
    'Authorization': 'Bearer BQCEWGDy2rD0knBuVWA-tPyS7AOX0oJySOuzyehyMrkFG3uPJuVV-aIAei5fz7mTlFn_EDls-uEg6CLOAq0-xNSi8YnrPmowrZsNuxbetOSj_0vA4IlDsH9ECgc4SiGX8N13vJ0u4TXPuxG9juhpo_nWAqZWwNog'
}


data = {}


def make_featured_query(country):
    return API_ROOT + '/browse/featured-playlists?country={}&limit={}'.format(
        COUNTRY_CODES[country], 50)


def obtain_api_token():
    r = requests.post('https://accounts.spotify.com/api/token', headers={ 'Authorization': 'Basic OTJhNWZiZWNlMzc5NGRkZGJjMDlmNTI1MGE4OWQyMjg6NTFmYjg3MWQ2NDZiNDFmZmI4ZWRjOGY0M2M4ODUxOWQ=' }, data={ 'grant_type': 'client_credentials'} )
    token = r.json()['access_token']
    headers['Authorization'] = 'Bearer ' + token
   



obtain_api_token()

requests_made = 0

for country_name in COUNTRY_CODES.keys():
    print('Working on ' + country_name)
    r = requests.get(make_featured_query(country_name), headers=headers)
    json = r.json()
    playlist_tracks = [ plist['tracks']['href'] for plist in json['playlists']['items'] ]

    for item in playlist_tracks:
        r = requests.get(item, headers=headers)
        json = r.json()
        artists_urls = []

        for playlist_track_data in json['items']:
            try:
                for artist in playlist_track_data['track']['artists']:
                    artists_urls.append(artist['href'])
            except:
                pass

        for url in artists_urls:
            r = requests.get(url, headers=headers)
            json = r.json()
            genres = json['genres']
            artist_name = json['name']

            country_data = data.get(country_name, None)

            if not country_data:
                data[country_name] = {}
                country_data = data[country_name]

            for gen in genres:
                genre_count = country_data.get(gen, None)
                if not genre_count:
                    country_data[gen] = 1
                else:
                    country_data[gen] += 1

            requests_made += 1
            if requests_made % 250 == 0:
                print('250 more')
                obtain_api_token()               

                with open('raw_data.txt', 'w') as file_handle:
                    file_handle.write(jsonlib.dumps(data))


