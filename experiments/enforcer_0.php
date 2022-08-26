<?php
// Start/resume the session.
session_start();

// If this is a previous session, reload the PID and quiz attempts;
// otherwise, set them and generate the condition assignment.
if (isset($_SESSION["pid"])) {
  $condition_assignment = $_SESSION["condition_assignment"];
  $quiz_attempts = $_SESSION["quiz_attempts"];
  if ($quiz_attempts >= 2) {
    die("Sorry, you failed the quiz too many times. You are not eligible for this study.");
  }
} else {
  $pid = htmlspecialchars($_GET["PROLIFIC_PID"]);
  $quiz_attempts = 0;
  $_SESSION["pid"] = $pid;
  $_SESSION["quiz_attempts"] = $quiz_attempts;

  // Set up the number of participants.
  $num_participants = 20;

  // Set up the path to the experiment files.
  $experiment_dir = "/var/www/html/studies/lopez-brau/physical_pragmatics/experiments/enforcer_0/";

  // Set up the path to where the assigned condition indices are stored.
  $data_dir = $experiment_dir . "data/";

  // Find the earliest condition index available.
  $files = scandir($data_dir);
  for ($i = 0; $i < $num_participants; $i++) {
    $filename = $i . ".txt";

    // If the current condition index doesn't exist in the directory, try to
    // open it.
    if (!in_array($filename, $files)) {
      # Try to open the current condition index.
      $file = fopen($data_dir . $filename, "x");

      // Write the PID to the current condition index if successful;
      // otherwise, find another index.
      if (!$file) {
        continue;
      } else {
        // Sanitize our URL input, write it, and close the file.
        fwrite($file, htmlspecialchars($_GET["PROLIFIC_PID"]));
        fclose($file);

        // Find the condition that corresponds to the current condition index.
        $condition_assignment_file = fopen($experiment_dir . "condition_assignment.csv", "r");
        for ($j = 0; $j <= $i; $j++) {
          $condition_assignment = fgets($condition_assignment_file);
        }
        fclose($condition_assignment_file);
        break;
      }
    }
  }

  // Display an error message if no condition index was available.
  if ($i == $num_participants) {
    echo "ERROR: Please contact Michael Lopez-Brau at michael.lopez-brau@yale.edu.";
  } else {
    $_SESSION["condition_index"] = $i;
    $_SESSION["condition_assignment"] = $condition_assignment;
  }
}
?>

<html>
<script type="text/javascript">var condition_assignment = <?php echo json_encode($condition_assignment); ?>;</script>
<script type="text/javascript">var quiz_attempts = <?php echo json_encode($quiz_attempts); ?>;</script>
<head>
  <title>Psychology Study</title>

  <!-- External general utilities. -->
  <script src="shared/js/jquery-1.11.1.min.js "></script>
  <script src="shared/full-projects/jquery-ui/jquery-ui.min.js"></script>
  <script src="shared/js/underscore-min.js"></script>

  <!-- CoCoLab experiment logic. -->
  <script src="shared/js/exp-V2.js"></script>
  <script src="shared/js/stream-V2.js"></script>

  <!-- CoCoLab general utilities. -->
  <script src="shared/js/mmturkey.js "></script>
  <script src="shared/js/browserCheck.js"></script>
  <script src="shared/js/utils.js"></script>

  <!-- CSS files. -->
  <link href="shared/full-projects/jquery-ui/jquery-ui.min.css" rel="stylesheet" type="text/css"/>
  <link href="shared/css/cocolab-style.css" rel="stylesheet" type="text/css"/>
  <link href="css/local-style.css" rel="stylesheet" type="text/css"/>

  <!-- Experiment files. -->
  <script src="js/enforcer_0.js"></script>

  <!-- Experiment specific helper functions. -->
  <script src="js/enforcer_0_utils.js"></script>
</head>

