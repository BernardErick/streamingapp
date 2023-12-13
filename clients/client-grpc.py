import sys
sys.path.append('../streamingapp')  # Aponte para o diretório pai do pacote streamingapp

import grpc
import streaming_pb2
import streaming_pb2_grpc
import logging

# Configurar o logger
logging.basicConfig(level=logging.INFO)

def run():
    # Conectar ao servidor gRPC
    with grpc.insecure_channel('localhost:8004') as channel:
        # Criar instância do cliente
        client = streaming_pb2_grpc.UserServiceStub(channel)

        # Enviar uma solicitação para ListAllUsers
        logging.info("Sending ListAllUsers request...")
        response_users = client.ListAllUsers(streaming_pb2.Empty())
        for user in response_users:
            logging.info(f"Received user: {user.name}")

        # Enviar uma solicitação para ListAllSongs
        client = streaming_pb2_grpc.SongServiceStub(channel)
        logging.info("Sending ListAllSongs request...")
        response_songs = client.ListAllSongs(streaming_pb2.Empty())
        for song in response_songs:
            logging.info(f"Received song: {song.name}")

        # Enviar uma solicitação para ListUserPlaylists
        client = streaming_pb2_grpc.UserPlaylistServiceStub(channel)
        logging.info("Sending ListUserPlaylists request...")
        response_playlists = client.ListUserPlaylists(streaming_pb2.UserPlaylistRequest(id_usuario=1))
        for playlist in response_playlists:
            logging.info(f"Received playlist: {playlist.nome}")

        # Enviar uma solicitação para ListPlaylistSongs
        client = streaming_pb2_grpc.PlaylistSongsServiceStub(channel)
        logging.info("Sending ListPlaylistSongs request...")
        response_playlist_songs = client.ListPlaylistSongs(streaming_pb2.PlaylistSongsRequest(nome='MinhaPlaylist'))
        for song in response_playlist_songs:
            logging.info(f"Received song in playlist: {song.name}")

        # Enviar uma solicitação para ListSongPlaylists
        client = streaming_pb2_grpc.SongPlaylistServiceStub(channel)
        logging.info("Sending ListSongPlaylists request...")
        response_song_playlists = client.ListSongPlaylists(streaming_pb2.SongPlaylistRequest(song_name='MinhaMusica'))
        for playlist in response_song_playlists:
            logging.info(f"Received playlist containing song: {playlist.nome}")

if __name__ == '__main__':
    run()
