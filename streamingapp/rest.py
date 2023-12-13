from flask import Flask, jsonify, request
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json

app = Flask(__name__)

class MusicService:
    @app.route('/', methods=['GET'])
    def home():
        return "Api rest server! Localhost 8001..."
    @app.route('/users', methods=['GET'])
    def list_all_users():
        with open('../db/users.json', 'r') as file:
            users_data = json.load(file)

        user_names = [user["name"] for user in users_data]
        return jsonify(user_names)

    @app.route('/songs', methods=['GET'])
    def list_all_songs():
        with open('../db/songs.json', 'r') as file:
            songs_data = json.load(file)

        songs_data = [song["nome"] for song in songs_data]
        return jsonify(songs_data)

    @app.route('/user_playlists/<id_usuario>', methods=['GET'])
    def list_user_playlists(id_usuario):
        with open('../db/playlists.json', 'r') as file:
            playlists_data = json.load(file)
        
        # Filtrar playlists com base no id_usuario
        user_playlists = [playlist["nome"] for playlist in playlists_data if playlist["id_usuario"] == int(id_usuario)]

        return jsonify(user_playlists)

    @app.route('/playlist_songs/<nome>', methods=['GET'])
    def list_playlist_songs(nome):
        with open('../db/playlists.json', 'r') as file:
            playlists_data = json.load(file)
        
        # Encontrar a playlist com o nome fornecido
        playlist = next((playlist for playlist in playlists_data if playlist["nome"] == nome), None)

        if playlist:
            # Retornar a lista de músicas da playlist encontrada
            return jsonify([str(song_id) for song_id in playlist["songs"]])
        else:
            return jsonify([])

    @app.route('/song_playlists/<song_name>', methods=['GET'])
    def list_song_playlists(song_name):
        # Ler dados do arquivo songs.json
        with open('../db/songs.json', 'r') as file:
            songs_data = json.load(file)

        # Encontrar o ID da música com o nome fornecido
        song_id = next((song["id"] for song in songs_data if song["nome"] == song_name), None)

        if song_id is not None:
            # Ler dados do arquivo playlists.json
            with open('../db/playlists.json', 'r') as file:
                playlists_data = json.load(file)

            # Encontrar playlists que contenham o ID da música na lista de músicas
            playlists_containing_song = [playlist["nome"] for playlist in playlists_data if song_id in playlist["songs"]]

            return jsonify(playlists_containing_song)
        else:
            return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=8001)
