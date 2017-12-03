<?php

function do_curl($url) {
    # initialize curl session
    $ch = curl_init();

    # set options
    if(!curl_setopt_array($ch, array(
        CURLOPT_URL => $url,
        /* CURLOPT_HTTPHEADER => $header, */
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 10,
    ))){
        throw new Exception("failed option");
    }

    # send request
    $result = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    if ($http_code >= 100 && $http_code < 300) {
        return $result;
    }elseif ($http_code == 302 || $http_code == 303){
        throw new Exception('Unhandled redirect');
    }else{
        throw new Exception("Error calling service " . $url . ". Got http status code " . $http_code . "\n" . $result);
    }
}

function get_captions($video_id) {

    $url = "https://www.youtube.com/watch?v=" . $video_id;

    $result = do_curl($url);

    $tt_url = null;
    foreach(preg_split("/((\r?\n)|(\r\n?))/", $result) as $line){
        if (strpos($line, "TTS_URL") !== false) {
            $p = strpos($line, "https");
            $buf = substr($line, $p, strlen($line) - $p - 2);
            $buf = str_replace("%2C", ",", $buf);
            $buf = str_replace("\\u0026", "&", $buf);
            $buf = str_replace("\\", "", $buf);
            $tt_url = $buf;
            continue;
        }
    }

    if (is_null($tt_url)) throw new Exception("Failed to find tt_url");

    $x = parse_url($tt_url);
    $def_params = array();
    parse_str($x['query'], $def_params);

    $conf_params = array(
        "hl" => "en_US",
        "caps" => "asr",
        "sparams" => "asr_langs,caps,v,expire",
        "v" => "Hi3eeLJPKUw",
        "key" => "yttt1",
        "asr_langs" => "en,de,ja,ko,fr,ru,pt,nl,es,it",
        "kind" => "asr",
        "lang" => "en",
        "fmt" => "srv1",
        "tlang" => "sv",
    );

    foreach ($def_params as $k => $v) $conf_params[$k] = $v;

    $url = $x['scheme'] . "://" . $x['host'] . $x['path'] . "?";
    $url .= http_build_query($conf_params);

    $test = do_curl($url);

    return $test;
}

/* $vid = "he8Gl03cZHg"; */
$vid = $argv[1];
$test = get_captions($vid);

$xml = new SimpleXMLElement($test);
$data = array();
foreach ($xml->text as $elem) {
    $text = (string)$elem;
    $attr = $elem->attributes();
    $data[] = array(
        'html' => $text,
        'text' => preg_replace('/<.+>/U', '', $text),
        'start' => (string)$attr['start'],
        'duration' => (string)$attr['dur'],
    );
}

file_put_contents("media/tmp/" . $vid . ".json", json_encode($data));