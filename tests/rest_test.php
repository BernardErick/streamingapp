<?php

$base_url = 'http://127.0.0.1:8001';

function request_get($endpoint)
{
    global $base_url;
    $url = "{$base_url}/{$endpoint}";

    // Record start time
    $startTime = microtime(true);

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);

    // Record end time
    $endTime = microtime(true);

    curl_close($ch);

    // Calculate response time
    $responseTime = $endTime - $startTime;

    return array(
        'response' => json_decode($response, true),
        'response_time' => $responseTime,
    );
}

// Simulate load for 100 users
$userCount = 100;
$responses = array();

// Create multi-curl handler
$multiHandler = curl_multi_init();

for ($i = 1; $i <= $userCount; $i++) {
    $endpoints = array('users', 'songs', "user_playlists/{$i}");

    // Create individual curl handles
    $handles = array();
    foreach ($endpoints as $endpoint) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "{$base_url}/{$endpoint}");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $handles[$endpoint] = $ch;
        curl_multi_add_handle($multiHandler, $ch);
    }

    // Execute all queries simultaneously
    $active = null;
    do {
        $mrc = curl_multi_exec($multiHandler, $active);
    } while ($mrc == CURLM_CALL_MULTI_PERFORM);

    while ($active && $mrc == CURLM_OK) {
        if (curl_multi_select($multiHandler) != -1) {
            do {
                $mrc = curl_multi_exec($multiHandler, $active);
            } while ($mrc == CURLM_CALL_MULTI_PERFORM);
        }
    }

    // Retrieve responses and response times
    foreach ($handles as $endpoint => $ch) {
        $responses[$i][$endpoint] = request_get($endpoint);
        curl_multi_remove_handle($multiHandler, $ch);
    }
}

// Close the multi-curl handler
curl_multi_close($multiHandler);

// Print the responses and response times
for ($i = 1; $i <= $userCount; $i++) {
    echo "User $i:\n";
    foreach ($responses[$i] as $endpoint => $result) {
        echo "$endpoint: " . json_encode($result['response']) . "\n";
        echo "Response Time: " . $result['response_time'] . " seconds\n";
    }
    echo "------------------------\n";
}