<?php
	include "header.php";
?>

Your Order History:<p>
<form action="view.php" method="post">
Username: <input name="username" type="text" size="8">
<br/><br/>
Password: <input name="password" type="password" size="8">
<br/><br/>
<input name="go" type="submit" value="Send" />
<input name="reset" type="reset" value="Clear Input" />
<br/><br/>
<a class="pizza_go" href="index.php">Mainsite</a>

</form>

<p>
<?php

$username = $_POST['username'];
$password = $_POST['password'];
$out = array();

if(isset($_POST['go']))
{
        if( $username != "" && $password != "") 
        { 
            echo exec(escapeshellcmd("/app/backend/pizzaservice.sh -v -u \"$username\" -p \"$password\" ")."2>&1", $out);
	echo"<pre>";
		foreach($out as $zeile)
		{	
			echo "$zeile\n";
		}
	echo"</pre>";
        }
        else
        {          
            echo "No User found!";
        }
}


?>

<?php
	include "footer.html";
?>
