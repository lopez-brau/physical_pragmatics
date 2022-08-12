var j = 0;

function make_slides(f) {
  var slides = {};

  slides.i0 = slide({
    name: "i0",
    start: function() {
      exp.startT = Date.now();
    }
  });

  // Set up the background slides.
  for (var i = 0; i <= 7; i++) {
    slides["background_" + i] = slide({
      name: "background_" + i,
      start: function() {},
      button: function() { exp.go(); }
    });
  }

  // Set up the instruction slides.
  for (var i = 0; i <= 0; i++) {
    slides["instructions_" + i] = slide({
      name: "instructions_" + i,
        start: function() {},
        button: function() { exp.go(); }
      });
  }

  // Set up the inclusion survey slide.
  slides.inclusion_survey = slide({
    name: "inclusion_survey",
    start: function() {
      $(".survey_error").hide();

      exp.sentence = [
        "Which door do you want this employee to avoid?",
        "What is the least amount of rocks you can place?",
        "What is the most amount of rocks you can place?",
        "Is it harder for this employee to cross through a door with 2 rocks than it is for them to cross through a door with 1 rock?",
        // "How much does it cost you to place a rock?",
        "Will this employee realize that the rocks were intentionally placed by someone else and think about them?"
      ];

      $(".survey_questions").html(
        "<p style=\"margin-bottom:0px;\">" + exp.sentence[0] + "</p>" +
        "<p style=\"margin-top:5px;\">" +
        "<label><input type=\"radio\" name=\"sentence_0\" value=\"0\"/>Left</label>" +
        "<label><input type=\"radio\" name=\"sentence_0\" value=\"1\"/>Right</label>" +
        "<label><input type=\"radio\" name=\"sentence_0\" value=\"2\"/>Both</label>" +
        "</p>" +
        "<p style=\"margin-bottom:0px;\">" + exp.sentence[1] + "</p>" +
        "<p style=\"margin-top:5px;\">" +
        "<label><input type=\"radio\" name=\"sentence_1\" value=\"0\"/>0</label>" +
        "<label><input type=\"radio\" name=\"sentence_1\" value=\"1\"/>2</label>" +
        "<label><input type=\"radio\" name=\"sentence_1\" value=\"2\"/>3</label>" +
        "<label><input type=\"radio\" name=\"sentence_1\" value=\"3\"/>4</label>" +
        "</p>" +
        "<p style=\"margin-bottom:0px;\">" + exp.sentence[2] + "</p>" +
        "<p style=\"margin-top:5px;\">" +
        "<label><input type=\"radio\" name=\"sentence_2\" value=\"0\"/>0</label>" +
        "<label><input type=\"radio\" name=\"sentence_2\" value=\"1\"/>2</label>" +
        "<label><input type=\"radio\" name=\"sentence_2\" value=\"2\"/>3</label>" +
        "<label><input type=\"radio\" name=\"sentence_2\" value=\"3\"/>4</label>" +
        "</p>" +
        "<p style=\"margin-bottom:0px;\">" + exp.sentence[3] + "</p>" +
        "<p style=\"margin-top:5px;\">" +
        "<label><input type=\"radio\" name=\"sentence_3\" value=\"0\"/>Yes</label>" +
        "<label><input type=\"radio\" name=\"sentence_3\" value=\"1\"/>No</label>" +
        "</p>" +
        // "<p style=\"margin-bottom:0px;\">" + exp.sentence[4] + "</p>" +
        // "<p style=\"margin-top:5px;\">" +
        // "<label><input type=\"radio\" name=\"sentence_4\" value=\"0\"/>$0.10</label>" +
        // "<label><input type=\"radio\" name=\"sentence_4\" value=\"1\"/>$0.20</label>" +
        // "<label><input type=\"radio\" name=\"sentence_4\" value=\"2\"/>$0.25</label>" +
        // "<label><input type=\"radio\" name=\"sentence_4\" value=\"3\"/>$0.30</label>" +
        // "</p>" +
        "<p style=\"margin-bottom:0px;\">" + exp.sentence[4] + "</p>" +
        "<p style=\"margin-top:5px;\">" +
        "<label><input type=\"radio\" name=\"sentence_4\" value=\"0\"/>Yes</label>" +
        "<label><input type=\"radio\" name=\"sentence_4\" value=\"1\"/>No</label>" +
        "</p>"
      );
    },
    button: function() {
      exp.target_0 = $("input[name='sentence_0']:checked").val();
      exp.target_1 = $("input[name='sentence_1']:checked").val();
      exp.target_2 = $("input[name='sentence_2']:checked").val();
      exp.target_3 = $("input[name='sentence_3']:checked").val();
      exp.target_4 = $("input[name='sentence_4']:checked").val();
      // exp.target_5 = $("input[name='sentence_5']:checked").val();

      // If a participant fails to answer every question.
      // if ((exp.target_0 == undefined) || (exp.target_1 == undefined) ||
      //     (exp.target_2 == undefined) || (exp.target_3 == undefined) ||
      //     (exp.target_5 == undefined)) {
      //   $(".survey_error").show();
      // }
      if ((exp.target_0 == undefined) || (exp.target_1 == undefined) ||
          (exp.target_2 == undefined) || (exp.target_3 == undefined)) {
        $(".survey_error").show();
      }

      // If a participant fails to answer all questions properly.
      else if ((exp.target_0 != (exp.renovation_side == "left" ? "0" : "1")) ||
               (exp.target_1 != "0") ||
               (exp.target_2 != "3") ||
               (exp.target_3 != "0") ||
               // (exp.target_4 != "0") ||
               (exp.target_4 != (exp.agent_condition == "agentive" ? "0" : "1"))) {
        // Stitch the participant responses together and send them as URL
        // parameters.
        exp.survey_results = [
          exp.target_0,
          exp.target_1,
          exp.target_2,
          exp.target_3,
          exp.target_4,
          // exp.target_5
        ];
        window.location.replace("https://compdevlab.yale.edu/studies/lopez-brau/" +
          "physical_pragmatics/experiments/enforcer_0/fail.php" +
          "?PROLIFIC_PID=" + exp.id + "&QUIZ=" + exp.survey_results.join("-"));
      } else {
        exp.inclusion_survey.push({
          "agent_condition": exp.agent_condition,
          "renovation_side": exp.renovation_side,
          "sentence_0": exp.sentence[0],
          "target_0": exp.target_0,
          "sentence_1": exp.sentence[1],
          "target_1": exp.target_1,
          "sentence_2": exp.sentence[2],
          "target_2": exp.target_2,
          "sentence_3": exp.sentence[3],
          "target_3": exp.target_3,
          "sentence_4": exp.sentence[4],
          "target_4": exp.target_4,
          // "sentence_5": exp.sentence[5],
          // "target_5": exp.target_5,
          "quiz_attempts": quiz_attempts
        });
        exp.go();
      }
    }
  });

  // Set up a trial slide.
  function start() {
    $(".trial_error").hide();

    // Show the stimulus.
    if (exp.employee_preferences[j] == "none") {
      $(".display_prompt").html("The " + exp.employee_number[j] + " employee has no preference for taking either door.");
    } else {
      $(".display_prompt").html("The " + exp.employee_number[j] + " employee prefers taking the door on the " + exp.employee_preferences[j] + ".");
    }
    $(".display_stimulus").html(
      "<img style=\"height:210px;width:auto;\" src=\"../stimuli/enforcer_0/closed_door.png\">" +
      "<img style=\"height:210px;width:auto;\" src=\"../stimuli/enforcer_0/closed_door_employee.png\">"
    );

    // Make the multiple-choice question.
    $(".display_options").html(
      // "<p style=\"margin-bottom:0px;\">How many rocks will you decide to place?</p>" +
      "<p style=\"margin-bottom:0px;\">What do you think is the <b>minimum</b> number of rocks you need to place to keep this employee away?</p>" +
      "<div style=\"margin-top:5px;\">" +
      "<label style=\"display:inline-block;\">" +
      "<img style=\"height:160px;width:auto;display:block;\" src=\"../stimuli/enforcer_0/closed_door.png\">" +
      "<p style=\"margin:5px 0px 10px 0px;\">0</p>" +
      "<input type=\"radio\" name=\"sentence_" + (j+5) + "\" value=\"0\" style=\"margin:0 auto;\"/>" +
      "</label>" +
      "<label style=\"display:inline-block;\">" +
      "<img style=\"height:160px;width:auto;display:block;\" src=\"../stimuli/enforcer_0/one_rock.png\">" +
      "<p style=\"margin:5px 0px 10px 0px;\">1</p>" +
      "<input type=\"radio\" name=\"sentence_" + (j+5) + "\" value=\"1\" style=\"margin:0 auto;\"/>" +
      "</label>" +
      "<label style=\"display:inline-block;\">" +
      "<img style=\"height:160px;width:auto;display:block;\" src=\"../stimuli/enforcer_0/two_rocks.png\">" +
      "<p style=\"margin:5px 0px 10px 0px;\">2</p>" +
      "<input type=\"radio\" name=\"sentence_" + (j+5) + "\" value=\"2\" style=\"margin:0 auto;\"/>" +
      "</label>" +
      "<label style=\"display:inline-block;\">" +
      "<img style=\"height:160px;width:auto;display:block;\" src=\"../stimuli/enforcer_0/three_rocks.png\">" +
      "<p style=\"margin:5px 0px 10px 0px;\">3</p>" +
      "<input type=\"radio\" name=\"sentence_" + (j+5) + "\" value=\"3\" style=\"margin:0 auto;\"/>" +
      "</label>" +
      "<label style=\"display:inline-block;\">" +
      "<img style=\"height:160px;width:auto;display:block;\" src=\"../stimuli/enforcer_0/four_rocks.png\">" +
      "<p style=\"margin:5px 0px 10px 0px;\">4</p>" +
      "<input type=\"radio\" name=\"sentence_" + (j+5) + "\" value=\"4\" style=\"margin:0 auto;\"/>" +
      "</label>" +
      "</div>"
    );
  }

  // Run when the "Continue" button is hit on a slide.
  function button() {
    exp.target = $("input[name='sentence_" + (j+5) + "']:checked").val();
    if (exp.target === undefined) {
      $(".trial_error").show();
    } else {
      exp.data_trials.push({
        "trial_num": j + 1,
        "agent_condition": exp.agent_condition,
        "renovation_side": exp.renovation_side,
        "employee_preference": exp.trials[j],
        "target": exp.target
      });
      j++;
      exp.go();
    }
  }

  // Stitches together all of the trial slides.
  for (var i = 1; i <= exp.num_trials; i++) {
    slides["trial" + i] = slide({
      name: "trial" + i,
      start: start,
      button: button
    });
  }

  slides.subj_info = slide({
    name: "subj_info",
    start: function() {},
    submit: function(e) {
      exp.subj_data = {
        "language": $("#language").val(),
        "asses": $("input[name='assess']:checked").val(),
        "age": $("#age").val(),
        "gender": $("#gender").val(),
        "education": $("#education").val(),
        "problems": $("#problems").val(),
        "comments": $("#comments").val()
      };
      exp.go();
    }
  });

  slides.thanks = slide({
    name: "thanks",
    start: function() {
      exp.data = {
        "id": exp.id,
        "condition": exp.condition,
        "trials": exp.data_trials,
        "system": exp.system,
        "subject_information": exp.subj_data,
        "time_in_minutes": (Date.now() - exp.startT) / 60000
      };
      $(".end").html(
        "<form method=\"post\" action=\"enforcer_0/end.php\">" +
        "<input type=\"hidden\" name=\"data\" value=\'" +
        JSON.stringify(exp.data).replace(/'/g, "") + "\' />" +
        "<button type=\"submit\">Finish Experiment</button>" +
        "</form>"
      );
    }
  });

  return slides;
}

function init() {
  // Read in the participant ID.
  exp.id = get_url_parameters("PROLIFIC_PID");

  // Read in this participant's quiz attempts.
  exp.quiz_attempts = quiz_attempts;

  // Initialize the task duration and payment amount (affected by possible bonus).
  exp.time = 8;
  $(".time").html(exp.time);
  exp.rate = 12.00;
  $(".payment").html("$" + (exp.time/60*exp.rate).toPrecision(3));

  // Extract the condition information.
  exp.condition_assignment = condition_assignment.replace(/\r\n/g, "").split(",");
  console.log(exp.condition_assignment);
  exp.agent_condition = exp.condition_assignment[0];
  exp.renovation_side = exp.condition_assignment[1];
  exp.employee_preferences = exp.condition_assignment.slice(2, 5);
  exp.employee_number = ["first", "second", "third"];

  // Set up condition-specific text.
  if (exp.renovation_side == "left") {
    $(".background_3").html(
      "<p>Your job, as a construction worker, is to <b>make sure this " +
      "employee doesn't walk through the door on the " + exp.renovation_side +
      "</b> while you're working inside.</p>" +
      "<br>" +
      "<div align=\"center\">" +
      "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/renovation_door.png\">" +
      "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/closed_door.png\">" +
      "</div>"
    );
    $(".background_4").html(
      "<p>Normally, you'd use construction tape or signs to try to keep " +
      "them out, but you don't have either. Instead, you have 4 large " +
      "rocks that you can place in front of the door. You and this " +
      "employee are never in the same room at the same time, so they only " +
      "see the rocks you leave behind, if any.</p>" +
      "<div align=\"center\">" +
      "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/closed_door_construction_worker.png\">" +
      "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/opaque_door.png\">" +
      "</div>"
    );
    if (exp.agent_condition == "agentive") {
      $(".background_5").html(
        "<p>When this employee sees any number of rocks in front of a " +
        "door, they will know that someone must have put them there on " +
        "purpose, and think about why someone would do that.</p>" +
        "<br>" +
        "<div align=\"center\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/closed_door.png\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/opaque_door_employee.png\">" +
        "</div>"
      );
      $(".background_6").html(
        "<p>This employee is very cooperative and will avoid going into the " +
        "renovation site. They just don't know where it is and could " +
        "accidentally walk into it.</p>" +
        "<br>" +
        "<div align=\"center\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/closed_door.png\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/opaque_door_employee.png\">" +
        "</div>"
      );
    } else {
      $(".background_5").html(
        "<p>When this employee sees any amount of rocks in front of a " +
        "door, they will not realize that someone put them there on " +
        "purpose, and will think they must have ended up there by " +
        "accident.</p>" +
        "<br>" +
        "<div align=\"center\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/closed_door.png\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/opaque_door_employee.png\">" +
        "</div>"
      );
    }
  } else {
    $(".background_3").html(
      "<p>Your job, as a construction worker, is to <b>make sure this " +
      "employee doesn't walk through the door on the " + exp.renovation_side +
      "</b> while you're working inside.</p>" +
      "<br>" +
      "<div align=\"center\">" +
      "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/closed_door.png\">" +
      "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/renovation_door.png\">" +
      "</div>"
    );
    $(".background_4").html(
      "<p>Normally, you'd use construction tape or signs to try to keep " +
      "them out, but you don't have either. Instead, you have 4 large " +
      "rocks that you can place in front of the door. You and this " +
      "employee are never in the same room at the same time, so they only " +
      "see the rocks you leave behind, if any.</p>" +
      "<div align=\"center\">" +
      "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/opaque_door_construction_worker.png\">" +
      "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/closed_door.png\">" +
      "</div>"
    );
    if (exp.agent_condition == "agentive") {
      $(".background_5").html(
        "<p>When this employee sees any number of rocks in front of a " +
        "door, they will know that someone must have put them there on " +
        "purpose, and think about why someone would do that.</p>" +
        "<br>" +
        "<div align=\"center\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/opaque_door.png\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/closed_door_employee.png\">" +
        "</div>"
      );
      $(".background_6").html(
        "<p>This employee is very cooperative and will avoid going into the " +
        "renovation site. They just don't know where it is and could " +
        "accidentally walk into it.</p>" +
        "<br>" +
        "<div align=\"center\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/opaque_door.png\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/closed_door_employee.png\">" +
        "</div>"
      );
    } else {
      $(".background_5").html(
        "<p>When this employee sees any amount of rocks in front of a " +
        "door, they will not realize that someone put them there on " +
        "purpose, and will think they must have ended up there by " +
        "accident.</p>" +
        "<br>" +
        "<div align=\"center\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/opaque_door.png\">" +
        "<img style=\"height:280px;width:220px;\" src=\"../stimuli/enforcer_0/closed_door_employee.png\">" +
        "</div>"
      );
    }
  }

  // Set up the basic trial information.
  exp.trials = exp.employee_preferences;
  exp.num_trials = exp.trials.length;
  $(".num_trials").html(exp.num_trials);
  exp.inclusion_survey = [];
  exp.data_trials = [];

  // Get user system specs.
  exp.system = {
    Browser: BrowserDetect.browser,
    OS: BrowserDetect.OS,
    screenH: screen.height,
    screenUH: exp.height,
    screenW: screen.width,
    screenUW: exp.width
  };

  // Stitch together the blocks of the experiment.
  if (exp.agent_condition == "agentive") {
    exp.structure = [
      "i0",
      "background_0",
      "background_1",
      "background_2",
      "background_3",
      "background_4",
      "background_5",
      "background_6",
      "background_7",
      // "instructions_0",
      "instructions_0",
      "inclusion_survey"
    ];
  } else {
    exp.structure = [
      "i0",
      "background_0",
      "background_1",
      "background_2",
      "background_3",
      "background_4",
      "background_5",
      "background_7",
      // "instructions_0",
      "instructions_0",
      "inclusion_survey"
    ];
  }
  for (var k = 1; k <= exp.num_trials; k++) {
    exp.structure.push("trial" + k);
  }
  exp.structure.push("subj_info");
  exp.structure.push("thanks");

  // Make and embed the slides.
  exp.slides = make_slides(exp);
  embed_slides(exp.num_trials);

  // Get the length of the experiment.
  exp.nQs = utils.get_exp_length();

  // Hide the slides.
  $(".slide").hide();

  // Make sure Turkers have accepted HIT (or you're not in MTurk).
  $("#start_button").click(function() {
    if (turk.previewMode) {
      $("#mustaccept").show();
    } else {
      $("#start_button").click(function() { $("#mustaccept").show(); });
        exp.go();
    }
  });

  // Launch the slides.
  exp.go();
}
