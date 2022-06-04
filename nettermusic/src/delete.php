<?php 
    $sql = "DELETE from playlists where id = '".$specifier."' and userid = '".$owner_identifier."';";
    $ret = pg_query($db, $sql);
    if (!$ret) {
        echo "ERR: while deleting playlist<br>";
    } else {
        echo "Records DELETED successfully<br>";
    }
    pg_close($db);
?>