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

    // More questions.
    slides["trial2"] = slide({
        name: "trial2",
        start: function() {
            $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
            $(".error").hide();

            $(".display_setup").html("What do you think someone was trying to tell you about the door with the " + exp.object + "?");

            $(".display_stimulus").html(//"<br><br>" 
                                        "<div align=\"center\">" +
                                        // "<div style=\"display:inline-block;vertical-align:top;margin-right:-20px;\">" +
                                        // "<img style=\"-webkit-transform:rotate(90deg);height:200px;width:auto;\" src=\"imgs/agent_1/" + 
                                        "<div style=\"display:inline-block;vertical-align:top;margin-left:40px\">" +
                                        "<img style=\"height:300px;width:auto;\" src=\"imgs/agent_1/" +
                                        exp.trials[0][0] + "\"></img>" + 
                                        // "<br><br>" +
                                        "</div>" + 
                                        // "<div style=\"display:inline-block;vertical-align:top;margin-left:-20px;\">" +
                                        // "<img style=\"-webkit-transform:rotate(90deg);height:200px;width:auto;\" src=\"imgs/agent_1/" + 
                                        "<div style=\"display:inline-block;vertical-align:top;margin-left:60px;\">" +
                                        "<img style=\"height:300px;width:auto;\" src=\"imgs/agent_1/" +
                                        exp.trials[0][1] + "\"></img>" +
                                        // "<br><br>" + 
                                        "</div>" + 
                                        "</div>" + 
                                        "<div>" + 
                                        "<p style=\"text-align:left;text-indent:140px;\">Could you walk through the door with the " + 
                                        exp.object + " if you wanted to?</p>" +
                                        "<label><input type=\"radio\" name=\"target_1\" value=\"0\">Yes</label>" +
                                        "<label><input type=\"radio\" name=\"target_1\" value=\"1\">No</label>" +
                                        "<label><input type=\"radio\" name=\"target_1\" value=\"2\">Not Sure</label></p>" +
                                        "</div>");
        },
        button: function() {
            if ($("input[name='target_1']:checked").val() == undefined) { 
                $(".error").show(); 
            }
            else {
                exp.data_trials.push({
                    // "trial_num": j + 1,
                    // "left_door": exp.trials[0][0],
                    // "right_door": exp.trials[0][1],
                    "target_1": $("input[name='target_1']:checked").val()
                });
                j++;
                exp.go();
            }
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
            $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
            $(".catch_error_0").hide();

            var sentences = ["What is the only difference between the two exits?"];
            exp.sentence_0 = sentences[0];

            $(".display_catch_options").html("<p>" + exp.sentence_0 + "</p>" +
                                             "<p>" +
                                             "<label><input type=\"checkbox\" name=\"sentence_0_0\" value=\"0\"/>color of the door  </label>" +
                                             "<label><input type=\"checkbox\" name=\"sentence_0_1\" value=\"1\"/>amount of lighting  </label>" +
                                             "<label><input type=\"checkbox\" name=\"sentence_0_2\" value=\"2\"/>the " + exp.object + "  </label>" +
                                             "<label><input type=\"checkbox\" name=\"sentence_0_3\" value=\"3\"/>not sure  </label>" +
                                             "</p>");
        },
        button: function() {
            exp.target_0_0 = ($("input[name='sentence_0_0']:checked").val() == "0") ? 1 : 0;
            exp.target_0_1 = ($("input[name='sentence_0_1']:checked").val() == "1") ? 1 : 0;
            exp.target_0_2 = ($("input[name='sentence_0_2']:checked").val() == "2") ? 1 : 0;
            exp.target_0_3 = ($("input[name='sentence_0_3']:checked").val() == "3") ? 1 : 0;

            // Triggers if the participant fails to answer all of the questions.
            if (exp.target_0_0 + exp.target_0_1 + exp.target_0_2 + exp.target_0_3 == 0) {
                $(".catch_error_0").show();
            }

            // Triggers if the participant fails to answer the question correctly.
            else if ((exp.target_0_0 == 1) || (exp.target_0_1 == 1) || (exp.target_0_2 == 0) || (exp.target_0_3 == 1)) {
                $(".catch_error_0").hide();
                exp.go(-1);
            }
            else {
                exp.catch_trials.push({
                    "enforcer_name": exp.enforcer.name,
                    "enforcer_gender": exp.enforcer.gender,
                    "sentence_0": exp.sentence_0,
                    "target_0_0": exp.target_0_0,
                    "target_0_1": exp.target_0_1,
                    "target_0_2": exp.target_0_2,
                    "target_0_3": exp.target_0_3
                });
                exp.go();
            }
        }
    });

    // Set up a trial slide.
    function start() {
        $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
        $(".error").hide();

        $(".display_setup").html("What do you think someone was trying to tell you about the door with the " + exp.object + "?");

        $(".display_stimulus").html(//"<br><br>" 
                                    "<div align=\"center\">" +
                                    // "<div style=\"display:inline-block;vertical-align:top;margin-right:-20px;\">" +
                                    // "<img style=\"-webkit-transform:rotate(90deg);height:200px;width:auto;\" src=\"imgs/agent_1/" + 
                                    "<div style=\"display:inline-block;vertical-align:top;margin-left:40px\">" +
                                    "<img style=\"height:300px;width:auto;\" src=\"imgs/agent_1/" +
                                    exp.trials[0][0] + "\"></img>" + 
                                    // "<br><br>" +
                                    "</div>" + 
                                    // "<div style=\"display:inline-block;vertical-align:top;margin-left:-20px;\">" +
                                    // "<img style=\"-webkit-transform:rotate(90deg);height:200px;width:auto;\" src=\"imgs/agent_1/" + 
                                    "<div style=\"display:inline-block;vertical-align:top;margin-left:60px;\">" +
                                    "<img style=\"height:300px;width:auto;\" src=\"imgs/agent_1/" +
                                    exp.trials[0][1] + "\"></img>" +
                                    // "<br><br>" + 
                                    "</div>" + 
                                    "</div>" + 
                                    "<div>" + 
                                    "<p style=\"text-align:left;text-indent:130px;\"><label><input type=\"radio\" name=\"target_0\" value=\"0\">" +
                                    "You <b>should</b> walk through the door with the " + exp.object + 
                                    "</label></p>" +
                                    "<p style=\"text-align:left;text-indent:130px;\"><label><input type=\"radio\" name=\"target_0\" value=\"1\">" +
                                    "You <b>should not</b> walk through the door with the " + exp.object +
                                    "</label></p>" + 
                                    "</div>");
    }

    // Run when the "Continue" button is hit on a slide.
    function button() {
        if ($("input[name='target_0']:checked").val() == undefined) { 
            $(".error").show(); 
        }
        else {
            exp.data_trials.push({
                "trial_num": j + 1,
                "left_door": exp.trials[0][0],
                "right_door": exp.trials[0][1],
                "target_0": $("input[name='target_0']:checked").val()
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
        var ut_id = "malb_social_pragmatics_02-04-2018_agent_1";
        if (UTWorkerLimitReached(ut_id)) {
            $('.slide').empty();
            repeatWorker = true;
            alert("You have already completed the maximum number of HITs allowed by this requester. " +
                  "Please click 'Return HIT' to avoid any impact on your approval rating.");
        }
    })();

    // Sample a name for the enforcer and the agent along with appropriate
    // pronouns.
    exp.characters = get_characters(characters);
    exp.enforcer = exp.characters[0];
    $(".display_enforcer").html(exp.enforcer.name);
    $(".display_enforcer_pronoun_1").html(get_pronoun_1(exp.enforcer, false));
    $(".display_enforcer_pronoun_1_capitalized").html(get_pronoun_1(exp.enforcer, true));
    $(".display_enforcer_pronoun_2").html(get_pronoun_2(exp.enforcer, false));
    $(".display_enforcer_pronoun_2_capitalized").html(get_pronoun_2(exp.enforcer, true));
    $(".display_enforcer_pronoun_3").html(get_pronoun_3(exp.enforcer, false));
    $(".display_enforcer_pronoun_3_capitalized").html(get_pronoun_3(exp.enforcer, true));
    $(".display_enforcer_pronoun_4").html(get_pronoun_4(exp.enforcer, false));
    $(".display_enforcer_pronoun_4_capitalized").html(get_pronoun_4(exp.enforcer, true));

    // Select whether the door is open or closed.
    // exp.door = _.sample(["closed", "open"]);
    exp.door = "open";
    // exp.cost = _.sample(["low", "none"]);
    exp.cost = "low";
    // exp.object = _.sample(["chair", "plant"])
    exp.object = "plant";
    $(".display_object").html(exp.object);

    // Set up a container for the catch trial information.
    exp.catch_trials = [];

    // Set up trial slide information.
    exp.trials = trials(exp.door, exp.cost, exp.object);
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
    exp.structure = ["i0", "instructions", "catch_trial"];
    for (var k = 1; k <= exp.num_trials; k++) {
        exp.structure.push("trial" + k);
    }
    exp.structure.push("trial2");
    exp.structure.push("subj_info");
    exp.structure.push("thanks");
   
    // Make and embed the slides.
    exp.slides = make_slides(exp);
    embed_slides(exp.num_trials+1);

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
