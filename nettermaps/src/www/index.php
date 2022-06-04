<?php
	$nettermappoints_code = FALSE;
	if(empty($_COOKIE["nettermappoints_code"]) || !preg_match("/^[a-f0-9]{64}$/", $_COOKIE["nettermappoints_code"]))
	{
		$nettermappoints_code = hash('sha256', 'nettermappoints_code'.mt_rand(0,1000000)."__".serialize($_SERVER)."__".microtime());
		setcookie("nettermappoints_code", $nettermappoints_code);
	}
	else
		$nettermappoints_code = $_COOKIE["nettermappoints_code"];

	$api_url = str_replace("index.php", "db.php", "http://".$_SERVER["SERVER_NAME"].$_SERVER["SCRIPT_NAME"]);
?>
<!DOCTYPE html>
<html>
<head>
	<title>nettermaps</title>
	<meta charset="utf-8" />
	<link rel="stylesheet" href="./leaflet/leaflet.css" />
	<script src="./leaflet/leaflet.js"></script>
	    <style>
		body {
		    padding: 0;
		    margin: 0;
		}
		html, body, #mapid {
		    height: 100%;
		    width: 100%;
		}
		a {
			cursor: pointer;
		}
	    </style>
</head>
<body>

<noscript>We are very sorry but nettermaps requires javascript to be used properly. Please enable javascript in your browser to use this service!</noscript>
<div id="mapid"></div>
<script>
	var mymap = L.map('mapid').setView([20, 30], 13);
//	const apiurl='<?php echo $api_url; ?>';
	const apiurl=location.href.replace("index.php", "")+"/db.php";

	mepoc = document.cookie.replace("nettermappoints_code=", "");
	if(mepoc.length < 10)
		alert("Invalid nettermappoints operator code!");

	L.tileLayer('./tile.php?id={id}&z={z}&x={x}&y={y}', {
		maxZoom: 13,
		minZoom: 10,
		tileSize: 512,
		attribution: 'nettermaps | Images: &copy; Apple Emojis | <a onclick=\"open_help();\">help</a> | operator <tt><?php echo substr($nettermappoints_code,0,8)."..." ?></tt>',
		id: 'nettermaps'
	}).addTo(mymap);

	var LeafIcon = L.Icon.extend({
		options: {
			iconAnchor:   [50, 50],
			popupAnchor:  [0, 0]
		}
	});

	var iconlist = new Array();

	markertypes = 5;
	for(i = 0; i < markertypes; i++)
		iconlist[i] = new LeafIcon({iconUrl: './markers/marker'+i+'.png'});
	iconlist[9] = new LeafIcon({iconUrl: './markers/marker'+9+'.png'});

	var popup = L.popup();

	function onMapClick(e) {
		if(confirm("Please confirm you want to set a marker for this location"))
		{

			var rname = prompt("Please enter marker name", "My Location");

			if(rname != null)
			{
				if(rname.match(/^[-. A-Za-z0-9]{3,60}$/))
				{
					var rtype = Math.floor(Math.random() * markertypes);
					if(rtype == 6) rtype = Math.floor(Math.random() * markertypes);

					L.marker([e.latlng.lat, e.latlng.lng], {icon: iconlist[rtype]}).bindPopup("Location saved for marker:<br /><tt>"+rname+"</tt>").addTo(mymap);

					var visible = confirm("Should the marker be publicly visible?");

					const Http = new XMLHttpRequest();
					const url=apiurl+'?add=marker&lat='+e.latlng.lat+'&lng='+e.latlng.lng+'&rname='+rname.replace(" ","+")+'&mepoc='+mepoc+'&rtype='+rtype+'&rvisible='+(visible?"1":"0");
					Http.open("GET", url);
					Http.send();
				}
				else
					alert("Invalid marker name!");
			}

		}
	}

	var markerlist = new Array();

	mymap.on('click', onMapClick);

	const Http = new XMLHttpRequest();
	const url=apiurl+'?mepoc='+mepoc;
	Http.open("GET", url);
	Http.send();
	Http.onreadystatechange=function(){
		if(this.readyState==4 && this.status==200)
		{
			var resp = Http.responseText;
			var lines = resp.split("\n");
			var i = 0;
			for(i = 0; i < lines.length; i++)
			{
				if(lines[i].length < 2)
					continue;
				var data = lines[i].split(";");
				var owner = data[0];
				var rname = data[1];
				var lat = data[2];
				var lng = data[3];
				var rtype = data[4];
				var rvisible = data[5];
				var cdate = data[6];
				var cref = data[7];
				var own = data[8];
				var text = "Location of marker:<br /><tt>"+rname+"</tt><br />Owner:<br /><tt>"+owner+"</tt><br />";
				if(own == "1")
					text = text + "<br /><a onclick=\"unset_marker('"+cref+"')\">unset marker location</a>";
				markerlist[cref] = L.marker([lat, lng], {icon: iconlist[rtype]}).bindPopup(text).addTo(mymap);
			}
		}
	}

	function unset_marker(cref)
	{
		if(confirm("Please confirm to unset marker location!"))
		{
			mymap.removeLayer(markerlist[cref]);

			const Http = new XMLHttpRequest();
			const url=apiurl+'?remove=marker&mepoc='+mepoc+'&cref='+cref;
			Http.open("GET", url);
			Http.send();
		}
	}

	function open_help()
	{
		L.popup({maxWidth : 600})
			.setLatLng(mymap.getCenter())
			.setContent(	"<font size=\"+1\">nettermaps</font><br /><br />" +
					"<strong>nettermaps is your personal storage for your favorite locations.</strong><br /><br />" +
					"Features:<br />" +
					"Click anywhere on the map to create a marker at this position. " +
					"The dialog requires you then to enter a marker name and choose if the marker should be visible for everyone. <br />" +
					"Marker locations will be saved and displayed at any time when you open the map again. <br />" +
					"If a marker is public, the position will be displayed for others as well. <br />" + 
					"If you need to unset a marker, click the marker and use the option \"unset marker location\". " +
					"Please note that this option is not available for markers that were just saved. You need to refresh the map beforehand. <br />" +
					"<br />" +
					"<br />" +
					"Credits for used software: <a href=\"https://leafletjs.com\" title=\"A JS library for interactive maps\">Leaflet</a>"
				)
			.openOn(mymap);

	}
</script>

</body>
</html>

