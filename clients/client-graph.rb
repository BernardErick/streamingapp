require 'httparty'

# URL do servidor GraphQL
url = 'http://127.0.0.1:8003/graphql'

# Consulta GraphQL para obter todos os usuários
query_all_users = <<~QUERY
  query {
    listAllUsers {
      id
      name
      idade
    }
  }
QUERY

# Consulta GraphQL para obter todas as músicas
query_all_songs = <<~QUERY
  query {
    listAllSongs {
      id
      nome
      artista
    }
  }
QUERY

# Consulta GraphQL para obter playlists do usuário com ID 1
query_user_playlists = <<~QUERY
  query {
    listUserPlaylists(idUsuario: 1)
  }
QUERY

# Consulta GraphQL para obter músicas da playlist 'Playlist A'
query_playlist_songs = <<~QUERY
  query {
    listPlaylistSongs(nome: "Playlist A")
  }
QUERY

# Consulta GraphQL para obter playlists que contêm a música 'Song A'
query_song_playlists = <<~QUERY
  query {
    listSongPlaylists(songName: "Song A")
  }
QUERY

# Enviar as consultas GraphQL para o servidor e verificar as respostas
queries = [query_all_users, query_all_songs, query_user_playlists, query_playlist_songs, query_song_playlists]

queries.each do |query|
  response = HTTParty.post(url, body: { query: query }.to_json, headers: { 'Content-Type' => 'application/json' })

  # Verificar se a solicitação foi bem-sucedida (código de status 200)
  if response.code == 200
    # Exibir a resposta JSON
    data = response.parsed_response
    puts JSON.pretty_generate(data)
  else
    puts "Erro na solicitação: #{response.code}, #{response.body}"
  end
end