<body onload="init();">
  <noscript>This task requires JavaScript.</noscript>

  <!-- Introduction slide. -->
  <div class="slide" id="i0">
    <div>
      <img id="logo" style="height:50px;width:50px;" src="shared/images/yale.jpg">
      <span id="logo">Computation and Cognitive Development Lab</span>
    </div>
    <div id="instruct-text">
      <!-- <p>In this experiment, you will be presented with a story and asked to answer some multiple-choice questions. The experiment should take about <span class="time"></span> minutes. You will also be eligible for a bonus. Please read carefully, thanks!</p> -->
      <p>In this experiment, you will be presented with a story and asked to answer some multiple-choice questions. The experiment should take about <span class="time"></span> minutes. Please read carefully, thanks!</p>
    </div>
    <div id="legal">
      <span style="text-align:center;font-weight:bold;">LEGAL INFORMATION</span>
      <br><br>
      <div style="height:30%;width:80%;margin:0px auto;border:1px solid #ccc;overflow:auto;">
        <p>Informed Consent Form</p>
        <p align="left">Purpose: We are conducting research on reasoning.</p>
        <p align="left">Procedures: This experiment takes around <span class="time"></span> minutes to complete. You will first view a story. Then, in each trial, you will view images and answer some multiple-choice questions. You will receive <span class="payment"></span> upon completing the experiment.</p>
        <p align="left">Risks and Benefits: Completing this task poses no more risk of harm to you than do the experiences of everyday life (e.g., from working on a computer). Although this study will not benefit you personally, it will contribute to the advancement of our understanding of human reasoning.</p>
        <p align="left">Confidentiality: All of the responses you provide during this study will be anonymous. You will not be asked to provide any identifying information, such as your name, in any of the questionnaires. Typically, only the researchers involved in this study and those responsible for research oversight will have access to the information you provide. However, we may also share the data with other researchers so that they can check the accuracy of our conclusions; this will not impact you because the data are anonymous. The researcher will not know your name, and no identifying information will be connected to your survey answers in any way. The survey is therefore anonymous. However, your account is associated with an mTurk number that the researcher has to be able to see in order to pay you, and in some cases these numbers are associated with public profiles which could, in theory, be searched. For this reason, though the researcher will not be looking at anyone's public profiles, the fact of your participation in the research (as opposed to your actual survey responses) is technically considered "confidential" rather than truly anonymous.</p>
        <p align="left">Voluntary Participation: Your participation in this study is voluntary. You are free to decline to participate, to end your participation at any time for any reason, or to refuse to answer any individual question. Questions: If you have any questions about this study, you may contact Michael Lopez-Brau at <a style="text-decoration:none" href="mailto:michael.lopez-brau@yale.edu">michael.lopez-brau@yale.edu</a> or Julian Jara-Ettinger at julian.jara-ettinger@yale.edu. If you would like to talk with someone other than the researchers to discuss problems or concerns, to discuss situations in the event that a member of the research team is not available, or to discuss your rights as a research participant, you may contact, and mention HSC number 2000020357:</p>
        <p align="left" style="text-indent:180px;margin:0;">Yale University Human Subjects Committee</p>
        <p align="left" style="text-indent:180px;margin:0;">Box 208010, New Haven, CT 06520-8010</p>
        <p align="left" style="text-indent:180px;margin:0;">(203) 785-4688; human.subjects@yale.edu</p>
        <p align="left">Additional information is available <a style="text-decoration:none;" href="https://your.yale.edu/research-support/human-research/research-participants/rights-research-participant">here</a>.</p>
      </div>
      <p align="left">Agreement to participate: By clicking the button below, you acknowledge that you have read the above information, and agree to participate in the study. You must be at least 18 years of age to participate; agreeing to participate confirms you are 18 years of age or older.  Click the "Start Experiment" button to confirm your agreement and continue.</p>
    </div>
    <button id="start_button" type="button">Start Experiment</button>
  </div>

  <!-- Background slides. -->
  <div class="slide" id="background_0">
    <h3>Background</h3>
    <p>There will be a quiz at the end of the instructions. Please read carefully! You must pass the quiz to be eligible for the experiment. If you fail the quiz <b>twice</b>, you will be ineligible for the experiment.</p>
    <button onclick="_s.button()">Continue</button>
  </div>
  <div class="slide" id="background_1">
    <h3>Background</h3>
    <p>Imagine you're working on a renovation inside of an office building.</p>
    <div align="center">
      <img style="height:150px;width:auto;" src="../stimuli/enforcer_0/construction_worker.png">
    </div>
    <button onclick="_s.button()">Continue</button>
  </div>
  <div class="slide" id="background_2">
    <h3>Background</h3>
    <p>There are two doors that an employee can take to get through the building. One of these doors leads to the renovation site.</p>
    <br><br>
    <div align="center">
      <img style="height:280px;width:220px;" src="../stimuli/enforcer_0/closed_door.png"><img style="height:280px;width:220px;" src="../stimuli/enforcer_0/closed_door_employee.png">
    </div>
    <button onclick="_s.button()">Continue</button>
  </div>
  <div class="slide" id="background_3">
    <h3>Background</h3>
    <div class="background_3"></div>
    <button onclick="_s.button()">Continue</button>
  </div>
  <div class="slide" id="background_4">
    <h3>Background</h3>
    <div class="background_4"></div>
    <button onclick="_s.button()">Continue</button>
  </div>
  <div class="slide" id="background_5">
    <h3>Background</h3>
    <div class="background_5"></div>
    <button onclick="_s.button()">Continue</button>
  </div>
  <div class="slide" id="background_6">
    <h3>Background</h3>
    <div class="background_6"></div>
    <button onclick="_s.button()">Continue</button>
  </div>
  <div class="slide" id="background_7">
    <h3>Background</h3>
    <div class="background_7"></div>
    <button onclick="_s.button()">Continue</button>
  </div>

  <!-- Instruction slides. -->
  <!-- <div class="slide" id="instructions_0">
    <h3>Background</h3>
    <p>In this experiment, you have the chance to earn a bonus. The fewer rocks that you use, the higher your bonus will be.</p>
    <p>You will start off with a bonus of $1.00. Moving the rocks is hard work, so each rock you decide to place will cost $0.10 from your bonus.</p>
    <p>In a separate experiment, we have obtained data for how people choose a door in the role of employees. If at least 50% of employees avoid your door, you will earn <b>an additional $0.50 to your bonus</b>.</p>
    <p>For example, if you place 2 rocks (costing $0.20) and the majority of employees avoid your door, your bonus will total $1.30.</p>
    <button onclick="_s.button()">Continue</button>
  </div> -->
  <div class="slide" id="instructions_0">
    <h3>Background</h3>
    <!-- <p>Lastly, different employees have different preferences for walking through a particular door. However, all employees can always use either door to navigate through the building.</p> -->
    <!-- <p>You will complete this task 3 different times. Each time, we will tell you whether the employee prefers using one of the doors or not.</p> -->
    <p><b>One last thing</b>: We are going to ask you about 3 employees, so you will complete this task 3 different times.</p>
    <p>The employees are all identical <b>except</b> that they each have a different preference for walking through a particular door when there's no renovations going on. For each employee, we will tell you what their preference is, but remember that everything else about them is the same.</p>
    <p>When deciding how many rocks to place, keep in mind that any rocks you place for one employee will <b>not</b> be seen by the other employees, so only plan for one employee at a time.</p>
    <!-- <p>On each trial, you will receive 1 chance at a bonus, for a maximum of 3 bonuses.</p> -->
    <p>For the quiz, answer as if there was still just one employee. Press "Continue" to begin the quiz.</p>
    <button onclick="_s.button()">Continue</button>
  </div>

  <!-- Inclusion survey slide. -->
  <div class="slide" id="inclusion_survey">
    <h3>Inclusion Survey</h3>
    <p class="survey_questions"></p>
    <p class="survey_error">Please answer all of the questions before continuing.</p>
    <button onclick="_s.button()">Continue</button>
  </div>

  <!-- Trial slides. -->
  <div class="trial_slides"></div>

  <!-- Subject information slides. -->
  <div class="slide"  id="subj_info">
    <div class="long_form">
      <div class="subj_info_title">Additional Information</div>
      <p class="info">Please answer the following questions, as they will help us understand your answers.</p>
      <p>Did you read the instructions and do you think you did the experiment correctly?</p>
      <label><input type="radio" name="assess" value="No"/>No</label>
      <label><input type="radio" name="assess" value="Yes"/>Yes</label>
      <label><input type="radio" name="assess" value="Confused"/>I was confused</label>
      <p>Were there any problems or bugs in the experiment?</p>
      <textarea id="problems" rows="2" cols="50"></textarea>
      <p>Gender:
        <select id="gender">
          <label><option value=""/></label>
          <label><option value="Male"/>Male</label>
          <label><option value="Female"/>Female</label>
          <label><option value="Other"/>Other</label>
        </select>
      </p>
      <p>Age: <input type="text" id="age" required/></p>
      <p>Level of Education:
        <select id="education">
          <label><option value="-1"/></label>
          <label><option value="0"/>Some High School</label>
          <label><option value="1"/>Graduated High School</label>
          <label><option value="2"/>Some College</label>
          <label><option value="3"/>Graduated College</label>
          <label><option value="4"/>Hold a higher degree</label>
        </select>
      </p>
      <p>Native Language: <input type="text" id="language"/></p>
      <label>(the language(s) spoken at home when you were a child)</label>
      <p>Any additional comments about this experiment:</p>
      <textarea id="comments" rows="3" cols="50"></textarea>
      <br/>
      <button onclick="_s.submit()">Submit</button>
    </div>
  </div>

  <div id="thanks" class="slide js">
    <p class="big">Thank you for your participation! Press "Finish Experiment" to finish the experiment and receive your completion link.</p>
    <div class="end"></div>
  </div>

  <div class="progress">
    <span>Progress:</span>
    <div class="bar-wrapper">
      <div class="bar" width="0%"></div>
    </div>
  </div>
</body>
</html>
