<?php
// Load in the database configuration.
include "database_config.php";

// Retrieve the participant data.
$data = $_POST["data"];

// Retrieve the completion date.
$my_date = date("Y-m-d H:i:s");

// Establish a connection to the MySQL database.
$con = mysqli_connect($host, $username, $password, $dbname);
if (!$con) {
    die("Connection failed: " . mysqli_connect_error() . " Please e-mail Michael Lopez-Brau at michael.lopez-brau@yale.edu with this message.");
}

// Attempt to update the database.
$query = "INSERT INTO `physical_pragmatics_decider_3` (data, completion_date) VALUES ('$data', '$my_date')";
if (!mysqli_query($con, $query)){
	echo "Could not update database. Please e-mail Michael Lopez-Brau at michael.lopez-brau@yale.edu with the following message:<br>" . mysqli_error($con);
}

// Close the connection to the database.
mysqli_close($con);
?>

<html>
<head>
  <title>Psychology Study</title>
  <link href="../shared/css/cocolab-style.css" rel="stylesheet" type="text/css"/>
</head>
<body>
	<div class="slide" style="display:grid;grid-template-rows:1fr;grid-template-columns:1fr;position:relative;align-items:center;">
		<h3><p style="grid-row:1;grid-column:1;">To receive credit for completing this experiment and return back to Prolific, please click <a href="https://app.prolific.co/submissions/complete?cc=54B2323C">here</a>.</p><h3>
	</div>
</body>
</html>
