<?php
// Start/resume the session.
session_start();

// If this is a previous session, reload the PID and update the quiz attempts;
// otherwise, generate a blank page.
if (isset($_SESSION["pid"])) {
  // Load in database configuration.
  include "database_config.php";

  // Load in experiment variables.
  $pid = $_SESSION["pid"];
  $_SESSION["quiz_attempts"] = $_SESSION["quiz_attempts"] + 1;
  $quiz_attempts = $_SESSION["quiz_attempts"];

  // Retrieve this participant's quiz responses and prepare to send them to
  // the MySQL database.
  $data = "{\"id\":\"" . $pid . "\"," . "\"quiz\":\"" . $_GET["QUIZ"] . "\"}";

  // Retrieve the completion date.
  $my_date = date("Y-m-d H:i:s");

  // Establish a connection to the MySQL database.
  $con = mysqli_connect($host, $username, $password, $dbname);
  if (!$con) {
    die("Connection failed: " . mysqli_connect_error() . " Please e-mail Michael Lopez-Brau at michael.lopez-brau@yale.edu with this message.");
  }

  // Attempt to update the database.
  $query = "INSERT INTO `physical_pragmatics_observer_0` (data, completion_date) VALUES ('$data', '$my_date')";
  if (!mysqli_query($con, $query)){
    echo "Could not update database. Please e-mail Michael Lopez-Brau at michael.lopez-brau@yale.edu with the following message:<br>" . mysqli_error($con);
  }

  // Close the connection to the database.
  mysqli_close($con);
} else {
  die();
}
?>

<html>
<script>var pid = <?php echo json_encode($pid); ?>;</script>
<script>var quiz_attempts = <?php echo json_encode($quiz_attempts); ?>;</script>
<head>
  <title>Psychology Study</title>
  <link href="../shared/css/cocolab-style.css" rel="stylesheet" type="text/css"/>
</head>
<body>
  <div class="slide" style="display:grid;grid-template-rows:1fr;grid-template-columns:1fr;position:relative;align-items:center;">
    <div id="fail"></div>
    <script>
      // Set up the function to return participants to the experiment.
      function continue_experiment() {
        window.location.replace("https://compdevlab.yale.edu/studies/lopez-brau/" +
          "physical_pragmatics/experiments/observer_0.php" +
          "?PROLIFIC_PID=" + pid);
      }

      // Let participants retry the experiment if they failed once;
      // otherwise, they aren't eligible.
      var fail = document.getElementById("fail");
      if (quiz_attempts == 1) {
        fail.innerHTML = "<h3><p style=\"grid-row:1;grid-column:1;\">Sorry, you failed the quiz. " +
          "Please re-read the introduction and try again. You have one more attempt.</p></h3>" +
          "<button onclick=\"continue_experiment()\">Continue</button>";
      } else {
        fail.innerHTML = "<h3><p style=\"grid-row:1;grid-column:1;\">Sorry, you failed the quiz too many times. " +
          "You are not eligible for this study.</p></h3>";
      }
    </script>
  </div>
</body>
</html>
