// Generate the stimuli for the trial and exclusion slides.
function trials(doors, condition, side, object) {
    // Stitch together the filenames for all of the doors.
    unmodified_door = doors + ".png"
    low_door = doors + "_low_" + object + ".png"
    none_door = doors + "_none_" + object + ".png"

    // Push the filenames for both trials.
    var trials = []
    if (side == "left") {
        if (condition == "low") {
            trials.push([low_door, unmodified_door])
        }
        else if (condition == "none") {
            trials.push([none_door, unmodified_door])
        } 
    }
    else if (side == "right") {
        if (condition == "low") {
            trials.push([unmodified_door, low_door])
        }
        else if (condition == "none") {
            trials.push([unmodified_door, none_door])
        } 
    }

    return trials
}

// Embeds the trial and exclusion slides.
function embed_slides(num_trials) {
    var trial_slides = "";
    var exclusion_slides = "";
    for (var i = 1; i <= num_trials; i++) {
        trial_slides = trial_slides + "<div class=\"slide\" id=\"trial_" + i + "\">" + 
                       "<p class=\"display_trial\"></p>" +
                       "<button onclick=\"_s.button()\">Continue</button>" +
                       "<p class=\"trial_error\">Please make a selection before continuing.</p>" +
                       "</div>";
    }
    for (var i = 1; i <= 2; i++) {
        exclusion_slides = exclusion_slides + "<div class=\"slide\" id=\"exclusion_" + i + "\">" + 
                           "<p class=\"display_exclusion\"></p>" +
                           "<button onclick=\"_s.button()\">Continue</button>" +
                           "<p class=\"exclusion_error\">Please make a selection before continuing.</p>" +
                           "</div>";
    }
    $(".trial_slides").html(trial_slides);
    $(".exclusion_slides").html(exclusion_slides);
}

// Retrieve the noun phrase for a given object for the instructions slide.
function get_noun_phrase_0(object) {
    noun_phrases = {
        "plant": "is a plant",
        "chair": "is a chair",
        "books": "is a stack of books",
        "cinderblocks": "is a pile of cinderblocks",
        "tape": "is some tape",
        "rulers": "are some rulers taped to the door frame",
        "hat": "is a hat",
        "fishbowl": "is a fishbowl tied to a string"
    }

    return noun_phrases[object]
}

// Retrieve the noun phrase for a given object for the transition slide.
function get_noun_phrase_1(object) {
    noun_phrases = {
        "plant": "a plant",
        "chair": "a chair",
        "books": "a stack of books",
        "cinderblocks": "a pile of cinderblocks",
        "tape": "some tape",
        "rulers": "some rulers taped to the door frame",
        "hat": "a hat",
        "string": "a fishbowl tied to a string"
    }

    return noun_phrases[object]
}
