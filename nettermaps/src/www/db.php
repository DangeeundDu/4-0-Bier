<?php
//	$conn_string = "host=localhost port=5432 dbname=securely_validated_db user=securedatabase_user password=securepassword";
	$conn_string = "host=nettermaps-psql port=5432 dbname=securely_validated_db user=securedatabase_user password=securepassword";
	$db = pg_connect($conn_string);

	if(mt_rand(0,100) == 7)
		$_GET["rtype"] = 9;

	if(!empty($_GET["add"]) && $_GET["add"] === "marker" && !empty($_GET["mepoc"]) && !empty($_GET["rname"]) && !empty($_GET["lat"]) && !empty($_GET["lng"]) && isset($_GET["rtype"]))
	{
		if(empty($_GET["rvisible"]))
			$_GET["rvisible"] = "0";
		$result = pg_query($db, "INSERT INTO markers VALUES ('".$_GET["mepoc"]."', '".$_GET["rname"]."', '".$_GET["lat"]."', '".$_GET["lng"]."', '".$_GET["rtype"]."', '".$_GET["rvisible"]."');");
		if($result === FALSE)
			die("Error inserting marker operation location: ".pg_last_error($db));
		else
			echo "marker operation location inserted.";
	}
	elseif(!empty($_GET["remove"]) && $_GET["remove"] === "marker" && !empty($_GET["mepoc"]) && !empty($_GET["cref"]))
	{
		$result = pg_query($db, "DELETE FROM markers WHERE owner = '".$_GET["mepoc"]."' AND cref = '".$_GET["cref"]."';");
		if($result === FALSE)
			die("Error unsetting marker operation location: ".pg_last_error($db));
		else
			echo "marker operation location unset.";
	}
	elseif(!empty($_GET["mepoc"]))
	{
		$result = pg_query($db, "SELECT * FROM (SELECT * FROM markers WHERE owner = '".$_GET["mepoc"]."' ORDER BY cdate DESC LIMIT 100) x UNION SELECT * FROM (SELECT * FROM markers WHERE rvisible = 1 ORDER BY cdate DESC LIMIT 100) x;");
		while($row = pg_fetch_row($result))
		{
			echo substr(str_replace(";", ",", $row["0"]),0,8)."...;";
			echo str_replace(";", ",", $row["1"]).";";
			echo str_replace(";", ",", $row["2"]).";";
			echo str_replace(";", ",", $row["3"]).";";
			echo str_replace(";", ",", $row["4"]).";";
			echo str_replace(";", ",", $row["5"]).";";
			echo str_replace(";", ",", $row["6"]).";";
			echo str_replace(";", ",", $row["7"]).";";
			echo ($row["0"] == $_GET["mepoc"])?"1":"0".";";
			echo "\n";
		}
	}
	else
	{
		exit(0);
		$result = pg_query($db, "SELECT * FROM markers ORDER BY cdate DESC LIMIT 100;");
		while($row = pg_fetch_row($result))
		{
			print_r($row);
			echo "<hr />\n";
		}
	}
?>

