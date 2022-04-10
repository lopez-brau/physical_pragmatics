<?php
// Start/resume the session.
session_start();

// If this is a previous session, reload the PID and quiz attempts;
// otherwise, set them.
if (isset($_SESSION["pid"])) {
  $quiz_attempts = $_SESSION["quiz_attempts"];
  if ($quiz_attempts >= 2) {
    die("Sorry, you failed the quiz too many times. You are not eligible for this study.");
  }
} else {
  $pid = htmlspecialchars($_GET["PROLIFIC_PID"]);
  $quiz_attempts = 0;
  $_SESSION["pid"] = $pid;
  $_SESSION["quiz_attempts"] = $quiz_attempts;
}
?>

<html>
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
  <script src="js/observer_0.js"></script>

  <!-- Experiment specific helper functions. -->
  <script src="js/observer_0_utils.js"></script>
</head>

<body onload="init();">
  <noscript>This task requires JavaScript.</noscript>

  <!-- Introduction slide. -->
  <div class="slide" id="i0">
    <div>
      <img id="logo" style="height:50px;width:50px;" src="shared/images/yale.jpg"></img>
      <span id="logo">Computation and Cognitive Development Lab</span>
    </div>
    <div id="instruct-text">
      <p>In this experiment, you will be presented with a story about several people and asked about what they think. The experiment should take about <span class="time"></span> minutes. Please read carefully, thanks!</p>
    </div>
    <div id="legal">
      <span style="text-align:center;font-weight:bold;">LEGAL INFORMATION</span>
      <br><br>
      <div style="height:30%;width:80%;margin:0px auto;border:1px solid #ccc;overflow:auto;">
        <p>Informed Consent Form</p>
        <p align="left">Purpose: We are conducting research on reasoning.</p>
        <p align="left">Procedures: This experiment takes around <span class="time"></span> minutes to complete. You will first view a story. Then, in each trial, you will view images and answer some range slider questions. You will receive <span class="payment"></span> upon completing the experiment.</p>
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
    <div align="center">
      <img style="height:150px;width:auto;" src="../stimuli/observer_0/farmer.png"></img>
    </div>
    <p>This is a farmer. This farmer is one of many that live along the mountainous countryside of a small town.</p>
    <button onclick="_s.button()">Continue</button>
  </div>
  <div class="slide" id="background_1">
    <h3>Background</h3>
    <div align="center">
      <img style="height:280px;width:auto;" src="../stimuli/observer_0/background_2.png"></img>
    </div>
    <p align="left" style="text-indent:40px">This a typical farm. Each farmer owns a farm with pear and pomegranate crops. Town hikers often take a detour into the farms and take some fruit before returning to their hike. The farmers don't mind, but they prefer that hikers take the pears instead of pomegranates, since the pomegranates are more expensive.</p>
    <button onclick="_s.button()">Continue</button>
  </div>
  <div class="slide" id="background_2">
    <h3>Background</h3>
    <div align="center">
      <div style="vertical-align:middle;display:inline-block;">
        <img style="height:100px;width:auto;" src="../stimuli/observer_0/farmer.png"></img>
      </div>
      <div style="vertical-align:bottom;display:inline-block;">
        <span style="margin-right:10px;"><img style="height:50px;width:auto;" src="../stimuli/observer_0/boulder_0_tray.png" ></img></span>
        <span style="margin-right:10px;"><img style="height:50px;width:auto;" src="../stimuli/observer_0/boulder_1_tray.png" ></img></span>
        <span style="margin-right:10px;"><img style="height:50px;width:auto;" src="../stimuli/observer_0/boulder_2_tray.png" ></img></span>
        <span><img style="height:50px;width:auto;" src="../stimuli/observer_0/boulder_3_tray.png" ></img></span>
      </div>
    </div>
    <p align="left" style="text-indent:40px;">Hikers don't know what preferences farmers have when walking into the farms. Since the farmers don't have any signs, they use boulders to ensure that hikers don't eat the pomegranates. The farmers can place up to 3 boulders around each grove, and hikers would need to walk around them to get the pomegranates.</p>
    <button onclick="_s.button()">Continue</button>
  </div>
  <div class="slide" id="background_3">
    <h3>Background</h3>
    <div align="center" style="vertical-align:bottom;">
      <img style="height:150px;width:auto;" src="../stimuli/observer_0/tired_farmer.png"></img>
      <img style="margin-right:35px;height:107px;width:auto;" src="../stimuli/observer_0/boulder.png"></img>
      <img style="margin-left:35px;margin-right:20px;height:107px;width:auto;" src="../stimuli/observer_0/tired_hiker.png"></img>
      <img style="height:107px;width:auto;" src="../stimuli/observer_0/tile.png"></img>
    </div>
    <p align="left" style="text-indent:40px;">It's exhausting for the farmers to place the boulders. As a result, farmers only place the minimum number of boulders they think they need to. Similarly, hikers want to walk the least amount possible while pursuing a grove so that they can get back to their hike. The groves are always visible to the hikers, even if there are boulders in the way.</p>
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
    
  <!-- Instruction slides. -->
  <div class="slide" id="instructions_0">
    <h3>Instructions</h3>
    <p align="left" style="text-indent:40px">On each trial, you will see a different hiker at the entrance to a different farmer's farm and how many boulders that farmer arranged, if any. The farms will be slightly different in each trial. Below are some examples of some of the farms you'll see:</p>
    <div>
      <img style="vertical-align:middle;margin-right:30px;height:180px;width:auto" src="../stimuli/observer_0/instructions_0.png"></img>
      <img style="vertical-align:middle;margin-left:30px;height:180px;width:auto" src="../stimuli/observer_0/instructions_1.png"></img>
    </div>
    <p align="left" style="text-indent:40px"><b>Your task is to figure out what each farmer was thinking when they arranged the boulders.</b> Specifically, you will decide:</p>
    <ul class="task" style="text-align:left;"></ul>
    <p align="left">The hiker can move horizontally or vertically on the grid, but not diagonally. They also cannot walk across tiles that have boulders.</p>
    <button onclick="_s.button()">Continue</button>
  </div>
  <div class="slide" id="instructions_1">
    <h3>Instructions</h3>
    <p align="left" style="text-indent:40px">There are <span class="num_trials"></span> trials in total. Before you begin, please answer the following questions. You <b>must</b> answer them correctly to continue. If you fail to answer them correctly, you will be sent back to re-read the story.</p>
    <button onclick="_s.button()">Continue</button>
  </div>

  <!-- Catch trial slide. -->
  <div class="slide" id="catch_trial">
    <p class="catch_slide"></p>
    <p class="catch_error_incomplete">Please answer all of the questions before continuing.</p>
    <p class="catch_error_incorrect">Please select two features or "Not sure" but not both.</p>
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
