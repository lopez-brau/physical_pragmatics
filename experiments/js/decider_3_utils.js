// Generate the stimuli for the trial and exclusion slides.
function trials(doors, condition, side, object) {
  // Stitch together the filenames for all of the doors.
  unmodified_door = doors + "_door.png";
  low_door = doors + "_low_" + object + ".png";
  none_door = doors + "_none_" + object + ".png";

  // Push the filenames for both trials.
  var trials = [];
  if (side == "left") {
    if (condition == "low") {
      trials.push([low_door, unmodified_door]);
    }
    else if (condition == "none") {
      trials.push([none_door, unmodified_door]);
    }
  }
  else if (side == "right") {
    if (condition == "low") {
      trials.push([unmodified_door, low_door]);
    }
    else if (condition == "none") {
      trials.push([unmodified_door, none_door]);
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
function get_noun_phrase(condition, object) {
  noun_phrases = {
    "cone": "is a traffic cone",
    "stanchion": "is a stanchion",
    "tape": "is some construction tape"
  }

  return noun_phrases[object];
}

// Extracts the URL parameters.
function get_url_parameters(parameter) {
  var url = window.location.search.substring(1);
  var url_variables = url.split("&");
  for (var i = 0; i < url_variables.length; i++) {
    var parameter_assignment = url_variables[i].split("=");
    if (parameter_assignment[0] == parameter) {
      return parameter_assignment[1];
    }
  }
  console.log("No parameters found.");
  return "no_params";
}
