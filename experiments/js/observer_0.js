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
  for (var i = 0; i <= 5; i++) {
    slides["background_" + i] = slide({
      name: "background_" + i,
      start: function() {},
      button: function() { exp.go(); }
    });
  }

  // Set up the instructions slides.
  for (var i = 0; i <= 1; i++) {
    slides["instructions_" + i] = slide({
      name: "instructions_" + i,
        start: function() {},
        button: function() { exp.go(); }
      });
  }

  // Set up the catch trial slide.
  slides.catch_trial = slide({
    name: "catch_trial",
    start: function() {
      $(".catch_error_incomplete").hide();
      $(".catch_error_incorrect").hide();

      exp.sentence = [
        "Do the farmers prefer that hikers take pears or pomegranates?",
        "What is the minimum number of boulders each farmer can place?",
        "What is the maximum number of boulders each farmer can place?",
        "Do the hikers ever realize that a farmer placed the boulder(s), if any?",
        "What are the two features that make it harder for hikers to get to a fruit grove?"
      ];

      $(".catch_slide").html(
        "<p>" + exp.sentence[0] + "</p><p>" +
        "<label><input type=\"radio\" name=\"sentence_0\" value=\"Pears\"/>Pears</label>" +
        "<label><input type=\"radio\" name=\"sentence_0\" value=\"Pomegranates\"/>Pomegranates</label>" +
        "<label><input type=\"radio\" name=\"sentence_0\" value=\"Not_sure\"/>Not sure</label>" +
        "</p><p>" + exp.sentence[1] + "</p><p>" +
        "<label><input type=\"radio\" name=\"sentence_1\" value=\"0\"/>0</label>" +
        "<label><input type=\"radio\" name=\"sentence_1\" value=\"1\"/>1</label>" +
        "<label><input type=\"radio\" name=\"sentence_1\" value=\"2\"/>2</label>" +
        "<label><input type=\"radio\" name=\"sentence_1\" value=\"3\"/>3</label>" +
        "<label><input type=\"radio\" name=\"sentence_1\" value=\"Not_sure\"/>Not sure</label>" +
        "</p><p>" + exp.sentence[2] + "</p><p>" +
        "<label><input type=\"radio\" name=\"sentence_2\" value=\"0\"/>0</label>" +
        "<label><input type=\"radio\" name=\"sentence_2\" value=\"1\"/>1</label>" +
        "<label><input type=\"radio\" name=\"sentence_2\" value=\"2\"/>2</label>" +
        "<label><input type=\"radio\" name=\"sentence_2\" value=\"3\"/>3</label>" +
        "<label><input type=\"radio\" name=\"sentence_2\" value=\"Not_sure\"/>Not sure</label>" +
        "</p><p>" + exp.sentence[3] + "</p><p>" +
        "<label><input type=\"radio\" name=\"sentence_3\" value=\"Yes\"/>Yes</label>" +
        "<label><input type=\"radio\" name=\"sentence_3\" value=\"No\"/>No</label>" +
        "<label><input type=\"radio\" name=\"sentence_3\" value=\"Not_sure\"/>Not sure</label>" +
        "</p><p>" + exp.sentence[4] + "</p><p>" +
        "<label><input type=\"checkbox\" name=\"sentence_4_0\" value=\"Weather\"/>Weather  </label>" +
        "<label><input type=\"checkbox\" name=\"sentence_4_1\" value=\"Distance\"/>Distance from the grove  </label>" +
        "<label><input type=\"checkbox\" name=\"sentence_4_2\" value=\"Time_of_day\"/>Time of day  </label>" +
        "<label><input type=\"checkbox\" name=\"sentence_4_3\" value=\"Boulders\"/>Boulders  </label>" +
        "<label><input type=\"checkbox\" name=\"sentence_4_4\" value=\"Not_sure\"/>Not sure  </label></p>" +
        "</p>"
      );
    },
    button: function() {
      exp.target_0 = $("input[name='sentence_0']:checked").val();
      exp.target_1 = $("input[name='sentence_1']:checked").val();
      exp.target_2 = $("input[name='sentence_2']:checked").val();
      exp.target_3 = $("input[name='sentence_3']:checked").val();
      exp.target_4_0 = ($("input[name='sentence_4_0']:checked").val() == "Weather") ? 1 : 0;
      exp.target_4_1 = ($("input[name='sentence_4_1']:checked").val() == "Distance") ? 1 : 0;
      exp.target_4_2 = ($("input[name='sentence_4_2']:checked").val() == "Time_of_day") ? 1 : 0;
      exp.target_4_3 = ($("input[name='sentence_4_3']:checked").val() == "Boulders") ? 1 : 0;
      exp.target_4_4 = $("input[name='sentence_4_4']:checked").val();

      // If a participant fails to answer every question.
      if ((exp.target_0 == undefined) || (exp.target_1 == undefined) ||
          (exp.target_2 == undefined) || (exp.target_3 == undefined) ||
          ((exp.target_4_0 + exp.target_4_1 + exp.target_4_2 + exp.target_4_3 == 0) && (exp.target_4_4 != "Not sure"))) {
        $(".catch_error_incorrect").hide();
        $(".catch_error_incomplete").show();
      }

      // If a participant doesn't answer the last question properly.
      else if (((exp.target_4_0 + exp.target_4_1 + exp.target_4_2 + exp.target_4_3 != 2) && (exp.target_4_4 != "Not sure")) ||
               ((exp.target_4_0 + exp.target_4_1 + exp.target_4_2 + exp.target_4_3 != 0) && (exp.target_4_4 == "Not sure"))) {
        $(".catch_error_incomplete").hide();
        $(".catch_error_incorrect").show();
      }

      // If a participant fails to answer all questions properly.
      else if ((exp.target_0 != "Pears") || (exp.target_1 != "0") || (exp.target_2 != "3") ||
               (exp.target_3 != (exp.condition == "non-agentive" ? "No" : "Yes")) ||
               (exp.target_4_1 != 1) || (exp.target_4_3 != 1)) {
        // Convert the last response into a bit string.
        exp.target_4 = exp.target_4_0.toString() +
          exp.target_4_1.toString() +
          exp.target_4_2.toString() +
          exp.target_4_3.toString() +
          (exp.target_4_4 == "Not_sure" ? "1" : "0");

        // Stitch the participant responses together and send them as URL
        // parameters.
        exp.quiz = [
          exp.target_0,
          exp.target_1,
          exp.target_2,
          exp.target_3,
          exp.target_4
        ];
        window.location.replace("https://compdevlab.yale.edu/studies/lopez-brau/" +
          "physical_pragmatics/experiments/observer_0/fail.php" +
          "?PROLIFIC_PID=" + exp.id + "&QUIZ=" + exp.quiz.join("-"));
      } else {
        exp.catch_trials.push({
          "actor_preference": "pomegranates",
          "sentence_0": exp.sentence[0],
          "target_0": exp.target_0,
          "sentence_1": exp.sentence[1],
          "target_1": exp.target_1,
          "sentence_2": exp.sentence[2],
          "target_2": exp.target_2,
          "sentence_3": exp.sentence[3],
          "target_3": exp.target_3,
          "sentence_4": exp.sentence[4],
          "target_4_0": exp.target_4_0,
          "target_4_1": exp.target_4_1,
          "target_4_2": exp.target_4_2,
          "target_4_3": exp.target_4_3,
          "target_4_4": exp.target_4_4,
          "quiz_attempts": quiz_attempts
        });
        exp.go();
      }
    }
  });

  // Set up a trial slide.
  function start() {
    $(".trial_error").hide();
    $(".slider_row").remove();

    // Show the setup and the stimulus.
    $(".display_setup").html("Consider the following scenario with a <b>new</b> farmer and farm.");
    $(".display_stimulus").html("<img style=\"height:280px;width:auto;\" src=\"../stimuli/observer_0/" +
      exp.trials[j] + "\"></img>");

    // Make the sliders.
    exp.sentence = [
      "How much does this farmer think that hikers like pomegranates?",
      "How cooperative does this farmer think hikers are?"
    ];
    if (exp.condition == "non-agentive") {
      $("#multi_slider_table" + (j+1)).append(
        "<tr class=\"slider_row\"><td class=\"slider_target\" id=\"sentence_0" +
        "\">" + exp.sentence[0] + "</td><td colspan=\"2\"><div id=\"slider_0" +
        "\" class=\"slider\">-------[ ]--------</div></td></tr>");
      utils.match_row_height("#multi_slider_table" + (j+1), ".slider_target");
      utils.make_slider("#slider_0", make_slider_callback(0));
    } else if (exp.condition == "agentive") {
      $("#multi_slider_table" + (j+1)).append(
        "<tr class=\"slider_row\"><td class=\"slider_target\" id=\"sentence_0" +
        "\">" + exp.sentence[0] + "</td><td colspan=\"2\"><div id=\"slider_0" +
        "\" class=\"slider\">-------[ ]--------</div></td></tr>" +
        "<tr><td></td>" +
        "<td class=\"left\">not at all</td>" +
        "<td class=\"right\">very much</td>" +
        "</tr>" +
        "<tr class=\"slider_row\"><td class=\"slider_target\" id=\"sentence_1" +
        "\">" + exp.sentence[1] + "</td><td colspan=\"2\"><div id=\"slider_1" +
        "\" class=\"slider\">-------[ ]--------</div></td></tr>");
      utils.match_row_height("#multi_slider_table" + (j+1), ".slider_target");
      utils.make_slider("#slider_0", make_slider_callback(0));
      utils.make_slider("#slider_1", make_slider_callback(1));
    }
    exp.sliderPost = [];
  }

  // Run when the "Continue" button is hit on a slide.
  function button() {
    if ((exp.condition == "non-agentive") &&
        (exp.sliderPost[0] === undefined)) {
      $(".trial_error").show();
    } else if ((exp.condition == "agentive") &&
        ((exp.sliderPost[0] === undefined) || (exp.sliderPost[1] === undefined))) {
      $(".trial_error").show();
    } else {
      exp.data_trials.push({
        "trial_num": j + 1,
        "decider_coords": exp.trials[j].slice(0, 9),
        "pear_coords": exp.trials[j].slice(10, 19),
        "layout": exp.trials[j].slice(20, 31),
        "sentence_0": exp.sentence[0],
        "target_0": exp.sliderPost[0],
        "sentence_1": (exp.condition == "non-agentive") ? -1 : exp.sentence[1],
        "target_1": (exp.condition == "non-agentive") ? -1 : exp.sliderPost[1]
      });
      j++;
      exp.go();
    }
  }

  function make_slider_callback(i) {
    return function(event, ui) { exp.sliderPost[i] = ui.value; };
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
        "catch_trials": exp.catch_trials,
        "trials": exp.data_trials,
        "system": exp.system,
        "subject_information": exp.subj_data,
        "time_in_minutes": (Date.now() - exp.startT) / 60000
      };
      $(".end").html(
        "<form method=\"post\" action=\"observer_0/end.php\">" +
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

  // Initialize the task duration and payment amount.
  exp.time = 20;
  $(".time").html(exp.time);
  exp.rate = 13.00;
  $(".payment").html("$" + (exp.time/60*exp.rate).toPrecision(3));

  // Set up the experiment condition and some experiment-specific text.
  exp.condition = "non-agentive";
  if (exp.condition == "non-agentive") {
    $(".background_4").html(
      "<div align=\"center\">" +
      "<img style=\"height:320px;width:auto;\" src=\"../stimuli/observer_0/hiker_reasoning_1.png\">" +
      "</div>" +
      "<p align=\"left\" style=\"text-indent:40px\">" +
      "Hikers never realize that the boulders were placed by a farmer, and " +
      "instead think they were there naturally. They consider how much " +
      "effort it takes to pass the boulders when deciding which fruit to " +
      "take." +
      "</p>"
    );
    $(".background_5").html(
      "<div align=\"center\">" +
      "<img style=\"height:320px;width:auto;\" src=\"../stimuli/observer_0/farmer_reasoning_1.png\">" +
      "</div>" +
      "<p align=\"left\" style=\"text-indent:40px\">" +
      "Farmers think that hikers will go for the fruit they like the best. " +
      "They assume that the hikers will only think about the effort it " +
      "takes to walk around the boulders." +
      "</p>"
    );
    $(".task").html("<li>How much each farmer thinks that hikers like pomegranates (from \"not at all\" to \"very much\")</li>");
  } else if (exp.condition == "agentive") {
    $(".background_4").html(
      "<div align=\"center\">" +
      "<img style=\"height:320px;width:auto;\" src=\"../stimuli/observer_0/hiker_reasoning_0.png\">" +
      "</div>" +
      "<p align=\"left\" style=\"text-indent:40px\">" +
      "Hikers always realize that the boulders were placed by a farmer, and " +
      "they consider why the farmer placed them there when deciding which " +
      "fruit to take." +
      "</p>"
    );
    $(".background_5").html(
      "<div align=\"center\">" +
      "<div style=\"padding-right:40px;border-right:1px solid #000000;display:inline-block;vertical-align:top;width:40%;\">" +
      "<img style=\"height:320px;width:auto;\" src=\"../stimuli/observer_0/farmer_reasoning_0.png\">" +
      "</div>" +
      "<div style=\"display:inline-block;vertical-align:top;margin-left:40px;width:40%;\">" +
      "<img style=\"height:320px;width:auto;\" src=\"../stimuli/observer_0/farmer_reasoning_1.png\">" +
      "</div>" +
      "</div>" +
      "<p align=\"left\" style=\"text-indent:40px\">" +
      "Some farmers are confident that hikers will be respectful of their " +
      "preferences when they see the boulders. Other farmers are less " +
      "confident that hikers will be respectful of their preferences, and " +
      "instead think that hikers will go for the fruit they like the best. " +
      "These farmers assume that the hikers will only think about the " +
      "effort it takes to walk around the boulders." +
      "</p>"
    );
    $(".task").html(
      "<li>How much each farmer thinks that hikers like pomegranates (from \"not at all\" to \"very much\")</li>" +
      "<li>How cooperative each farmer thinks hikers are (from \"not at all\" to \"very much\")</li>"
    );
  }

  // Set up trial slide information.
  exp.pear_position = 1;
  exp.trials = trials(exp.pear_position);
  exp.num_trials = exp.trials.length;
  exp.catch_trials = [];
  exp.data_trials = [];
  $(".num_trials").html(exp.num_trials);

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
  exp.structure = [
    "i0",
    "background_0",
    "background_1",
    "background_2",
    "background_3",
    "background_4",
    "background_5",
    "instructions_0",
    "instructions_1",
    "catch_trial"
  ];
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
