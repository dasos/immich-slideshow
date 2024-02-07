// Some nice yummy global variables
currentIndex = -1;
list = [];

var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/photos', true);

xhr.onload = function() {

  if (xhr.status == 200) {

    list = JSON.parse(xhr.responseText);
    console.log(list);
    
    // Kick things off
    nextPhoto();


  }
};

// Set up a function to handle errors
xhr.onerror = function() {
  console.error('Request failed');
};

// Send the request
xhr.send();


function nextPhoto() {
    
      currentIndex = (currentIndex + 1) % list.length; // Loop back to the beginning when reaching the end

      var i = document.getElementById('image');

	  var origClassName = i.className;
	  i.className += " transition";
	  console.log("Starting transition")
	  
	  // Give it a chance to fade out. Not too long though, the image will take a while to load
	  setTimeout(function() {
	    console.log("Changing photo")
        i.src = "api/proxy/" + list[currentIndex].id;
        
        // Wait till the photo is loaded. This can be a while
        i.onload = function() {
            console.log("Photo loaded");
            
		    i.className = origClassName;
        	console.log("Ending transition")
       
	        setTimeout(nextPhoto, 7000);
            
        };
        
        i.onerror = function() {
            setTimeout(nextPhoto, 7000);
        }
        
	  }, 250);

};



// Refresh early in the morning
(function () {
    var now = new Date();

	var tomorrow = new Date(now);
	tomorrow.setDate(now.getDate() + 1);
	tomorrow.setHours(2, 0, 0, 0); // Set time to 2 AM tomorrow
	var timeUntil2AM = tomorrow - now; // Time until 2 AM tomorrow in milliseconds
    }

    // Schedule refresh at 2 AM
    setTimeout(function() {
        location.reload();
    }, timeUntil2AM);
})();