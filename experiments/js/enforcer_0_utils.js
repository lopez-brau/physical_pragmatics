// Embeds the trial slides.
function embed_slides(num_trials) {
  var slides = "";
  for (var i = 1; i <= num_trials; i++) {
    slides = slides + "<div class=\"slide\" id=\"trial" + i + "\">" +
      "<p class=\"display_prompt\" style=\"margin-bottom:0px;\"></p>" +
      "<p class=\"display_stimulus\" style=\"margin-top:0px;\"></p>" +
      "<p class=\"display_options\"></p>" +
      "<button onclick=\"_s.button()\">Continue</button>" +
      "<p class=\"trial_error\">Please answer the question before continuing.</p>" +
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
