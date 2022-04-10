// Generate the prompts for each condition and object pair.
function generate_prompt(condition, object) {
  var prompts = {
    "plant": (condition == "none") ? "a flower pot beside the door." : "a flower pot in front of the door.",
    "chair": (condition == "none") ? "a chair beside the door." : "a chair in front of the door.",
    "books": (condition == "none") ? "a pile of books beside the door." : "a pile of books in front of the door.",
    "cinderblocks": (condition == "none") ? "a pile of cinderblocks beside the door." : "a pile of cinderblocks in front of the door.",
    "tape": (condition == "none") ? "some tape beside the door." : "some tape across the front of the door.",
    "rulers": (condition == "none") ? "some rulers beside the door." : "some rulers in front of the door.",
    "hat": (condition == "none") ? "a hat beside the door." : "a hat on the door knob.",
    "string": (condition == "none") ? "a piece of string in front of the door." : "a piece of string tied to a fishbowl in front of the door."
  };
  return prompts[object];
}

// Embeds the trial slides.
function embed_slides(num_trials) {
  var slides = "";
  for (var i = 1; i <= num_trials; i++) {
    slides = slides + "<div class=\"slide\" id=\"trial" + i + "\">" +
      "<p class=\"display_prompt\"></p>" +
      "<p class=\"display_stimulus\"></p>" +
      "<table id=\"multi_slider_table" + i + "\"" + "class=\"slider_table\">" +
      "<tr><td></td>" +
      "<td class=\"left\">not at all</td>" +
      "<td class=\"right\">very unusual</td>" +
      "</tr></table>" +
      "<button onclick=\"_s.button()\">Continue</button>" +
      "<p class=\"trial_error\">Please adjust the slider(s) before continuing.</p>" +
      "</div>";
    $(".trial_slides").html(slides);
  }
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
