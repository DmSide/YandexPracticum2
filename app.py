from flask import Flask, abort, request, jsonify
import elasticsearch as ES
import settings

from validate import validate_args

app = Flask(__name__)


@app.route('/')
def index():
    return 'worked'


@app.route('/api/movies/')
def movie_list():
    validate = validate_args(request.args)

    if not validate['success']:
        return abort(422)

    # Тут уже валидно все
    data = validate['data']

    # Уходит в тело запроса. Если запрос не пустой - мультисерч, если пустой - выдает все фильмы
    body = {
        "query": {
            "multi_match": {
                "query": data['search'],
                "fields": ["title"]
            }
        }
    } if data.get('search') else {}

    params = {
        'from': data['limit'] * (data['page'] - 1),
        'size': data['limit'],
        'sort': [{
            data["sort"]: data["sort_order"]
        }]
    }

    with ES.Elasticsearch(settings.ELASTIC_SETTINGS) as es_client:
        try:
            search_res = es_client.search(
                body=body,
                index=settings.ELASTIC_INDEX,
                params=params,
                filter_path=['hits.hits._source']
            )

            if search_res:
                return jsonify([doc['_source'] for doc in search_res['hits']['hits']])
        except ES.ConnectionError:
            print('No connection with ElasticSearch')

    return jsonify({})


@app.route('/api/movies/<string:movie_id>')
def get_movie(movie_id):
    with ES.Elasticsearch(settings.ELASTIC_SETTINGS) as es_client:
        try:
            search_result = es_client.get(index='movies', id=movie_id, ignore=404)
            if search_result['found']:
                return jsonify(search_result['_source'])
        except ES.ConnectionError:
            print('No connection with ElasticSearch')

    return abort(404)


if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT)
