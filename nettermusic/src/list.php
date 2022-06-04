<?php
    //$verified_password = password_verify($username.$password, $owner_identifier);

    $sql = "SELECT * from playlists WHERE userid = '".$owner_identifier."' ORDER BY id ASC;";

    if ($command === "admin" && $username === "admin" && $password === $admin_password) {
        $sql = "SELECT * from playlists ORDER BY id ASC";
    }

    $ret = pg_query($db, $sql);
    while($row = pg_fetch_array($ret) ) {
        echo "<br>";
        //print_r($row);
        //echo "<br><br>";
        echo "ID = ". $row['id'] . "<br>";
        echo "TRACKS (separated by the | character) = ".$row['tracks'] ."<br><br>";
    }
    echo "Operation done successfully<br>";
    pg_close($db);
?>