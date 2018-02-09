var j = 0;

function make_slides(f) {
    var slides = {};

    slides.i0 = slide({
        name: "i0",
        start: function() {
            exp.startT = Date.now();
        }
    });

    // Setup the catch trial.
    slides.instructions = slide({
        name: "instructions",
        start: function() {
            $(".catch_err").hide();
            var catch_sentence = ["How likely is it that the gardener thought %NAME% wanted bananas?", 
                                  "How likely is it that the gardener thought %NAME% wanted pears?"];
            for (var i = 0; i < exp.num_catch; i++) {
                $("#multi_slider_table0").append("<tr class=\"slider_row\"><td class=\"slider_target\" id=\"sentence" + i + 
                                                 "\">" + catch_sentence[i] + "</td><td colspan=\"2\"><div id=\"slider" + i + 
                                                 "\" class=\"slider\">-------[ ]--------</div></td></tr>");
                utils.match_row_height("#multi_slider_table0", ".slider_target");
                utils.make_slider("#slider" + i, make_slider_callback(i));
            }
            exp.sliderPost = [];
        },
        button: function() {
            if ((exp.sliderPost[0] === undefined) || (exp.sliderPost[1] === undefined)) {
                $(".catch_err").show(); 
            }
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

    // Set up a trial slide.
    function start() {
        // Hide any errors and sliders from the previous slide.
        $(".err").hide();
        $(".slider_row").remove();

        // Display the setup, stimulus, and prompt on the slide.
        $(".display_setup").html("Suppose the farmer takes the following action.");
        $(".display_stimulus").html("<img style=\"height:350px;width:350px;\" src=\"../imgs/stimuli/" + 
                                    exp.trials[j] + "\"></script>");
    
        sentence1 = "How much did the farmer think %NAME% wanted this fruit?"
        sentence2 = "Do you think the farmer was anticipating that %NAME% would thinking about it's potential actions?"

        // set up the text next to each slider
        for (var i = exp.num_catch; i < exp.num_sentences+exp.num_catch; i++) {
            // display the slider for each slide
            sentence = i == 2 ? sentence1 : sentence2
            $("#multi_slider_table" + (j+1)).append("<tr class=\"slider_row\"><td class=\"slider_target\" id=\"sentence" + i + 
                                                    "\">" + sentence + "</td><td colspan=\"2\"><div id=\"slider" + i + 
                                                    "\" class=\"slider\">-------[ ]--------</div></td></tr>");
            utils.match_row_height("#multi_slider_table" + (j+1), ".slider_target");
            utils.make_slider("#slider" + i, make_slider_callback(i));
        }

        // init_sliders(exp.num_sentences);
        exp.sliderPost = [];
    }

    // These two functions help set up and read info from the sliders.
    // function init_sliders(num_sentences) {
    //     for (var i = exp.num_catch; i < num_sentences+exp.num_catch; i++) {
    //         utils.make_slider("#slider" + i, make_slider_callback(i));
    //     }
    // }

    function make_slider_callback(i) {
        return function(event, ui) {
            exp.sliderPost[i] = ui.value;
        };
    }

    // runs when the "Continue" button is hit on a slide
    function button() {

        if ((exp.sliderPost[2] === undefined) || (exp.sliderPost[3] === undefined)) { 
            $(".err").show(); 
        }
        else {
            exp.data_trials.push({
                "trial_num": j + 1,
                "stimulus": exp.trials[j],
                "target0": exp.sliderPost[2],
                "target1": exp.sliderPost[3]
            });
            j++;
            exp.go();
        }
    }

    // stitches together all of the trial slides
    for (var i = 1; i <= exp.num_trials; i++) {
        slides["trial" + i] = slide({
            name: "trial" + i,
            start: start,
            button: button
        });
    }

    slides.subj_info =  slide({
        name: "subj_info",
        submit: function(e) {
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
            exp.go();
        }
    });

    slides.thanks = slide({
        name: "thanks",
        start: function() {
            exp.data = {
                "trials": exp.data_trials,
                "catch_trials": exp.catch_trials,
                "system": exp.system,
                "subject_information": exp.subj_data,
                "time_in_minutes": (Date.now() - exp.startT) / 60000
            };
            setTimeout(function() {turk.submit(exp.data);}, 1000);
        }
    });

    return slides;
}

function init() {

    repeatWorker = false;
    (function() {
        // How do I get my own ut_id?
        var ut_id = "mht-adjectives-20170115-cce";
        if (UTWorkerLimitReached(ut_id)) {
            $('.slide').empty();
            repeatWorker = true;
            alert("You have already completed the maximum number of HITs allowed by this requester. Please click 'Return HIT' to avoid any impact on your approval rating.");
        }
    })();

    exp.num_catch = 2;
    exp.catch_trials = [];

    exp.trials = trials();
    exp.num_trials = exp.trials.length;
    $(".display_trials").html(exp.num_trials);

  exp.num_sentences = 2
  // sample a phrase for this particular instance
  // exp.condition = sampleCondition();

  // stores the catch trial results for this experiment


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
  for (var k = 1; k <= exp.num_trials; k++) {
  // for (var k = 1; k <= 4; k++) {
    exp.structure.push("trial" + k);
  }
  exp.structure.push("subj_info");
  exp.structure.push("thanks");

  // holds the data from each trial
  exp.data_trials = [];

  // make corresponding slides
  exp.slides = make_slides(exp);

  // embed the slides
  embed_slides(exp.num_trials);

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
