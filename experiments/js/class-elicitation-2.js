// global variable for storing the index at each slide
var i = 0;

function makeSlides(f) {
  var slides = {};

  slides.i0 = slide({
    name: "i0",
    start: function() {
      exp.startT = Date.now();
    }
  });

  // the catch trial will take the first two indices of the sliders and of exp.sliderPost
  slides.instructions = slide({
    name: "instructions",
    start: function() {
      $(".errCatch").hide();
      var sentenceCatch = ["The Empire State Building is tall relative to other buildings.", "The Empire State Building is tall relative to other pineapples."];
      for (var j = 0; j < exp.nCatch; j++) {
        $("#multi_slider_table0").append("<tr class=\"slider_row\"><td class=\"slider_target\" id=\"sentence" + j + "\">" + sentenceCatch[j] +
          "</td><td colspan=\"2\"><div id=\"slider" + j + "\" class=\"slider\">-------[ ]--------</div></td></tr>");
        utils.match_row_height("#multi_slider_table0", ".slider_target");
        utils.make_slider("#slider" + j, make_slider_callback(j));
      }
      exp.sliderPost = [];
    },
    button: function() {
      if ((exp.sliderPost[0] === undefined) || (exp.sliderPost[1] === undefined)) { $(".errCatch").show(); }
      else {
        exp.catch_trials.push({
          object: "Empire State Building",
          property: "is tall",
          sentence1: "relative to other buildings",
          response1: exp.sliderPost[0],
          sentence2: "relative to other pineapples",
          response2: exp.sliderPost[1]
        });
        exp.go();
      }
    }
  });

  // runs when a slide is first loaded
  function start() {
    $(".err").hide();

    // removes the slider from the previous slide before making the slider for the current slide
    $(".slider_row").remove();

    // Display a 
    $(".display_p1").html("Suppose the ghost places one block on the grid.");

    // Display the stimulus.
    $(".display_stimulus").html("<img src=\"../imgs/stimuli/gridworld_1.png\"></script>");

    // Display the prompt.
    
    sentence1 = "To what degree did the ghost think PacMan wanted this fruit?"
    sentence2 = "Do you think the ghost believes that PacMan is thinking about it's actions?"

    // set up the text next to each slider
    for (var j = exp.nCatch; j < exp.nSentences+exp.nCatch; j++) {
      // display the slider for each slide
      sentence = j == 2 ? sentence1 : sentence2
      $("#multi_slider_table" + (i+1)).append("<tr class=\"slider_row\"><td class=\"slider_target\" id=\"sentence" + j + "\">" + sentence +
        "</td><td colspan=\"2\"><div id=\"slider" + j + "\" class=\"slider\">-------[ ]--------</div></td></tr>");
      utils.match_row_height("#multi_slider_table" + (i+1), ".slider_target");
    }

    init_sliders(exp.nSentences);
    exp.sliderPost = [];
  }

  // the two functions below help set up and read info from the sliders
  function init_sliders(nSentences) {
    for (var j = exp.nCatch; j < nSentences+exp.nCatch; j++) {
      utils.make_slider("#slider" + j,
        make_slider_callback(j));
    }
  }

  function make_slider_callback(j) {
    return function(event, ui) {
      exp.sliderPost[j] = ui.value;
    };
  }

  // runs when the "Continue" button is hit on a slide
  function button() {

    // stores the slider results
    subEndorse = exp.sliderPost[exp.sliderOrder.indexOf("sub_plural")+exp.nCatch];
    superEndorse = exp.sliderPost[exp.sliderOrder.indexOf("super")+exp.nCatch];

    // stores the adjective used in this experiment; same as the target
    adjective = exp.examples[i].target.split(" ").pop();

    if ((subEndorse === undefined) || (superEndorse === undefined)) { $(".err").show(); }
    else {
      exp.data_trials.push({
        "condition": exp.condition,
        "trial_num": i + 1,
        "context": exp.examples[i].context,
        "contextWithSuper": exp.pronoun ? exp.pronoun : exp.examples[i].contextWithSuper,
        "contextWithSuperPronoun": exp.pronoun ? (exp.pronoun.search("He") != -1 ? "He" : "She") : "",
        "target": exp.examples[i].target,
        "degree": exp.examples[i].degree,
        "form": exp.examples[i].form,
        "adjective": adjective,
        "strength": exp.examples[i].strength,
        "names": exp.names[i],
        "gender": getGender(exp.names[i]),
        "sub_category": exp.examples[i].sub_singular,
        "super_category": exp.examples[i].super,
        "paraphrase0": exp.sliderOrder[0],
        "paraphrase1": exp.sliderOrder[1],
        "sub_endorsement": subEndorse,
        "super_endorsement": superEndorse
      });
      i++;
      exp.go();
    }
  }

  // stitches together all of the trial slides
  for (var j = 1; j <= exp.trials; j++) {
    slides["trial" + j] = slide({
      name: "trial" + j,
      start: start,
      button: button
    });
  }

  slides.subj_info =  slide({
    name : "subj_info",
    submit : function(e) {
      //if (e.preventDefault) e.preventDefault(); // I don't know what this means.
      exp.subj_data = {
        language: $("#language").val(),
        enjoyment: $("#enjoyment").val(),
        asses: $('input[name="assess"]:checked').val(),
        age: $("#age").val(),
        gender: $("#gender").val(),
        education: $("#education").val(),
        problems: $("#problems").val(),
        fairprice: $("#fairprice").val(),
        comments: $("#comments").val()
      };
      exp.go(); // use exp.go() if and only if there is no "present" data
    }
  });

  slides.thanks = slide({
    name: "thanks",
    start: function() {
      exp.data = {
          "trials": exp.data_trials,
          "catch_trials": exp.catch_trials,
          "system": exp.system,
          "condition": exp.condition,
          "paraphrase0": exp.sliderOrder[0],
          "paraphrase1": exp.sliderOrder[1],
          "subject_information": exp.subj_data,
          "time_in_minutes": (Date.now() - exp.startT) / 60000
      };
      setTimeout(function() {turk.submit(exp.data);}, 1000);
    }
  });
  return slides;
}

