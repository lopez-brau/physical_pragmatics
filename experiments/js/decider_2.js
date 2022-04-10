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
  for (var i = 0; i <= 0; i++) {
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

  // Set up a trial slide.
  function start() {
    $(".trial_error").hide();
    $(".slider_row").remove();

    // Show the stimulus.
    $(".display_prompt").html("Here someone placed " + exp.prompts[j]);
    $(".display_stimulus").html("<img style=\"height:280px;width:auto;\" src=\"../stimuli/decider_2/" +
      exp.trials[j] + "\"></img>");

    // Make the sliders.
    exp.sentence = [
      "How unusual do you think it would be for someone to leave this here?"
    ];
    $("#multi_slider_table" + (j+1)).append(
      "<tr class=\"slider_row\"><td class=\"slider_target\" id=\"sentence_0" +
      "\">" + exp.sentence[0] + "</td><td colspan=\"2\"><div id=\"slider_0" +
      "\" class=\"slider\">-------[ ]--------</div></td></tr>");
    utils.match_row_height("#multi_slider_table" + (j+1), ".slider_target");
    utils.make_slider("#slider_0", make_slider_callback(0));
    exp.sliderPost = [];
  }

  // Run when the "Continue" button is hit on a slide.
  function button() {
    if (exp.sliderPost[0] === undefined) {
      $(".trial_error").show();
    } else {
      exp.data_trials.push({
        "trial_num": j + 1,
        "stimuli": exp.trials[j],
        "target": exp.sliderPost[0]
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
        "trials": exp.data_trials,
        "system": exp.system,
        "subject_information": exp.subj_data,
        "time_in_minutes": (Date.now() - exp.startT) / 60000
      };
      $(".end").html(
        "<form method=\"post\" action=\"decider_2/end.php\">" +
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

  // Initialize the task duration and payment amount.
  exp.time = 5;
  $(".time").html(exp.time);
  exp.rate = 13.00;
  $(".payment").html("$" + (exp.time/60*exp.rate).toPrecision(3));

  // Define which doors are open and closed.
  exp.doors = {
    "plant": "closed",
    "chair": "open",
    "books": "open",
    "cinderblocks": "open",
    "tape": "closed",
    "rulers": "open",
    "hat": "closed",
    "string": "closed"
  };

  // Extract the condition information.
  exp.condition_assignment = condition_assignment.replace(/\r\n/g, "").split(",");
  exp.first_condition = exp.condition_assignment[0];
  exp.first_object = exp.condition_assignment[1];
  exp.second_condition = exp.condition_assignment[2];
  exp.second_object = exp.condition_assignment[3];

  // Set up the basic trial information.
  exp.prompts = [
    generate_prompt(exp.first_condition, exp.first_object),
    generate_prompt(exp.second_condition, exp.second_object)
  ];
  exp.trials = [
    exp.doors[exp.first_object] + "_" + exp.first_condition + "_" + exp.first_object + ".png",
    exp.doors[exp.second_object] + "_" + exp.second_condition + "_" + exp.second_object + ".png"
  ];
  exp.num_trials = exp.trials.length;
  $(".num_trials").html(exp.num_trials);
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
  exp.structure = [
    "i0",
    "background_0",
    "instructions_0"
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
