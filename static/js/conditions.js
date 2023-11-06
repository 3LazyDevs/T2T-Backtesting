// select elements for attribute setting
var entry_criteria = document.querySelectorAll("#entry_criteria");
var exit_criteria = document.querySelectorAll("#exit_criteria");
var msl = document.querySelectorAll("#msl");
var tsl1 = document.querySelectorAll("#tsl1");
var tsl2 = document.querySelectorAll("#tsl2");
var days = document.querySelectorAll("#days");


var stopLossInputs = document.querySelectorAll(".stop-loss-group");
var criteriaInputs = document.querySelectorAll(".criteria-group");
// Show no stop loss inputs
stopLossInputs.forEach(function(input) {
  input.style.display = "none";
});

criteriaInputs.forEach(function(input) {
  input.style.display = "none";
});

document.getElementById("system").addEventListener("change", function() {
  var selectedSystem = this.value;



  // Show specific stop loss inputs based on the selected system
  if (selectedSystem === "0") {

      criteriaInputs.forEach(function(input) {
        input.style.display = "none";

    }, this);
      
      // Show no stop loss inputs
      stopLossInputs.forEach(function(input) {
        input.style.display = "none";

    });

  } else if (selectedSystem === "1") {
      msl[0].removeAttribute('required');
      tsl1[0].setAttribute('required', '');
      tsl2[0].setAttribute('required', '');
      days[0].removeAttribute('required');
      entry_criteria[0].removeAttribute('required');
      exit_criteria[0].removeAttribute('required');

      // Show the required inputs for system 1
      criteriaInputs[0].style.display = "none";
      criteriaInputs[1].style.display = "none";

      stopLossInputs[0].style.display = "none";
      stopLossInputs[1].style.display = "block";
      stopLossInputs[2].style.display = "block";
      stopLossInputs[3].style.display = "none";
      stopLossInputs[4].style.display = "block";
      stopLossInputs[5].style.display = "none";
  } else if (selectedSystem === "2") {
      msl[0].setAttribute('required', '');
      tsl1[0].removeAttribute('required');
      tsl2[0].removeAttribute('required');
      days[0].setAttribute('required', '');
      entry_criteria[0].removeAttribute('required');
      exit_criteria[0].removeAttribute('required');
      // Show the required inputs for system 2
      criteriaInputs[0].style.display = "none";
      criteriaInputs[1].style.display = "none";

      stopLossInputs[0].style.display = "block";
      stopLossInputs[1].style.display = "none";
      stopLossInputs[2].style.display = "none";
      stopLossInputs[3].style.display = "block";
      stopLossInputs[4].style.display = "none";
      stopLossInputs[5].style.display = "block";
      
  } else if (selectedSystem === "3") {
      msl[0].setAttribute('required', '');
      tsl1[0].removeAttribute('required');
      tsl2[0].removeAttribute('required');
      days[0].removeAttribute('required');

      entry_criteria[0].setAttribute('required', '');
      exit_criteria[0].setAttribute('required', '');
      // Show the required inputs for system 3
      criteriaInputs[0].style.display = "block";
      criteriaInputs[1].style.display = "block";

      stopLossInputs[0].style.display = "block";
      stopLossInputs[1].style.display = "none";
      stopLossInputs[2].style.display = "none";
      stopLossInputs[3].style.display = "none";
      stopLossInputs[4].style.display = "none";
      stopLossInputs[5].style.display = "block";
  }
  // Add more conditions for other system options if needed
});
