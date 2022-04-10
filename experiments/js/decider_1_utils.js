// Generate the stimuli for the trial and exclusion slides.
function trials(condition, side, object, doors) {
  // Stitch together the filenames for all of the doors.
  none_door = doors + "_none_" + ((object == "fishbowl") ? "string" : object) + ".png"
  low_door = doors + "_low_" + ((object == "fishbowl") ? "string" : object) + ".png"

  // Push the filenames for both trials.
  var trials = []
  if (side == "left") {
    if (condition == "none") {
      trials.push([low_door, none_door])
    }
    else if (condition == "high") {
      trials.push([low_door, high_door])
    } 
  }
  else if (side == "right") {
    if (condition == "none") {
      trials.push([none_door, low_door])
    }
    else if (condition == "high") {
      trials.push([high_door, low_door])
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

// Retrieve the noun phrase for a given object for the context slide.
function get_noun_phrase(object) {
  noun_phrases = {
    "plant": "some plants",
    "chair": "some chairs",
    "books": "stacks of books",
    "cinderblocks": "piles of cinderblocks",
    "tape": "some tape",
    "rulers": "some rulers taped to the door frames",
    "hat": "some hats",
    "fishbowl": "some string and a fishbowl tacked to one of the door frames"
  }

  return noun_phrases[object]
}

// Retrieve the plural form for the quiz.
function get_plural(object) {
  plural = {
    "plant": "plants",
    "chair": "chairs",
    "books": "books",
    "cinderblocks": "cinderblocks",
    "tape": "tape",
    "rulers": "rulers",
    "hat": "hats",
    "fishbowl": "string and a fishbowl"
  }

  return plural[object]
}

// Sample unique names for the enforcer.
function get_enforcer(characters) {
  return _.sample(characters);
}

// Use the appropriate gender-specific pronoun for the enforcer.
function get_enforcer_pronoun(character, capitalized) {
  if (character.gender == "male") {
    return capitalized ? "He" : "he";
  }
  else {
    return capitalized ? "She" : "she";
  }
}