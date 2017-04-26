from flask import Flask, render_template, request
from neo4j.v1 import GraphDatabase, basic_auth


app = Flask(__name__)


## Neo4j Initialization

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
session = driver.session()



@app.route("/")
def index():
    limit = request.args.get('limit') or '10'
    country = request.args.getlist('country')
    comparison_country_source = request.args.get('comparison_country_source')

    context = {
        'limit': limit,
        'country': country,
        'hot_genre_data': [],
        'neo4j_query': None
    }

    if (limit and limit.isdigit() and len(country) > 0):
        query = ('MATCH (c:Country)-[l:LISTENS_TO]->(g:Genre) '
                'WHERE c.name =~ "' + '|'.join(country) + '" '
                'RETURN g.name, sum(l.popularity) AS total_popularity ORDER BY total_popularity DESC '
                'LIMIT ' + limit)
        context['neo4j_query'] = query

        results = session.run(query)

        for res in results:
            context['hot_genre_data'].append({
                'name': res['g.name'],
                'total_popularity': res['total_popularity']
            })

    if comparison_country_source:
        query = ('MATCH(c:Country)-[l:LISTENS_TO]->'
                 '(g:Genre)<-[l2:LISTENS_TO]-(c2:Country) '
                 'WHERE c.name = "{origin_country}" AND c2.name <> "{origin_country}" '
                 'RETURN DISTINCT c2.name, sum(l.popularity * l2.popularity) AS similarity '
                 'ORDER BY similarity DESC;').format(**{ 'origin_country': comparison_country_source })

        context['comparison_query'] = query
        context['comparison_country_source'] = comparison_country_source

        results = session.run(query)

        context['country_similarity_data'] = []

        for res in results:
            context['country_similarity_data'].append({
                'similar_country_name': res['c2.name'],
                'similarity_score': res['similarity']
            });

        print(context)

    return render_template("index.html", **context)


if __name__ == '__main__':
    app.run()
