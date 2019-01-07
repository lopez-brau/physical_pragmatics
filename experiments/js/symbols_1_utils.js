// Generate the stimuli for the trial and exclusion slides.
function trials(doors, condition, side, first_object, second_object) {
    // Stitch together the filenames for all of the doors.
    unmodified_door = doors + ".png";
    if (condition == "object") {
        object_door = doors + "_low_" + ((first_object == "fishbowl") ? "string" : first_object) + ".png";
        symbol_door = doors + "_symbol_" + ((second_object == "fishbowl") ? "string" : second_object) + ".png";    
    }
    else if (condition == "symbol") {
        symbol_door = doors + "_symbol_" + ((first_object == "fishbowl") ? "string" : first_object) + ".png";
        object_door = doors + "_low_" + ((second_object == "fishbowl") ? "string" : second_object) + ".png";    
    }

    // Push the filenames for both trials.
    var trials = [];
    if (side == "left") {
        if (condition == "object") {
            trials.push([object_door, unmodified_door]);
            trials.push([symbol_door, unmodified_door]);
        }
        else if (condition == "symbol") {
            trials.push([symbol_door, unmodified_door]);
            trials.push([object_door, unmodified_door]);
        } 
    }
    else if (side == "right") {
        if (condition == "object") {
            trials.push([unmodified_door, object_door]);
            trials.push([unmodified_door, symbol_door]);
        }
        else if (condition == "symbol") {
            trials.push([unmodified_door, symbol_door]);
            trials.push([unmodified_door, object_door]);
        } 
    }

    return trials;
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
        exclusion_slides = exclusion_slides + "<div class=\"slide\" id=\"exclusion_" + i + "\">" + 
                           "<p class=\"display_exclusion\"></p>" +
                           "<button onclick=\"_s.button()\">Continue</button>" +
                           "<p class=\"exclusion_error\">Please make a selection before continuing.</p>" +
                           "</div>";
    }
    $(".trial_slides").html(trial_slides);
    $(".exclusion_slides").html(exclusion_slides);
}

// Retrieve the noun phrase for a given object for the context slide.
function get_noun_phrase_0(condition, object) {
    noun_phrases = {
        "plant": ((condition == "symbol") ? "is a picture of" : "is") + " a plant",
        "chair": ((condition == "symbol") ? "is a picture of" : "is") + " a chair",
        "books": ((condition == "symbol") ? "is a picture of" : "are")+ " some books",
        "cinderblocks": ((condition == "symbol") ? "is a picture of" : "is") + " a pile of cinderblocks",
        "tape": ((condition == "symbol") ? "is a picture of" : "is") + " some tape",
        "rulers": ((condition == "symbol") ? "is a picture of" : "are") + " some rulers taped to the door frame",
        "hat": ((condition == "symbol") ? "is a picture of" : "is") + " a hat",
        "fishbowl": ((condition == "symbol") ? "is a picture of" : "is") + " a fishbowl tied to a string"
    };

    return noun_phrases[object];
}

// Retrieve the first noun phrase for a given object for the transition slide.
function get_noun_phrase_1(condition, object) {
    noun_phrases = {
        "plant": ((condition == "symbol") ? "a picture of " : "") + "a plant",
        "chair": ((condition == "symbol") ? "a picture of " : "") + "a chair",
        "books": ((condition == "symbol") ? "a picture of " : "") + "some books",
        "cinderblocks": ((condition == "symbol") ? "a picture of " : "") + "a pile of cinderblocks",
        "tape": ((condition == "symbol") ? "a picture of " : "") + "some tape",
        "rulers": ((condition == "symbol") ? "a picture of " : "") + "some rulers taped to the door frame",
        "hat": ((condition == "symbol") ? "a picture of " : "") + "a hat",
        "fishbowl": ((condition == "symbol") ? "a picture of " : "") + "a fishbowl tied to a string"
    };

    return noun_phrases[object];
}
