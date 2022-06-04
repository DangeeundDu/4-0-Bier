<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>nettermusic</title>
    <link rel="stylesheet" href="nettermusicstyle.css">
</head>

<body>

<div id="container">
<br>
<a href="index.html" class="startpage_button">&rarr; GO TO STARTPAGE</a>
<h1>nettermusic</h1>
<img id="logo_img" src="nettermusic.png" alt="Logo von Nettermusic"><br><br>

<?php
    // ### CONFIG #####################
    $admin_password = "NETTERMUSIC_ADMIN_PW_PLACEHOLDER"; // admin password
    // COMMAND DICT
    $admin = "admin";
    $create = "create";
    $delete = "delete";
    $list = "list";
    $play = "play";
    // ################################

    // open database
    /*
    class MyDB extends SQLite3 {
        function __construct() {
            $this->open('playlists.db');
        }
    }
    $db = new MyDB();
    if(!$db) {
        //echo $db->lastErrorMsg();
        //pg_close($db);
        exit ("ERROR: Database error</div></body></html>");
    } else {
        //echo "DEBUG: Opened database successfully<br>";
    }
    */

    // avoid that fsync() is forced in order to not generate unreasonable I/O
    // $db->exec("PRAGMA synchronous = off;");

    $conn_string = "host=nettermusic-psql port=5432 dbname=securely_validated_db user=securedatabase_user password=securepassword";
	$db = pg_connect($conn_string);

    /*
    $ret = $db->exec($sql);
    if (!$ret) {
        echo $db->lastErrorMsg();
        pg_close($db);
        exit ("ERROR: Database error</div></body></html>");
    } else {
        //echo "DEBUG: Table opened or created successfully<br>";
    }
    */

    // check whether username and password are given
    $username = "";
    $password = "";
    if (!array_key_exists('username', $_POST) || !array_key_exists('username', $_POST)
            || empty($_POST["username"]) || empty($_POST["password"])) {
                pg_close($db);
        exit("ERROR: Username or Password not provided</div></body></html>");
    } else {
        $username = $_POST['username'];
        $password = $_POST['password'];
    }
    //$owner_identifier = password_hash($username.$password, PASSWORD_DEFAULT);
    $owner_identifier = hash("sha512", $username.$password);

    // evaluate which command is requested
    $command = "";
    if (!array_key_exists('command', $_POST)) {
        $command = "admin";
    } else {
        $command = $_POST["command"];
    }
    echo "<i>".$$command." command started</i><br>";

    // parse specifier
    $specifier = "";
    if (!array_key_exists('specifier', $_POST) || empty($_POST["specifier"])) {
        $specifier = null;
    } elseif ($command === "delete" || $command === "play" ) {
        $specifier = intval($_POST["specifier"]);
        if ($specifier <= 0) {
            $specifier = null;
        }
    } elseif ($command !== "create") {
        pg_close($db);
        exit("ERROR: Specifier error</div></body></html>");
    } else {
        $specifier = $_POST["specifier"];
        // NOTE: will be validated within create process
    }

    // Secure Validator
    $is_valid = false;
    #$validation_result = exec('./secure_validator '.$command);
    $validation_result = "TRUE"; // debug only pls remove and validate again
    if ($validation_result != false) {
        if (!(strpos($validation_result, 'TRUE') !== false)) {
            pg_close($db);
            exit("ERROR: Secure Validator Error</div></body></html>");
        } else {
            $is_valid = !$is_valid;
        }
    } else {
        pg_close($db);
        exit("ERROR: Secure Validator Error</div></body></html>");
    }

    // validate command – whitelisting for more security
    if ($is_valid && $command === "create") {
        require('create.php');
    } elseif ($is_valid && $command === "delete") {
        require('delete.php');
    } elseif ($is_valid && $command === "list") {
        require("list.php");
    } elseif ($is_valid && $command === "play") {
        require("play.php");
    } elseif ($is_valid && $command === "admin"
                && $username === "admin"
                && $password === $admin_password) {
        require("list.php");
    } else {
        // Do nothing
        pg_close($db);
        exit("ERROR: Invalid Command.</div></body></html>");
    }
?>

</div>

</body>

</html>