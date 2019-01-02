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

    // Set up the context slide.
    slides.context = slide({
        name: "context",
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
                                     "<label><input type=\"checkbox\" name=\"catch_0\" value=\"0\"/>" + 
                                     "color of the door  </label>" +
                                     "<label><input type=\"checkbox\" name=\"catch_1\" value=\"1\"/>" + 
                                     "amount of lighting  </label>" +
                                     "<label><input type=\"checkbox\" name=\"catch_2\" value=\"2\"/>" +
                                     "the " + exp.object + "  </label>" +
                                     "<label><input type=\"checkbox\" name=\"catch_3\" value=\"3\"/>" +
                                     "not sure  </label>" +
                                     "</p>");
        },
        button: function() {
            // Record the responses.
            exp.catch_response_0 = ($("input[name='catch_0']:checked").val() == "0") ? 1 : 0;
            exp.catch_response_1 = ($("input[name='catch_1']:checked").val() == "1") ? 1 : 0;
            exp.catch_response_2 = ($("input[name='catch_2']:checked").val() == "2") ? 1 : 0;
            exp.catch_response_3 = ($("input[name='catch_3']:checked").val() == "3") ? 1 : 0;

            // Triggers if the participant fails to answer the question.
            if (exp.catch_response_0 + exp.catch_response_1 + exp.catch_response_2 + exp.catch_response_3 == 0) {
                $(".catch_error").show();
            }

            // Triggers if the participant fails to answer the question correctly.
            else if ((exp.catch_response_0 == 1) || (exp.catch_response_1 == 1) || (exp.catch_response_2 == 0) || 
                     (exp.catch_response_3 == 1)) {
                $(".catch_error").hide();
                exp.go(-1);
            }
            else {
                exp.go();
            }
        }
    });

    // Set up a trial slide.
    function trial_start() {
        // Display the progress bar and remove any previous error messages.
        $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
        $(".trial_error").hide();

        // Display the prompt, stimuli, and the options.
        $(".display_trial").html("What do you think someone was trying to tell you about the door with the " +
                                 exp.object + "?" +
                                 "<div align=\"center\">" +
                                 "<div style=\"display:inline-block;vertical-align:top;margin-right:-20px;" + 
                                 "margin-bottom:-30px;\">" +
                                 "<img style=\"height:300px;width:auto;\" src=\"../stimuli/actor_0/" +
                                 exp.trials[j][0] + "\"></img>" + 
                                 "<br><br>" +
                                 "<p style=\"margin-right:20px;\"></p>" +
                                 "</label>" + 
                                 "</div>" + 
                                 "<div style=\"display:inline-block;vertical-align:top;margin-left:-20px;" + 
                                 "margin-bottom:-30px;\">" +
                                 "<label>" + 
                                 "<img style=\"height:300px;width:auto;\" src=\"../stimuli/actor_0/" +
                                 exp.trials[j][1] + "\"></img>" +
                                 "<br><br>" + 
                                 "</label>" +
                                 "</div>" + 
                                 "</div>" + 
                                 "<div style=\"width:70%;margin-left:auto;margin-right:auto;\" align=\"center\">" + 
                                 "<p align=\"left\"><label><input type=\"radio\" name=\"target\" value=\"0\">" +
                                 "You <b>should</b> walk through the door with the " + exp.object + 
                                 "</label></p>" +
                                 "<p align=\"left\"><label><input type=\"radio\" name=\"target\" value=\"1\">" +
                                 "You <b>should not</b> walk through the door with the " + exp.object +
                                 "</label></p>" +
                                 "</div>");
    }

    // Run when the "Continue" button is hit on a trial slide.
    function trial_button() {
        if ($("input[name='target']:checked").val() == undefined) { 
            $(".error").show(); 
        }
        else {
            exp.data_trials.push({
                "trial_num": j + 1,
                "left_door": exp.trials[j][0],
                "right_door": exp.trials[j][1],
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
            start: trial_start,
            button: trial_button
        });
    }

    // Set up the first exclusion slide.
    function exclusion_start_1() {
        // Display the progress bar and remove any previous error messages.
        $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
        $(".exclusion_error").hide();

        // Display the prompt, stimuli, and the options.
        $(".display_exclusion").html("Which door requires more work to walk through?" + 
                                     "<div align=\"center\">" +
                                     "<div style=\"display:inline-block;vertical-align:top;margin-right:-20px;" + 
                                     "margin-bottom:-30px;\">" +
                                     "<img style=\"height:300px;width:auto;\" src=\"../stimuli/actor_0/" +
                                     exp.trials[j-exp.num_trials][0] + "\"></img>" + 
                                     "<br><br>" +
                                     "<p style=\"margin-right:20px;\"></p>" +
                                     "</label>" + 
                                     "</div>" + 
                                     "<div style=\"display:inline-block;vertical-align:top;margin-left:-20px;" + 
                                     "margin-bottom:-30px;\">" +
                                     "<label>" + 
                                     "<img style=\"height:300px;width:auto;\" src=\"../stimuli/actor_0/" +
                                     exp.trials[j-exp.num_trials][1] + "\"></img>" +
                                     "<br><br>" + 
                                     "</label>" +
                                     "</div>" + 
                                     "</div>" + 
                                     "<div style=\"width:40%;margin-left:auto;margin-right:auto;\" align=\"center\">" + 
                                     "<p align=\"left\"><label><input type=\"radio\" name=\"exclusion\" value=\"0\">" +
                                     "The door on the left.</label></p>" +
                                     "<p align=\"left\"><label><input type=\"radio\" name=\"exclusion\" value=\"1\">" +
                                     "The door on the right.</label></p>" +
                                     "<p align=\"left\"><label><input type=\"radio\" name=\"exclusion\" value=\"2\">" +
                                     "Equally easy.</label></p>" +
                                     "</div>");
    }

    function exclusion_button_1() {
        if ($("input[name='exclusion']:checked").val() == undefined) { 
            $(".exclusion_error").show(); 
        }
        else {
            exp.data_trials.push({
                "exclusion_num": (j-exp.num_trials) + 1,
                "left_door": exp.trials[j-exp.num_trials][0],
                "right_door": exp.trials[j-exp.num_trials][1],
                "target": $("input[name='exclusion']:checked").val()
            });
            j++;
            exp.go();
        }
    }

    // Set up the second exclusion slide.
    function exclusion_start_2() {
        // Display the progress bar and remove any previous error messages.
        $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
        $(".exclusion_error").hide();

        // Display the prompt, stimuli, and the options.
        $(".display_exclusion").html("Do you think you would be able to walk through this door if you wanted to?" + 
                                     "<div align=\"center\">" +
                                     "<div style=\"display:inline-block;vertical-align:top;margin-right:-20px;" + 
                                     "margin-bottom:-30px;\">" +
                                     "<img style=\"height:300px;width:auto;\" src=\"../stimuli/actor_0/" +
                                     exp.trials[(j-1)-exp.num_trials][0] + "\"></img>" + 
                                     "<br><br>" +
                                     "<p style=\"margin-right:20px;\"></p>" +
                                     "</label>" + 
                                     "</div>" + 
                                     "<div style=\"display:inline-block;vertical-align:top;margin-left:-20px;" + 
                                     "margin-bottom:-30px;\">" +
                                     "<label>" + 
                                     "<img style=\"height:300px;width:auto;\" src=\"../stimuli/actor_0/" +
                                     exp.trials[(j-1)-exp.num_trials][1] + "\"></img>" +
                                     "<br><br>" + 
                                     "</label>" +
                                     "</div>" + 
                                     "</div>" + 
                                     "<div style=\"width:20%;margin-left:auto;margin-right:auto;\" align=\"center\">" + 
                                     "<p align=\"left\"><label><input type=\"radio\" name=\"exclusion\" value=\"0\">" +
                                     "Yes.</label></p>" +
                                     "<p align=\"left\"><label><input type=\"radio\" name=\"exclusion\" value=\"1\">" +
                                     "No.</label></p>" +
                                     "</div>");
    }

    function exclusion_button_2() {
        if ($("input[name='exclusion']:checked").val() == undefined) { 
            $(".exclusion_error").show(); 
        }
        else {
            exp.data_trials.push({
                "exclusion_num": (j-exp.num_trials) + 1,
                "left_door": exp.trials[(j-1)-exp.num_trials][0],
                "right_door": exp.trials[(j-1)-exp.num_trials][1],
                "target": $("input[name='exclusion']:checked").val()
            });
            j++;
            exp.go();
        }
    }

    // Stitches together all of the exclusion slides.
    for (var i = 1; i <= 2; i++) {
        slides["exclusion_" + i] = slide({
            name: "exclusion_" + i,
            start: (i == 1) ? exclusion_start_1 : exclusion_start_2 ,
            button: (i == 1) ? exclusion_button_1 : exclusion_button_2
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
                "setup": exp.setup,
                "trials": exp.data_trials,
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
    $(".display_payment").html("$0.30");
    repeatWorker = false;
    (function() {
        var ut_id = "lopez-brau_social_pragmatics_actor";
        if (UTWorkerLimitReached(ut_id)) {
            $(".slide").empty();
            repeatWorker = true;
            alert("You have already completed the maximum number of HITs allowed by this requester. " +
                  "Please click 'Return HIT' to avoid any impact on your approval rating.");
        }
    })();

    // Select whether the modified door has an object in front of it that incurs a low cost or no cost.
    exp.condition = "low";

    // Select which side the modified door is on.
    exp.side = _.sample(["left", "right"]);

    // Select which object is being used.
    exp.object = "plant";
    $(".display_stimuli_phrase_0").html(get_noun_phrase_0(exp.object));
    $(".display_stimuli_phrase_1").html(get_noun_phrase_1(exp.object));

    // Select whether the doors are open or closed.
    exp.doors = {
        "plant": "closed",
        "chair": "open",
        "books": "open",
        "cinderblocks": "open",
        "tape": "closed",
        "rulers": "open",
        "hat": "closed",
        "fishbowl": "closed"
    }[exp.object];

    // Store the experiment variables.
    exp.setup = {
        "condition": exp.condition,
        "side": exp.side,
        "object": exp.object,
        "doors": exp.doors
    };

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
    exp.structure = ["i0", "context", "catch_trial", "trial_1", "exclusion_1", "exclusion_2"];
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
