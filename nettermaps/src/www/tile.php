<?php

header('Content-Type: image/png');

function imagecopymerge_alpha($dst_im, $src_im, $dst_x, $dst_y, $src_x, $src_y, $src_w, $src_h, $pct) // taken from: https://www.php.net/manual/de/function.imagecopymerge.php#92787
{
	$cut = imagecreatetruecolor($src_w, $src_h);
	imagecopy($cut, $dst_im, 0, 0, $dst_x, $dst_y, $src_w, $src_h);
	imagecopy($cut, $src_im, 0, 0, $src_x, $src_y, $src_w, $src_h);
	imagecopymerge($dst_im, $cut, $dst_x, $dst_y, 0, 0, $src_w, $src_h, $pct);
}

function tile_rand($seed)
{
	$md = md5('z='.intval($_GET["z"]).' x='.intval($_GET["x"]).' y='.intval($_GET["y"]).' s='.$seed.' x='.$_SERVER["SERVER_ADDR"]);
	return hexdec(substr($md, 0, 12));
}

function tile_image($im, $filename, $x, $y)
{
	$filename = "./surface/".$filename;
	list($src_w, $src_h, $src_t, $src_a) = getimagesize($filename);
	$src_im = imagecreatefrompng($filename);
	imagecopymerge_alpha($im, $src_im, $x, $y, 0, 0, $src_w, $src_h, 100);
//	var_dump(array($src_w, $src_h, $src_t, $src_a));
	return $im;
}

$tile_size = 512;
$im = imagecreatetruecolor($tile_size, $tile_size);

$bg_color = imagecolorallocate($im, 94, 209, 104);
imagefill($im, 0, 0, $bg_color);

$text_color = imagecolorallocate($im, 0, 0, 0);
if(FALSE) imagestring($im, 2, 5, 5, 'z='.intval($_GET["z"]).' x='.intval($_GET["x"]).' y='.intval($_GET["y"]), $text_color);

for($i = 0; $i < 50; $i ++)
{
	$irand = tile_rand("speckle".$i);
	$speckle_color = imagecolorallocate($im, 49, 122, 55);

	$speckle_x = $irand % $tile_size;
	$speckle_y = $irand / 1000 % $tile_size;
	$speckle_points = array($speckle_x, $speckle_y,  $speckle_x + ($irand / 1) % 5, $speckle_y + ($irand / 100) % 5,  $speckle_x + ($irand / 10000) % 5, $speckle_y + ($irand / 10) % 5);
	imagefilledpolygon($im, $speckle_points, 3, $speckle_color);
}

if(intval($_GET["z"]) < 13)
{
	$text_color = imagecolorallocate($im, 0, 0, 0);
	imagestring($im, 3, 5, 25, 'Map details not available on this zoom level.', $text_color);
	imagestring($im, 3, 120, 25+256, 'Map details not available on this zoom level.', $text_color);
}
else
{
	$crand = tile_rand("building".$i);
	if(($crand / 10000) % 7 < 5)
	{
		tile_image($im, "building".(($crand / 10) % 6).".png", ($crand / 20000) % 160, ($crand / 200007) % 400);
		tile_image($im, "building".((($crand / 100)+1) % 6).".png", ($crand / 200000) % 160, ($crand / 2000007) % 400);
	}
	else
	{
		tile_image($im, "plant".(($crand / 10) % 3).".png", ($crand / 20000) % 360, ($crand / 200007) % 100);
		tile_image($im, "plant".((($crand / 10)+1) % 3).".png", ($crand / 200000) % 360, ($crand / 300007) % 100 + 250);
	}
}

imagepng($im);
imagedestroy($im);

?>