/// init ///
function init() {

  repeatWorker = false;
  (function(){
      var ut_id = "mht-adjectives-20170115-cce";
      if (UTWorkerLimitReached(ut_id)) {
        $('.slide').empty();
        repeatWorker = true;
        alert("You have already completed the maximum number of HITs allowed by this requester. Please click 'Return HIT' to avoid any impact on your approval rating.");
      }
  })();

  // generate all possible target-context pair combinations
  exp.examples = getUniqueTrials(examples);

  // one trial for each unique target-context pair
  exp.trials = exp.examples.length;
  $(".display_trials").html(exp.trials);

  // sample a phrase for this particular instance
  exp.condition = sampleCondition();

  // set the number of sliders to use and their order
  exp.sliderOrder = _.shuffle(["sub_plural", "super"]);
  exp.nSentences = exp.sliderOrder.length;

  // if we have more trials than we do unique names, some names will be reused
  if (exp.trials > characters.length) {
    // this needs to be fixed later to account for the possibility of two names on the same trial slide
    exp.names = sampleNames(characters).concat(sampleNames(characters));
    exp.extra = sampleNames(characters);
  } else {
    // generate a list of unique names
    exp.names = sampleNames(characters);

    // names for the trials that require an extra name
    exp.extra = exp.names.slice(exp.trials, exp.names.length);
  }

  // stores the catch trial results for this experiment
  exp.nCatch = 2;
  exp.catch_trials = [];

  // get user system specs
  exp.system = {
      Browser: BrowserDetect.browser,
      OS: BrowserDetect.OS,
      screenH: screen.height,
      screenUH: exp.height,
      screenW: screen.width,
      screenUW: exp.width
  };

  // the blocks of the experiment
  exp.structure = ["i0", "instructions"];
  // for (var k = 1; k <= exp.trials; k++) {
  for (var k = 1; k <= 2; k++) {
    exp.structure.push("trial" + k);
  }
  exp.structure.push("subj_info");
  exp.structure.push("thanks");

  // holds the data from each trial
  exp.data_trials = [];

  // make corresponding slides
  exp.slides = makeSlides(exp);

  // embed the slides
  embedCE2Slides(exp.trials);

  // this does not work if there are stacks of stims (but does work for an experiment with this structure)
  // relies on structure and slides being defined
  exp.nQs = utils.get_exp_length();

  // hide everything
  $(".slide").hide();

  // make sure Turkers have accepted HIT (or you're not in MTurk)
  $("#start_button").click(function() {
    if (turk.previewMode) {
      $("#mustaccept").show();
    } else {
      $("#start_button").click(function() { $("#mustaccept").show(); });
      exp.go();
    }
  });

  // show first slide
  exp.go();
}
