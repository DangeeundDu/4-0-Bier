<?php
	include "header.php";
?>

Register:<p>
<form action="register.php" method="post">

Username: <input name="username" type="text" size="8">
<br/><br/>
Password: <input name="password" type="password" size="8">
<br/><br/>
Address: <input name="adresse" type="text" size="10"/>
<br/><br/>
Full Name: <input name="fullname" type="text" size="10"/>
<br/><br/>
Phone: <input name="tel" type="text" size="10"/>
<br/><br/>
<input name="go" type="submit" value="Send" />
<input name="reset" type="reset" value="Clear Input" />
</form>

<p>
<?php

$username = $_POST['username'];
$password = $_POST['password'];
$adresse = $_POST['adresse'];
$fullname = $_POST['fullname'];
$tel = $_POST['tel'];

if(isset($_POST['go']))
{
        if( $username != "" && 
            $password != "" && 
            $adresse !=  "" &&
            $fullname != "" &&
            $tel != "")
        {
			$out = array();
			exec(escapeshellcmd("/app/backend/pizzaservice.sh -c -u \"$username\" -p \"$password\" -a \"$adresse\" -n \"$fullname\" -T \"$tel\""), $out);
			if(count($out) != 0) {
				echo "<pre>";
                foreach($out as $line)
                {  
                    echo $line."\n";
                }
                echo "</pre>";
			}
			echo "<a class=\"pizza_go\" href=\"order.php\">Order</a>";
        }
        else
        {
            echo "Please fill out all fields!";
        }
}
?>

<?php
	include "footer.html";
?>
