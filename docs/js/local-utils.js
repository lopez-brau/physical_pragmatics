// Generates the order of trial slides.
function trials() {
    // Set up and shuffle the potential natural costs and potential enforcer actions.
    natural_costs = _.shuffle([[2, 2], [2, 3], [3, 2], [3, 3], [2, 4], [4, 2], [3, 4], [4, 3], [4, 4]])
    enforcer_actions = _.shuffle([[0, 0], [1, 0], [2, 0], [3, 0]])

    // Construct the filenames of the stimuli to use for each trial.
    trials = []
    for (var i = 0; i < natural_costs.length; i++) {
        for (var j = 0; j < enforcer_actions.length; j++) {
            trials.push("[" + natural_costs[i].join(" ") + "]_[" + enforcer_actions[j].join(" ") + "].png")
        }
    }

    return trials
}

// Embeds the trial slides.
function embed_slides(num_trials) {
    var slides = "";
    for (var i = 1; i <= num_trials; i++) {
        slides = slides + "<div class=\"slide\" id=\"trial" + i + "\">" + 
            "<p class=\"display_setup\"></p>" +
            "<p class=\"display_stimulus\"></p>" +
            "<table id=\"multi_slider_table" + i + "\"" + "class=\"slider_table\">" +
            "<tr><td></td>" +
            "<td class=\"left\">very unlikely</td>"+
            "<td class=\"right\">very likely</td>" +
            "</tr></table><p></p>" +
            "<button onclick=\"_s.button()\">Continue</button>" +
            "<p class=\"err\">Please adjust both sliders before continuing.</p>" +
            "</div>";
        $(".trial_slides").html(slides);
    }
}
