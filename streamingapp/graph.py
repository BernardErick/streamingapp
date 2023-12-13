from flask import Flask, jsonify
from flask_graphql import GraphQLView
from graphene import ObjectType, Schema, List, String, Int
import json

app = Flask(__name__)

# Ler dados dos arquivos JSON
with open('../db/users.json', 'r') as file:
    users_data = json.load(file)

with open('../db/songs.json', 'r') as file:
    songs_data = json.load(file)

with open('../db/playlists.json', 'r') as file:
    playlists_data = json.load(file)

# Definindo tipos GraphQL
class UserType(ObjectType):
    id = Int()
    name = String()
    idade = Int()
    sexo = String()
    email = String()
    cep = String()

class SongType(ObjectType):
    id = Int()
    nome = String()
    artista = String()
    categoria = String()
    data_lancamento = String()

class PlaylistType(ObjectType):
    id_usuario = Int()
    nome = String()
    songs = List(Int)

# Definindo consulta GraphQL
class Query(ObjectType):
    list_all_users = List(UserType)
    list_all_songs = List(SongType)
    list_user_playlists = List(String, id_usuario=Int())
    list_playlist_songs = List(String, nome=String())
    list_song_playlists = List(String, song_name=String())

    def resolve_list_all_users(self, info):
        return users_data

    def resolve_list_all_songs(self, info):
        return songs_data

    def resolve_list_user_playlists(self, info, id_usuario):
        return [playlist["nome"] for playlist in playlists_data if playlist["id_usuario"] == id_usuario]

    def resolve_list_playlist_songs(self, info, nome):
        playlist = next((playlist for playlist in playlists_data if playlist["nome"] == nome), None)
        return [str(song_id) for song_id in playlist["songs"]] if playlist else []

    def resolve_list_song_playlists(self, info, song_name):
        song_id = next((song["id"] for song in songs_data if song["nome"] == song_name), None)
        return [playlist["nome"] for playlist in playlists_data if song_id in playlist["songs"]] if song_id else []

# Criando esquema GraphQL
schema = Schema(query=Query)

# Adicionando a rota GraphQL à aplicação Flask
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(debug=True, port=8003)
