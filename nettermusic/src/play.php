<?php

    function create_url_array_from_input_2($input) {
        return explode("|", (string)$input);
    }

    function play($youtube_id) {
        $url = "http://youtu.be/".$youtube_id;

        echo '<iframe width="420" height="315"
                src="'.$url.'">
              </iframe>';
    }

    // before playing, list playlists – can be activated
    // require('list.php');

    echo "<br><br><br><br>"; // TODO

    $sql = "SELECT * from playlists WHERE id = '".$specifier."' AND userid = '".$owner_identifier."';";

    $tracks_string = "";
    $playlists = array();
    
    $ret = pg_query($db, $sql);
    while($row = pg_fetch_array($ret) ) {
        $tracks_string = $row['tracks'];
    }
    echo "Operation done successfully<br><br>";
    pg_close($db);

    if ($tracks_string == "") {
        echo "Playlist does not exist or is empty.";
    } else {
        $playlists = create_url_array_from_input_2($tracks_string);

        $selected_song = "";
        $selected_song = $playlists[array_rand($playlists)];

        if ($selected_song != "") {}

        play($selected_song);
    }
?>