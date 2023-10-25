var stopLossInputs = document.querySelectorAll(".stop-loss-group");
// Show no stop loss inputs
stopLossInputs.forEach(function(input) {
  input.style.display = "none";
});


document.getElementById("system").addEventListener("change", function() {
  var selectedSystem = this.value;



  // Show specific stop loss inputs based on the selected system
  if (selectedSystem === "0") {
      // Show no stop loss inputs
      stopLossInputs.forEach(function(input) {
        input.style.display = "none";
    });

  } else if (selectedSystem === "1") {
      // Show the required inputs for system 1
      stopLossInputs[0].style.display = "block";
      stopLossInputs[1].style.display = "block";
      stopLossInputs[2].style.display = "block";
      stopLossInputs[3].style.display = "block";
      stopLossInputs[4].style.display = "none";
  } else if (selectedSystem === "2") {
      // Show the required inputs for system 2
      stopLossInputs[0].style.display = "block";
      stopLossInputs[1].style.display = "none";
      stopLossInputs[2].style.display = "none";
      stopLossInputs[3].style.display = "none";
      stopLossInputs[4].style.display = "block";
      
  } else if (selectedSystem === "3") {
      // Show the required inputs for system 3
      stopLossInputs[0].style.display = "block";
      stopLossInputs[1].style.display = "none";
      stopLossInputs[2].style.display = "none";
      stopLossInputs[3].style.display = "none";
      stopLossInputs[4].style.display = "block";
  }
  // Add more conditions for other system options if needed
});
