<?php
	include "header.php";
?>

Please place your order:<p>
<form action="order.php" method="post">
Username: <input name="username" type="text" size="8">
<br/><br/>
Password: <input name="password" type="password" size="8">
<br/><br/>
<select name="pizza1">
    <option selected>--select--</option>
    <option>Margherita EUR 5</option>
    <option>Vegetariana EUR 5</option>
    <option>Salami EUR 5</option>
    <option>Cardinale EUR 5</option>
    <option>Provinciale EUR 5</option>
    <option>Al Tonno EUR 5</option>
    <option>Hawaii EUR 5</option>
    <option>Quattro Formaggio EUR 5</option>
    <option>Quattro Stagione EUR 5</option>
    <option>Con Frutti di Mare EUR 5</option>
</select>
<br/>
<select name="pizza2">
    <option selected>--select--</option>
    <option>Margherita EUR 5</option>
    <option>Vegetariana EUR 5</option>
    <option>Salami EUR 5</option>
    <option>Cardinale EUR 5</option>
    <option>Provinciale EUR 5</option>
    <option>Al Tonno EUR 5</option>
    <option>Hawaii EUR 5</option>
    <option>Quattro Formaggio EUR 5</option>
    <option>Quattro Stagione EUR 5</option>
    <option>Con Frutti di Mare EUR 5</option>
</select>
<br/>
<select name="pizza3">
    <option selected>--select--</option>
    <option>Margherita EUR 5</option>
    <option>Vegetariana EUR 5</option>
    <option>Salami EUR 5</option>
    <option>Cardinale EUR 5</option>
    <option>Provinciale EUR 5</option>
    <option>Al Tonno EUR 5</option>
    <option>Hawaii EUR 5</option>
    <option>Quattro Formaggio EUR 5</option>
    <option>Quattro Stagione EUR 5</option>
    <option>Con Frutti di Mare EUR 5</option>
</select>
<br/><br/>
Comment:<br> <textarea name="comment" id="comment" cols="20" rows="3"></textarea>
<br/><br/>
<input name="go" type="submit" value="Send" />
<input name="reset" type="reset" value="Clear Input" />
<br/><br/>
<a class="pizza_go" href="index.php">Mainsite</a>

</form>

<p>
<?php

$username = escapeshellarg($_POST['username']);
$password = escapeshellarg($_POST['password']);
$pizza1 = escapeshellarg($_POST['pizza1']);
$pizza2 = escapeshellarg($_POST['pizza2']);
$pizza3 = escapeshellarg($_POST['pizza3']);
#$comment = $_POST['comment'];
$order = "";
$anz = 0;
$out = array(); 


if(isset($_POST['go']))
{
        if( $username != escapeshellarg("") &&
            $password != escapeshellarg("") &&  
          ( $pizza1 != escapeshellarg("--select--") || 
            $pizza2 != escapeshellarg("--select--") || 
            $pizza3 != escapeshellarg("--select--")))
        {
         
            if($pizza1 != escapeshellarg("--select--")){ $order = $order."1 x $pizza1\n"; $anz += 1;}
            if($pizza2 != escapeshellarg("--select--")){ $order = $order."1 x $pizza2\n"; $anz += 1;}
            if($pizza3 != escapeshellarg("--select--")){ $order = $order."1 x $pizza3\n"; $anz += 1;}
        
	    $anz *= 5;

			$order=str_replace("\"","",$order);
            $order = $order."+++++++++++++++\nTotal EUR $anz\n+++++++++++++++\n$comment\n";
    
			$str = '/app/backend/pizzaservice.sh -o -u '.$username.' -p '.$password.' -t "'.$order.'" 2>&1';
			$ret = -1;
            exec($str, $out, $ret);

			if($ret == 0) {
				echo  "<p>Order was successful</p>";
			}

		echo "<pre>";
		foreach($out as $line)
		{
			echo $line."\n";
		}
		echo "</pre>";

	
        }
        else
        {          
            echo "Aren't you in the mood for Pizza?";
        }
}

?>

<?php
	include "footer.html";
?>
