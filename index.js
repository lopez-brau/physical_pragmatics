var j = 0;

function make_slides(f) {
    var slides = {};

    slides.i0 = slide({
        name: "i0",
        start: function() {
            exp.startT = Date.now();
            $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
        }
    });

    // Set up the instructions slide.
    slides.instructions = slide({
        name: "instructions",
        start: function() { $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%"); },
        button: function() { exp.go(); }
    });

    // Set up the catch trial slide.
    slides.catch_trial = slide({
        name: "catch_trial",
        start: function() {
            // Display the progress bar and remove any previous error messages.
            $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
            $(".catch_error").hide();

            // Set up the catch trial prompt and display it along with the options.
            exp.catch_prompt = "What is the only difference between the two exits?";
            $(".display_catch").html("<p>" + exp.catch_prompt + "</p>" +
                                     "<p>" +
                                     "<label><input type=\"checkbox\" name=\"response_0\" value=\"0\"/>color of the door  </label>" +
                                     "<label><input type=\"checkbox\" name=\"response_1\" value=\"1\"/>amount of lighting  </label>" +
                                     "<label><input type=\"checkbox\" name=\"response_2\" value=\"2\"/>the " + exp.object + "  </label>" +
                                     "<label><input type=\"checkbox\" name=\"response_3\" value=\"3\"/>not sure  </label>" +
                                     "</p>");
        },
        button: function() {
            // Record the responses.
            exp.catch_response_0 = ($("input[name='response_0']:checked").val() == "0") ? 1 : 0;
            exp.catch_response_1 = ($("input[name='response_1']:checked").val() == "1") ? 1 : 0;
            exp.catch_response_2 = ($("input[name='response_2']:checked").val() == "2") ? 1 : 0;
            exp.catch_response_3 = ($("input[name='response_3']:checked").val() == "3") ? 1 : 0;

            // Triggers if the participant fails to answer the question.
            if (exp.catch_response_0 + exp.catch_response_1 + exp.catch_response_2 + exp.catch_response_3 == 0) {
                $(".catch_error").show();
            }

            // Triggers if the participant fails to answer the question correctly.
            else if ((exp.catch_response_0 == 1) || (exp.catch_response_1 == 1) || (exp.catch_response_2 == 0) || (exp.catch_response_3 == 1)) {
                $(".catch_error").hide();
                exp.go(-1);
            }
            else {
                exp.go();
            }
        }
    });

    // Set up the transition slide.
    slides.transition = slide({
        name: "transition",
        start: function() { $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%"); },
        button: function() { exp.go(); }
    });

    // Set up a trial slide.
    function start() {
        // Display the progress bar and remove any previous error messages.
        $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
        $(".error").hide();

        // Display the prompt, stimuli, and the options.
        if ((j+1) == 1) {
            $(".display_prompt").html("What do you think someone was trying to tell you about the door with the " + exp.object + "?");
            $(".display_stimulus").html("<div align=\"center\">" +
                                        "<div style=\"display:inline-block;vertical-align:top;margin-right:-20px;margin-bottom:-30px;\">" +
                                        "<img style=\"height:300px;width:auto;\" src=\"stimuli/symbols_0/" +
                                        exp.trials[j][0] + "\"></img>" + 
                                        "<br><br>" +
                                        "<p style=\"margin-right:20px;\"></p>" +
                                        "</label>" + 
                                        "</div>" + 
                                        "<div style=\"display:inline-block;vertical-align:top;margin-left:-20px;margin-bottom:-30px;\">" +
                                        "<label>" + 
                                        "<img style=\"height:300px;width:auto;\" src=\"stimuli/symbols_0/" +
                                        exp.trials[j][1] + "\"></img>" +
                                        "<br><br>" + 
                                        "</label>" +
                                        "</div>" + 
                                        "</div>" + 
                                        "<div style=\"width:60%;margin-left:auto;margin-right:auto;\" align=\"center\">" + 
                                        "<p align=\"left\"><label><input type=\"radio\" name=\"target\" value=\"0\">" +
                                        "You <b>should</b> walk through the door with the " + exp.object + 
                                        "</label></p>" +
                                        "<p align=\"left\"><label><input type=\"radio\" name=\"target\" value=\"1\">" +
                                        "You <b>should not</b> walk through the door with the " + exp.object +
                                        "</label></p>" +
                                        "</div>");
        else if ((j+1) == 2) {
            $(".display_prompt").html("What do you think someone was trying to tell you about the door with the picture?");
            $(".display_stimulus").html("<div align=\"center\">" +
                                        "<div style=\"display:inline-block;vertical-align:top;margin-right:-20px;margin-bottom:-30px;\">" +
                                        "<img style=\"height:300px;width:auto;\" src=\"stimuli/symbols_0/" +
                                        exp.trials[j][0] + "\"></img>" + 
                                        "<br><br>" +
                                        "<p style=\"margin-right:20px;\"></p>" +
                                        "</label>" + 
                                        "</div>" + 
                                        "<div style=\"display:inline-block;vertical-align:top;margin-left:-20px;margin-bottom:-30px;\">" +
                                        "<label>" + 
                                        "<img style=\"height:300px;width:auto;\" src=\"stimuli/symbols_0/" +
                                        exp.trials[j][1] + "\"></img>" +
                                        "<br><br>" + 
                                        "</label>" +
                                        "</div>" + 
                                        "</div>" + 
                                        "<div style=\"width:60%;margin-left:auto;margin-right:auto;\" align=\"center\">" + 
                                        "<p align=\"left\"><label><input type=\"radio\" name=\"target\" value=\"0\">" +
                                        "You <b>should</b> walk through the door with the picture</label></p>" +
                                        "<p align=\"left\"><label><input type=\"radio\" name=\"target\" value=\"1\">" +
                                        "You <b>should not</b> walk through the door with the picture</label></p>" +
                                        "</div>");
        }
    }

    // Run when the "Continue" button is hit on a slide.
    function button() {
        if ($("input[name='target']:checked").val() == undefined) { 
            $(".error").show(); 
        }
        else {
            exp.data_trials.push({
                "trial_num": j + 1,
                "left": exp.trials[j][0],
                "right": exp.trials[j][1],
                "target": $("input[name='target']:checked").val()
            });
            j++;
            exp.go();
        }
    }

    // Stitches together all of the trial slides.
    for (var i = 1; i <= exp.num_trials; i++) {
        slides["trial_" + i] = slide({
            name: "trial_" + i,
            start: start,
            button: button
        });
    }

    slides.subj_info = slide({
        name: "subj_info",
        start: function() { $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%"); },
        submit: function(e) {
            exp.subj_data = {
                "language": $("#language").val(),
                "enjoyment": $("#enjoyment").val(),
                "asses": $("input[name='assess']:checked").val(),
                "age": $("#age").val(),
                "gender": $("#gender").val(),
                "education": $("#education").val(),
                "problems": $("#problems").val(),
                "fairprice": $("#fairprice").val(),
                "comments": $("#comments").val()
            };
            exp.go();
        }
    });

    slides.thanks = slide({
        name: "thanks",
        start: function() {
            $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
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

    // Set up the payment amount and Unique Turker.
    $(".display_payment").html("$0.10");
    repeatWorker = false;
    (function() {
        var ut_id = "malb_social_pragmatics_12-30-2018_symbols_0";
        if (UTWorkerLimitReached(ut_id)) {
            $(".slide").empty();
            repeatWorker = true;
            alert("You have already completed the maximum number of HITs allowed by this requester. " +
                  "Please click 'Return HIT' to avoid any impact on your approval rating.");
        }
    })();

    // Select whether the doors are open or closed.
    exp.doors = "open";

    // Select whether the modified door has a low-cost object or a symbol in front of it.
    exp.condition = "low";

    // Select which side the modified door is on.
    exp.side = "left";

    // Select which object is being used for the low cost and the symbol.
    exp.object = "plant";
    $(".display_stimuli").html(exp.object);
    $(".display_stimuli_phrase_0").html(get_noun_phrase_0(exp.object));
    $(".display_stimuli_phrase_1").html(get_noun_phrase_1(exp.object));

    // Set up a container for the catch trial information.
    exp.catch_trials = [];

    // Set up trial slide information.
    exp.trials = trials(exp.doors, exp.condition, exp.side, exp.object);
    exp.num_trials = exp.trials.length;
    exp.data_trials = [];
    $(".display_num_trials").html(exp.num_trials);

    // Get user system specs.
    exp.system = {
        Browser: BrowserDetect.browser,
        OS: BrowserDetect.OS,
        screenH: screen.height,
        screenUH: exp.height,
        screenW: screen.width,
        screenUW: exp.width
    };

    // Stich together the blocks of the experiment.
    exp.structure = ["i0", "instructions", "catch_trial", "trial_1", "transition", "trial_2"];
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
        }
        else {
            $("#start_button").click(function() { $("#mustaccept").show(); });
            exp.go();
        }
    });

    // Launch the slides.
    exp.go();
}
