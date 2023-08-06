// Process opening_hours data
const openingHoursString = '{{ opening_hours }}';  // Access the opening hours data in your JavaScript code
   const oh = new opening_hours(openingHoursString);
   const now = new Date();
   const isOpen = oh.getState(now);

   const openingStatusElement = document.getElementById('openingStatus');
   openingStatusElement.textContent = isOpen ? "It's open" : "It's closed";