// Generate the trial slides.
function trials(door, cost, object) {
    // Stitch together the filenames for each door.
    empty_door = door + ".png"
    object_door = door + "_" + cost + "_" + object + ".png"

    // Push the filenames to trials.
    var trials = []
    trials.push(_.shuffle([empty_door, object_door]))

    return trials
}

// Embeds the trial slides.
function embed_slides(num_trials) {
    var slides = "";
    for (var i = 1; i <= num_trials; i++) {
        slides = slides + "<div class=\"slide\" id=\"trial" + i + "\">" + 
            "<p class=\"display_setup\"></p>" +
            "<p class=\"display_stimulus\"></p>" +
            "<button onclick=\"_s.button()\">Continue</button>" +
            "<p class=\"error\">Please make a selection before continuing.</p>" +
            "</div>";
        $(".trial_slides").html(slides);
    }
}

// Sample unique names for the enforcer and the agent.
function get_characters(characters) {
    var shuffled_characters = _.shuffle(characters)
    var enforcer = shuffled_characters[0]
    var agent = shuffled_characters[1]
    return [enforcer, agent]
}

// Use the appropriate gender-specific pronoun for a given character.
function get_pronoun_1(character, capitalized) {
    if (character.gender == "male") {
        return capitalized ? "He" : "he"
    }
    else {
        return capitalized ? "She" : "she"
    }
}

// Use the appropriate gender-specific pronoun for a given character.
function get_pronoun_2(character, capitalized) {
    if (character.gender == "male") {
        return capitalized ? "Him" : "him"
    }
    else {
        return capitalized ? "Her" : "her"
    }
}

// Use the appropriate gender-specific pronoun for a given character.
function get_pronoun_3(character, capitalized) {
    if (character.gender == "male") {
        return capitalized ? "His" : "his"
    }
    else {
        return capitalized ? "Hers" : "hers"
    }
}

// Use the appropriate gender-specific pronoun for a given character.
function get_pronoun_4(character, capitalized) {
    if (character.gender == "male") {
        return capitalized ? "His" : "his"
    }
    else {
        return capitalized ? "Her" : "her"
    }
}