// Generates the trial slides.
function trials(pear_position) {
  // Construct a randomized list of stimuli.
  var trials = [];
  var natural_costs = [[5, 5], [5, 7], [7, 5], [5, 9], [9, 5], [7, 7], [7, 9], [9, 7], [9, 9]];
  var actor_actions = [[1, 0], [2, 0], [3, 0]];
  for (var i = 0; i < natural_costs.length; i++) {
    for (var j = 0; j < actor_actions.length; j++) {
      // Sample decider and pear coordinates.
      var decider_coords = _.sample(["[0.5 0.5]", "[9.5 0.5]", "[9.5 9.5]", "[0.5 9.5]"]);
      var pear_coords = {
        "[0.5 0.5]": ["[9.5 0.5]", "[0.5 9.5]"],
        "[9.5 0.5]": ["[9.5 9.5]", "[0.5 0.5]"],
        "[9.5 9.5]": ["[0.5 9.5]", "[9.5 0.5]"],
        "[0.5 9.5]": ["[0.5 0.5]", "[9.5 9.5]"]
      }[decider_coords][parseInt(pear_position)];
      filepath = decider_coords + "/" + pear_coords + "/[" + natural_costs[i].join(" ") + "]_[" +
        actor_actions[j].join(" ") + "].png";
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
        "<table id=\"multi_slider_table" + i + "\"" + "class=\"slider_table\">" +
        "<tr><td></td>" +
        "<td class=\"left\">not at all</td>" +
        "<td class=\"right\">very much</td>" +
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
