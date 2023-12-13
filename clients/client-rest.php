<?php

$base_url = 'http://127.0.0.1:8001'; 
function request_get($endpoint) {
    global $base_url;
    $url = "{$base_url}/{$endpoint}";
    $response = file_get_contents($url);
    return json_decode($response, true);
}

// Exemplos de chamadas
echo "Listagem de usuários: " . json_encode(request_get('users')) . PHP_EOL;
echo "Listagem de músicas: " . json_encode(request_get('songs')) . PHP_EOL;
echo "Playlists do usuário 1: " . json_encode(request_get('user_playlists/1')) . PHP_EOL;
echo "Músicas da Playlist A: " . json_encode(request_get('playlist_songs/Playlist%20A')) . PHP_EOL;
echo "Playlists que contêm a música Song A: " . json_encode(request_get('song_playlists/Song%20A')) . PHP_EOL;
