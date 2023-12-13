import grpc
from concurrent import futures
import streaming_pb2
import streaming_pb2_grpc
import json
import logging

class MusicService(streaming_pb2_grpc.UserServiceServicer, 
                   streaming_pb2_grpc.SongServiceServicer,
                   streaming_pb2_grpc.UserPlaylistServiceServicer,
                   streaming_pb2_grpc.PlaylistSongsServiceServicer,
                   streaming_pb2_grpc.SongPlaylistServiceServicer):

    def __init__(self):
        # Carregar dados de arquivos JSON ao inicializar
        with open('../db/users.json', 'r') as file:
            self.users_data = json.load(file)

        with open('../db/songs.json', 'r') as file:
            self.songs_data = json.load(file)

        with open('../db/playlists.json', 'r') as file:
            self.playlists_data = json.load(file)

    def ListAllUsers(self, request, context):
        logging.info("Received ListAllUsers request")
        # Implementar lógica para listar todos os usuários
        users = [streaming_pb2.User(id=user["id"], name=user["name"]) for user in self.users_data]
        for user in users:
            yield user

    def ListAllSongs(self, request, context):
        logging.info("Received ListAllSongs request")
        # Implementar lógica para listar todas as músicas
        songs = [streaming_pb2.Song(id=song["id"], name=song["nome"], artist=song["artista"], 
                                    category=song["categoria"], release_date=song["data_lancamento"]) for song in self.songs_data]
        for song in songs:
            yield song

    def ListUserPlaylists(self, request, context):
        logging.info("Received ListUserPlaylists request")
        # Implementar lógica para listar playlists de um usuário
        id_usuario = request.id_usuario
        user_playlists = [playlist["nome"] for playlist in self.playlists_data if playlist["id_usuario"] == id_usuario]
        for playlist_name in user_playlists:
            yield streaming_pb2.Playlist(id_usuario=id_usuario, nome=playlist_name, songs=[])

    def ListPlaylistSongs(self, request, context):
        logging.info("Received ListPlaylistSongs request")
        # Implementar lógica para listar músicas de uma playlist
        playlist_name = request.nome
        playlist = next((playlist for playlist in self.playlists_data if playlist["nome"] == playlist_name), None)
        if playlist:
            song_ids = playlist["songs"]
            songs = [streaming_pb2.Song(id=song["id"], name=song["nome"], artist=song["artista"],
                                        category=song["categoria"], release_date=song["data_lancamento"]) for song in self.songs_data if song["id"] in song_ids]
            for song in songs:
                yield song

    def ListSongPlaylists(self, request, context):
        logging.info("Received ListSongPlaylists request")
        # Implementar lógica para listar playlists que contêm uma música
        song_name = request.song_name
        song_id = next((song["id"] for song in self.songs_data if song["nome"] == song_name), None)
        if song_id is not None:
            playlists_containing_song = [playlist["nome"] for playlist in self.playlists_data if song_id in playlist["songs"]]
            for playlist_name in playlists_containing_song:
                yield streaming_pb2.Playlist(id_usuario=0, nome=playlist_name, songs=[])

# Configurar o logger
logging.basicConfig(level=logging.INFO)

# Inicializar o servidor gRPC
def serve():
    logging.info("Iniciando serviço web com gRPC...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_UserServiceServicer_to_server(MusicService(), server)
    streaming_pb2_grpc.add_SongServiceServicer_to_server(MusicService(), server)
    streaming_pb2_grpc.add_UserPlaylistServiceServicer_to_server(MusicService(), server)
    streaming_pb2_grpc.add_PlaylistSongsServiceServicer_to_server(MusicService(), server)
    streaming_pb2_grpc.add_SongPlaylistServiceServicer_to_server(MusicService(), server)
    server.add_insecure_port('[::]:8004')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
