// Generates the trial slides.
function trials(pear_position) {
    // Sample agent and pear coordinates.
    var agent_coords = _.sample(["[0.5 0.5]", "[7.5 0.5]", "[7.5 7.5]", "[0.5 7.5]"]);
    var pear_coords = {
        "[0.5 0.5]": ["[6.5 0.5]", "[0.5 6.5]"],
        "[7.5 0.5]": ["[6.5 6.5]", "[0.5 0.5]"],
        "[7.5 7.5]": ["[0.5 6.5]", "[6.5 0.5]"],
        "[0.5 7.5]": ["[0.5 0.5]", "[6.5 6.5]"]
    }[agent_coords][parseInt(pear_position)];

    // Construct a randomized list of stimuli.
    var trials = [];
    var natural_costs = [[4, 4], [4, 5], [4, 6], [5, 4], [5, 5], [5, 6], [6, 4], [6, 5], [6, 6]];
    var enforcer_actions = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]];
    for (var i = 0; i < natural_costs.length; i++) {
        for (var j = 0; j < enforcer_actions.length; j++) {
            filepath = agent_coords + "/" + pear_coords + "/[" + natural_costs[i].join(" ") + "]_[" + 
                        enforcer_actions[j].join(" ") + "].png";
            trials.push(filepath);
        }
    }

    return _.shuffle(trials);
}

// Embeds the trial slides.
function embed_slides(num_trials) {
    var slides = "";
    for (var i = 1; i <= num_trials; i++) {
        slides = slides + "<div class=\"slide\" id=\"trial" + i + "\">" + 
            "<p class=\"display_setup\"></p>" +
            "<p class=\"display_stimulus\"></p>" +
            "<table style=\"margin-right:0px\"id=\"multi_slider_table_0" + i + "\"" + "class=\"slider_table\">" +
            "<tr><td></td>" +
            "<td class=\"left\">not at all</td>" +
            "<td class=\"right\">very much</td>" +
            "</tr></table>" + 
            "<table id=\"multi_slider_table_1" + i + "\"" + "class=\"slider_table\">" +
            "<tr><td></td>" +
            "<td class=\"left\">very bad</td>" + 
            "<td class=\"left\">&emsp;&emsp;&emsp;&emsp;&emsp;neither good nor bad</td>" +
            "<td class=\"right\">very good</td>" +
            "</tr></table>" +
            "<button onclick=\"_s.button()\">Continue</button>" +
            "<p class=\"err\">Please adjust both sliders before continuing.</p>" +
            "</div>";
        $(".trial_slides").html(slides);
    }
}

// Sample unique names for the enforcer and the agent.
function get_characters(characters) {
    var shuffled_characters = _.shuffle(characters);
    var enforcer = shuffled_characters[0];
    var agent = shuffled_characters[1];
    return [enforcer, agent];
}

// Use the appropriate gender-specific pronoun for a given character.
function get_pronoun_1(character, capitalized) {
    if (character.gender == "male") {
        return capitalized ? "He" : "he";
    }
    else {
        return capitalized ? "She" : "she";
    }
}

// Use the appropriate gender-specific pronoun for a given character.
function get_pronoun_2(character, capitalized) {
    if (character.gender == "male") {
        return capitalized ? "Him" : "him";
    }
    else {
        return capitalized ? "Her" : "her";
    }
}

// Use the appropriate gender-specific pronoun for a given character.
function get_pronoun_3(character, capitalized) {
    if (character.gender == "male") {
        return capitalized ? "His" : "his";
    }
    else {
        return capitalized ? "Hers" : "hers";
    }
}

// Use the appropriate gender-specific pronoun for a given character.
function get_pronoun_4(character, capitalized) {
    if (character.gender == "male") {
        return capitalized ? "His" : "his";
    }
    else {
        return capitalized ? "Her" : "her";
    }
}
