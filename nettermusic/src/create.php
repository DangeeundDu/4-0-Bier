<?php

    // credits go to: https://stackoverflow.com/questions/6556559/youtube-api-extract-video-id/6556662#6556662
    function youtube_id_from_url($url) {
        $pattern = 
            '%^# Match any youtube URL
            (?:https?://)?  # Optional scheme. Either http or https
            (?:www\.)?      # Optional www subdomain
            (?:             # Group host alternatives
            youtu\.be/    # Either youtu.be,
            | youtube\.com  # or youtube.com
            (?:           # Group path alternatives
                /embed/     # Either /embed/
            | /v/         # or /v/
            | /watch\?v=  # or /watch\?v=
            )             # End path alternatives.
            )               # End host alternatives.
            ([\w-]{10,35})  # Allow 10-35 for youtube id.
            $%x'
            ;
        $result = preg_match($pattern, $url, $matches);
        if ($result) {
            return $matches[1];
        }
        return false;
    }

    function create_url_array_from_input($input) {
        return explode("|", (string)$input);
    }
    
    function create_playlist_from_url_array($urls) {
        $playlist = array();
        foreach ($urls as &$url) {
            array_push($playlist, youtube_id_from_url($url));
        }
        unset($url); // break reference
        return array_filter($playlist, function($element) { return $element != false; });
        // remove all invalid values
    }

    function create_tracks_string_from_playlist_array($playlist) {
        $tracks_string = "";
        foreach ($playlist as &$track) {
            if ($tracks_string === "") {
                $tracks_string = $tracks_string.$track;
            } else {
                $tracks_string = $tracks_string."|".$track;
            }
        }
        return $tracks_string;
    }

    $playlist = create_playlist_from_url_array(
        create_url_array_from_input($_POST["specifier"])
        // Validates Specifier content (as youtube regex function does it)
    );
    $tracks_string = create_tracks_string_from_playlist_array($playlist);

    // be sure that both values are validated
    $sql = "INSERT INTO playlists (userid, tracks) VALUES ('".$owner_identifier."', '".$tracks_string."')";

    $ret = pg_query($db, $sql);
    if (!$ret) {
        echo "ERR: while creating new playlist";
    } else {
        echo "Records created successfully<br>";
    }
    pg_close($db);
?>