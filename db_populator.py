from neo4j.v1 import GraphDatabase, basic_auth
import requests
import base64
import json


driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
session = driver.session()

# session.run('CREATE CONSTRAINT ON (c:Country) ASSERT c.name IS UNIQUE')
# session.run('CREATE CONSTRAINT ON (g:Genre) ASSERT g.name IS UNIQUE')


data = None


with open('raw_data.txt', 'r') as file_handle:
    data = json.loads(file_handle.read())


# Create country nodes first
for country_name in data:
    session.run('CREATE (c:Country { name: {country_name} })',
                { 'country_name': country_name })

# Create the genre nodes
genres_seen = []

for country_name in data:
    for genre in data[country_name]:
        if genre not in genres_seen:
            session.run('CREATE (g:Genre { name: {genre_name} })',
                        { 'genre_name': genre })
            genres_seen.append(genre)


for country_name in data:
    for genre in data[country_name]:
        session.run('MATCH (c:Country { name: {country_name} }) MATCH (g:Genre { name: {genre_name} }) CREATE (c)-[:LISTENS_TO { popularity: {popularity} }]->(g)',
                    { 'country_name': country_name, 'genre_name': genre, 'popularity': data[country_name][genre] })
