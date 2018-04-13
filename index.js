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

    // Set up the background slides.
    slides.background_1 = slide({
        name: "background_1",
        start: function() { $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%"); },
        button: function() { exp.go(); }
    });
    slides.background_2 = slide({
        name: "background_2",
        start: function() { $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%"); },
        button: function() { exp.go(); }
    });
    slides.background_3 = slide({
        name: "background_3",
        start: function() { $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%"); },
        button: function() { exp.go(); }
    });
    slides.background_4 = slide({
        name: "background_4",
        start: function() { $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%"); },
        button: function() { exp.go(); }
    });
    slides.background_5 = slide({
        name: "background_5",
        start: function() { $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%"); },
        button: function() { exp.go(); }
    });

    // Set up the instructions slides.
    slides.instructions_1 = slide({
        name: "instructions_1",
        start: function() { $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%"); },
        button: function() { exp.go(); }
    });
    slides.instructions_2 = slide({
        name: "instructions_2",
        start: function() { $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%"); },
        button: function() { exp.go(); }
    });

    // Set up the catch trial slide.
    slides.catch_trial = slide({
        name: "catch_trial",
        start: function() {
            $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
            $(".catch_err_1").hide();
            $(".catch_err_2").hide();

            var sentences = ["Which fruit does " + exp.enforcer.name + " want hikers to take?",
                             "Does " + exp.enforcer.name + " know which fruit each hiker prefers?",
                             "What is the maximum number of boulders " + exp.enforcer.name + " can place?",
                             "Do hikers try to be helpful or are they selfish?",
                             "What are the two features that make it harder for hikers to get to a fruit grove?"];
            exp.sentence_0 = sentences[0];
            exp.sentence_1 = sentences[1];
            exp.sentence_2 = sentences[2];
            exp.sentence_3 = sentences[3];
            exp.sentence_4 = sentences[4];

            $(".display_catch_options").html("<p>" + exp.sentence_0 + "</p><p>" +
                                             "<label><input type=\"radio\" name=\"sentence_0\" value=\"pears\"/>Pears</label>" +
                                             "<label><input type=\"radio\" name=\"sentence_0\" value=\"pomegranates\"/>Pomegranates</label>" + 
                                             "<label><input type=\"radio\" name=\"sentence_0\" value=\"Not sure\"/>Not sure</label>" +
                                             "</p><p>" + exp.sentence_1 + "</p><p>" +
                                             "<label><input type=\"radio\" name=\"sentence_1\" value=\"No\"/>No</label>" +
                                             "<label><input type=\"radio\" name=\"sentence_1\" value=\"Yes\"/>Yes</label>" +
                                             "<label><input type=\"radio\" name=\"sentence_1\" value=\"Not sure\"/>Not sure</label>" +
                                             "</p><p>" + exp.sentence_2 + "</p><p>" +
                                             "<label><input type=\"radio\" name=\"sentence_2\" value=\"3\"/>3</label>" +
                                             "<label><input type=\"radio\" name=\"sentence_2\" value=\"1\"/>1</label>" +
                                             "<label><input type=\"radio\" name=\"sentence_2\" value=\"2\"/>2</label>" +
                                             "<label><input type=\"radio\" name=\"sentence_2\" value=\"Not sure\"/>Not sure</label>" +
                                             "</p><p>" + exp.sentence_3 + "</p><p>" +
                                             "<label><input type=\"radio\" name=\"sentence_3\" value=\"Selfish\"/>Selfish</label>" +
                                             "<label><input type=\"radio\" name=\"sentence_3\" value=\"Helpful\"/>Helpful</label>" + 
                                             "<label><input type=\"radio\" name=\"sentence_3\" value=\"Not sure\"/>Not sure</label>" +
                                             "</p><p>" + exp.sentence_4 + "</p><p>" +
                                             "<label><input type=\"checkbox\" name=\"sentence_4_0\" value=\"Weather\"/>Weather  </label>" +
                                             "<label><input type=\"checkbox\" name=\"sentence_4_1\" value=\"Distance\"/>Distance from the grove  </label>" +
                                             "<label><input type=\"checkbox\" name=\"sentence_4_2\" value=\"Time of day\"/>Time of day  </label>" +
                                             "<label><input type=\"checkbox\" name=\"sentence_4_3\" value=\"Boulders\"/>Boulders  </label>" +
                                             "<label><input type=\"checkbox\" name=\"sentence_4_4\" value=\"Not sure\"/>Not sure  </label></p>");
        },
        button: function() {
            exp.target_0 = $("input[name='sentence_0']:checked").val();
            exp.target_1 = $("input[name='sentence_1']:checked").val();
            exp.target_2 = $("input[name='sentence_2']:checked").val();
            exp.target_3 = $("input[name='sentence_3']:checked").val();
            exp.target_4_0 = ($("input[name='sentence_4_0']:checked").val() == "Weather") ? 1 : 0;
            exp.target_4_1 = ($("input[name='sentence_4_1']:checked").val() == "Distance") ? 1 : 0;
            exp.target_4_2 = ($("input[name='sentence_4_2']:checked").val() == "Time of day") ? 1 : 0;
            exp.target_4_3 = ($("input[name='sentence_4_3']:checked").val() == "Boulders") ? 1 : 0;
            exp.target_4_4 = $("input[name='sentence_4_4']:checked").val();

            if ((exp.target_0 == undefined) || (exp.target_1 == undefined) || 
                (exp.target_2 == undefined) || (exp.target_3 == undefined) ||
                ((exp.target_4_0 + exp.target_4_1 + exp.target_4_2 + exp.target_4_3 == 0) && (exp.target_4_4 != "Not sure"))) {
                $(".catch_err_2").hide();
                $(".catch_err_1").show();
            }
            else if (((exp.target_4_0 + exp.target_4_1 + exp.target_4_2 + exp.target_4_3 != 2) && (exp.target_4_4 != "Not sure")) ||
                     ((exp.target_4_0 + exp.target_4_1 + exp.target_4_2 + exp.target_4_3 != 0) && (exp.target_4_4 == "Not sure"))) {
                $(".catch_err_1").hide();
                $(".catch_err_2").show();
            }
            else if ((exp.target_0 != exp.preferred_fruit) || (exp.target_1 != "Yes") || (exp.target_2 != "3") || 
                     (exp.target_3 != "Helpful") || (exp.target_4_1 != 1) || (exp.target_4_3 != 1)) {
                $(".catch_err_1").hide();
                $(".catch_err_2").hide();
                exp.go(-3);
            }
            else {
                exp.catch_trials.push({
                    "enforcer_name": exp.enforcer.name,
                    "enforcer_gender": exp.enforcer.gender,
                    "preferred_fruit": exp.preferred_fruit,
                    "not_preferred_fruit": exp.not_preferred_fruit,
                    "agent_coords": exp.trials[j].slice(0, 5),
                    "pear_coords": exp.trials[j].slice(6, 11),
                    "sentence_0": exp.sentence_0,
                    "target_0": exp.target_0,
                    "sentence_1": exp.sentence_1,
                    "target_1": exp.target_1,
                    "sentence_2": exp.sentence_2,
                    "target_2": exp.target_2,
                    "sentence_3": exp.sentence_3,
                    "target_3": exp.target_3,
                    "sentence_4": exp.sentence_4,
                    "target_4_0": exp.target_4_0,
                    "target_4_1": exp.target_4_1,
                    "target_4_2": exp.target_4_2,
                    "target_4_3": exp.target_4_3,
                    "target_4_4": exp.target_4_4
                });
                exp.go();
            }
        }
    });

    // Set up a trial slide.
    function start() {
        $(".display_progress").html((exp.slideIndex/exp.nQs*100).toPrecision(3) + "%");
        $(".err").hide();
        $(".slider_row").remove();

        $(".display_setup").html("Consider the following scenario. Remember to place yourself in " + exp.enforcer.name + 
                                 "'s (the farmer's) shoes.");
        $(".display_stimulus").html("<img style=\"height:300px;width:auto;\" src=\"imgs/observer_1/" + 
                                    exp.trials[j] + "\"></img>");
    
        exp.sentence_0 = "How much did " + exp.enforcer.name + " think that this hiker likes " + exp.preferred_fruit + "?"
        exp.sentence_1 = "How good did " + exp.enforcer.name + " expect this hiker to be at detecting that " + 
                         exp.enforcer_pronoun + " placed the rocks?"

        $("#multi_slider_table_0" + (j+1)).append("<tr class=\"slider_row\"><td class=\"slider_target\" id=\"sentence_0" + 
                                                "\">" + exp.sentence_0 + "</td><td colspan=\"2\"><div id=\"slider_0" + 
                                                "\" class=\"slider\">-------[ ]--------</div></td></tr>");
        $("#multi_slider_table_1" + (j+1)).append("<tr class=\"slider_row\"><td class=\"slider_target\" id=\"sentence_1" + 
                                                "\">" + exp.sentence_1 + "</td><td colspan=\"2\"><div id=\"slider_1" + 
                                                "\" class=\"slider\">-------[ ]--------</div></td></tr>");
        utils.match_row_height("#multi_slider_table_0" + (j+1), ".slider_target");
        utils.match_row_height("#multi_slider_table_1" + (j+1), ".slider_target");
        utils.make_slider("#slider_0", make_slider_callback(0));
        utils.make_slider("#slider_1", make_slider_callback(1));

        exp.sliderPost = [];
    }

    // Run when the "Continue" button is hit on a slide.
    function button() {
        if ((exp.sliderPost[0] === undefined) || (exp.sliderPost[1] === undefined)) { 
            $(".err").show(); 
        }
        else {
            exp.data_trials.push({
                "trial_num": j + 1,
                "filename": exp.trials[j].slice(12),
                "sentence_0": exp.sentence_0,
                "target_0": exp.sliderPost[0],
                "sentence_1": exp.sentence_1,
                "target_1": exp.sliderPost[1]
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
    $(".display_payment").html("$1.00");
    repeatWorker = false;
    (function() {
        var ut_id = "malb_social_pragmatics_02-04-2018_observer_1";
        if (UTWorkerLimitReached(ut_id)) {
            $('.slide').empty();
            repeatWorker = true;
            alert("You have already completed the maximum number of HITs allowed by this requester. Please click 'Return HIT' to avoid any impact on your approval rating.");
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
    exp.enforcer_pronoun = get_pronoun_1(exp.enforcer, false);

    // Set up the fruit that the enforcer prefers the agent takes.
    // exp.fruit = _.shuffle(["pears", "pomegranates"]);
    // exp.preferred_fruit = exp.fruit[0];
    // exp.not_preferred_fruit = exp.fruit[1];
    exp.preferred_fruit = "pears";
    exp.not_preferred_fruit = "pomegranates";
    $(".display_preferred_fruit").html(exp.preferred_fruit);
    $(".display_not_preferred_fruit").html(exp.not_preferred_fruit);
    $(".display_not_preferred_fruit_singular").html(exp.not_preferred_fruit.slice(0, exp.not_preferred_fruit.length-1));

    // Set up a container for the catch trial information.
    exp.catch_trials = [];

    // Set up trial slide information.
    exp.pear_position = exp.preferred_fruit == "pears" ? 1 : 0;
    exp.trials = trials(exp.pear_position).slice(0, 18);
    exp.num_trials = exp.trials.length;
    exp.data_trials = [];
    $(".display_trials").html(exp.num_trials);

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
    exp.structure = ["i0", "background_1", "background_2", "background_3", "background_4", 
                     "background_5", "instructions_1", "instructions_2", "catch_trial"];
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
        }
        else {
            $("#start_button").click(function() { $("#mustaccept").show(); });
            exp.go();
        }
    });

    // Launch the slides.
    exp.go();
}
