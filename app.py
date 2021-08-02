import models
import requests
from utils import hashcode
from flask import Flask, render_template, request

app = Flask(__name__)

ts, public_key, hash_md5 = hashcode()


@app.route('/', methods=['POST', 'GET'])
def characters_():
    ''' Configuring POST and GET Methods

    Notes:
        This is where the methods for the requests were configured,
        where in the method "POST" the PostgreSQL Database is accessed
        to include objects in the database and in the method "GET" the
        objects are called together with the Marvel API.
'''
    if request.method == 'POST':
        data = request.form.get('character')

        if data:
            insert = f'''INSERT INTO characters(name)
            VALUES ('{data}');
            '''
            models.insert_db(insert)

    names = '''SELECT name FROM characters;'''
    characters = models.query_db(names)

    try:
        base = 'https://gateway.marvel.com'
        req = '/v1/public/characters?name={}&orderBy=name&limit=1'
        URL = base+req+'&ts='+ts+'&apikey='+public_key+'&hash='+hash_md5

        character_data = []

        for character in characters:

            response = requests.get(URL.format(character[0])).json()

            name = response['data']['results'][0]['name']
            path = response['data']['results'][0]['thumbnail']['path']
            extension = response['data']['results'][0]['thumbnail']['extension']  # noqa: E501

            person = {
                'name': name,
                'icon': path+'.'+extension
            }

            character_data.append(person)

        return render_template(['marvel_characters.html'], character_data=character_data)  # noqa: E501

    except AttributeError:
        message = 'Character Not Found!'
        resp = {'status': 'Error', 'message': message}
        return resp
    except Exception:
        message = 'Unknown Error!'
        resp = {'status': 'Error', 'message': message}
        return resp


if __name__ == '__main__':
    app.run(debug=True)
