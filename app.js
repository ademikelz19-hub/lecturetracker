// ==============================================================================
// ACADEMIC COUNTDOWN TRACKER - JAVASCRIPT APPLICATION SCRIPT
// Plain, beginner-friendly vanilla JavaScript designed for undergraduate defense
// Every single line has an explanatory comment describing what it does and why.
// ==============================================================================

// Global Array: Holds all the academic countdown items in memory
var academicItems = [];

// DOM Element: Reference to the form element where new events are submitted
var trackerForm = document.getElementById("trackerForm");

// DOM Element: Reference to the Category dropdown select field in the form
var categoryInput = document.getElementById("categoryInput");

// DOM Element: Reference to the Course Code / Title text input field
var titleInput = document.getElementById("titleInput");

// DOM Element: Reference to the Venue / Notes text input field
var venueInput = document.getElementById("venueInput");

// DOM Element: Reference to the Date picker input field
var dateInput = document.getElementById("dateInput");

// DOM Element: Reference to the Time picker input field
var timeInput = document.getElementById("timeInput");

// DOM Element: Reference to the error message box that shows validation errors
var formErrorMessage = document.getElementById("formErrorMessage");

// DOM Element: Reference to the Category filter dropdown select control
var categoryFilter = document.getElementById("categoryFilter");

// DOM Element: Reference to the Status filter dropdown select control
var statusFilter = document.getElementById("statusFilter");

// DOM Element: Reference to the Clear All button that resets all data
var clearAllBtn = document.getElementById("clearAllBtn");

// DOM Element: Reference to the text element displaying total matching items count
var counterSummary = document.getElementById("counterSummary");

// DOM Element: Reference to the container where countdown cards are rendered
var countdownList = document.getElementById("countdownList");

// Constant: The key name used to store and retrieve data from browser localStorage
var STORAGE_KEY = "academic_countdown_tracker_data";

// ==============================================================================
// FUNCTION: loadItemsFromLocalStorage
// WHAT IT DOES: Reads saved JSON string from browser storage and parses it into array
// WHY IT IS NEEDED: Preserves user data across page refreshes and browser restarts
// ==============================================================================
function loadItemsFromLocalStorage() {
    // Gets the raw string saved under our storage key from the browser's localStorage
    var savedData = localStorage.getItem(STORAGE_KEY);
    // Checks if any saved data was actually found in storage
    if (savedData !== null) {
        // Parses the JSON string back into a JavaScript array of objects
        academicItems = JSON.parse(savedData);
    } else {
        // If no data exists yet, initialize as an empty array
        academicItems = [];
    }
}

// ==============================================================================
// FUNCTION: saveItemsToLocalStorage
// WHAT IT DOES: Converts the academicItems array to JSON and writes it to localStorage
// WHY IT IS NEEDED: Ensures changes (adding, deleting, clearing) persist reliably
// ==============================================================================
function saveItemsToLocalStorage() {
    // Converts the academicItems array into a readable JSON string
    var jsonString = JSON.stringify(academicItems);
    // Writes the JSON string into localStorage under our predefined storage key
    localStorage.setItem(STORAGE_KEY, jsonString);
}

// ==============================================================================
// FUNCTION: formatTwoDigits
// WHAT IT DOES: Adds a leading zero to single digit numbers (e.g. 5 becomes "05")
// WHY IT IS NEEDED: Keeps countdown clock digits uniform and neatly aligned
// ==============================================================================
function formatTwoDigits(number) {
    // Checks if the number is less than 10
    if (number < 10) {
        // Adds "0" in front of the single digit number
        return "0" + number;
    }
    // Returns the number as a string unchanged if it is 10 or greater
    return "" + number;
}

// ==============================================================================
// FUNCTION: calculateCountdownInfo
// WHAT IT DOES: Compares event date/time with the current clock time
// WHY IT IS NEEDED: Determines status (Upcoming/Starting Soon/Passed) & remaining time
// ==============================================================================
function calculateCountdownInfo(dateString, timeString) {
    // Combines the date and time strings into standard ISO datetime format (YYYY-MM-DDTHH:MM:00)
    var fullDateTimeString = dateString + "T" + timeString + ":00";
    // Creates a JavaScript Date object representing the event's target date and time
    var targetDate = new Date(fullDateTimeString);
    // Creates a JavaScript Date object representing the exact current moment
    var currentDate = new Date();
    // Calculates the difference between target time and current time in milliseconds
    var differenceMs = targetDate.getTime() - currentDate.getTime();

    // Variable to hold the calculated status category string
    var status = "Upcoming";
    // Variable to hold the human-readable countdown text string
    var countdownText = "";

    // Checks if the target time has already occurred in the past
    if (differenceMs <= 0) {
        // Sets status to Passed because the time has elapsed
        status = "Passed";
        // Sets display text showing the event has concluded or deadline passed
        countdownText = "Deadline / Event has passed";
    } else {
        // 30 minutes in milliseconds = 30 minutes * 60 seconds * 1000 milliseconds = 1,800,000 ms
        var thirtyMinutesMs = 30 * 60 * 1000;
        // Checks if the event or deadline is scheduled within the next 30 minutes
        if (differenceMs <= thirtyMinutesMs) {
            // Flags item with urgent "Starting Soon" status
            status = "Starting Soon";
        } else {
            // Otherwise the event is in the normal "Upcoming" state
            status = "Upcoming";
        }

        // Calculates total full days remaining by dividing total ms by ms in a day
        var days = Math.floor(differenceMs / (1000 * 60 * 60 * 24));
        // Calculates remaining hours after subtracting full days
        var hours = Math.floor((differenceMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        // Calculates remaining minutes after subtracting full hours
        var minutes = Math.floor((differenceMs % (1000 * 60 * 60)) / (1000 * 60));
        // Calculates remaining seconds after subtracting full minutes
        var seconds = Math.floor((differenceMs % (1000 * 60)) / 1000);

        // Formats days, hours, minutes, and seconds with clean two-digit padding
        countdownText = formatTwoDigits(days) + "d " +
                        formatTwoDigits(hours) + "h " +
                        formatTwoDigits(minutes) + "m " +
                        formatTwoDigits(seconds) + "s";
    }

    // Returns an object containing both the status tag and formatted countdown string
    return {
        status: status,
        countdownText: countdownText,
        targetDateObj: targetDate
    };
}

// ==============================================================================
// FUNCTION: renderCountdownList
// WHAT IT DOES: Builds and injects HTML cards for all items matching current filters
// WHY IT IS NEEDED: Updates the user interface dynamically every second as time ticks
// ==============================================================================
function renderCountdownList() {
    // Reads current value of category filter dropdown (All, Lecture, Test, Examination, Assignment)
    var selectedCategory = categoryFilter.value;
    // Reads current value of status filter dropdown (All, Upcoming, Starting Soon, Passed)
    var selectedStatus = statusFilter.value;

    // Clears existing HTML cards inside the container before re-rendering
    countdownList.innerHTML = "";

    // Counter variable to keep track of how many cards are actively displayed
    var visibleItemCount = 0;

    // Standard for-loop iterating through each item in our academicItems array
    for (var i = 0; i < academicItems.length; i++) {
        // Gets reference to current item object from the array
        var item = academicItems[i];

        // Calculates current time remaining and status for this specific item
        var info = calculateCountdownInfo(item.date, item.time);

        // Checks if current item matches the category filter condition
        var matchesCategory = false;
        // If filter is "All", every item matches
        if (selectedCategory === "All") {
            matchesCategory = true;
        } else if (selectedCategory === item.category) {
            // Otherwise matches if item category equals selected category
            matchesCategory = true;
        }

        // Checks if current item matches the status filter condition
        var matchesStatus = false;
        // If status filter is "All", every item matches
        if (selectedStatus === "All") {
            matchesStatus = true;
        } else if (selectedStatus === info.status) {
            // Otherwise matches if item status equals selected status
            matchesStatus = true;
        }

        // Only create and show card if BOTH category and status filters match
        if (matchesCategory === true && matchesStatus === true) {
            // Increments the displayed item counter
            visibleItemCount = visibleItemCount + 1;

            // Creates a new div element to serve as the card wrapper
            var card = document.createElement("div");
            // Sets class attribute for the card styling
            card.className = "countdown-card";

            // Determines CSS class modifier based on category for border styling
            if (item.category === "Lecture") {
                card.classList.add("card-lecture");
            } else if (item.category === "Test") {
                card.classList.add("card-test");
            } else if (item.category === "Examination") {
                card.classList.add("card-examination");
            } else if (item.category === "Assignment") {
                card.classList.add("card-assignment");
            }

            // Determines CSS class for the category badge pill
            var categoryBadgeClass = "badge-lecture";
            if (item.category === "Test") {
                categoryBadgeClass = "badge-test";
            } else if (item.category === "Examination") {
                categoryBadgeClass = "badge-examination";
            } else if (item.category === "Assignment") {
                categoryBadgeClass = "badge-assignment";
            }

            // Determines CSS class for the status badge pill
            var statusBadgeClass = "status-upcoming";
            if (info.status === "Starting Soon") {
                statusBadgeClass = "status-soon";
            } else if (info.status === "Passed") {
                statusBadgeClass = "status-passed";
            }

            // Determines timer text CSS class (grayed out if passed)
            var timerValueClass = "timer-value";
            if (info.status === "Passed") {
                timerValueClass = "timer-value timer-passed";
            }

            // Formats display string for optional venue, portal, or notes
            var venueDisplay = "";
            if (item.venue && item.venue.trim() !== "") {
                venueDisplay = "Venue / Portal / Notes: " + item.venue;
            } else {
                venueDisplay = "Venue / Portal: Not specified";
            }

            // Determines descriptive label for date depending on whether it is an assignment
            var dateLabel = (item.category === "Assignment") ? "Due Date: " : "Scheduled: ";
            // Formats readable date and time string e.g. "Due Date: 2026-11-20 at 23:59"
            var scheduleDisplay = dateLabel + item.date + " at " + item.time;

            // Builds internal card HTML content with template placeholders
            card.innerHTML =
                '<div class="card-header">' +
                    '<span class="category-badge ' + categoryBadgeClass + '">' + item.category + '</span>' +
                    '<span class="status-badge ' + statusBadgeClass + '">' + info.status + '</span>' +
                '</div>' +
                '<div class="card-body">' +
                    '<h3 class="card-title">' + item.title + '</h3>' +
                    '<p class="card-venue">' + venueDisplay + '</p>' +
                    '<p class="card-datetime">' + scheduleDisplay + '</p>' +
                '</div>' +
                '<div class="card-timer-container">' +
                    '<div class="' + timerValueClass + '">' + info.countdownText + '</div>' +
                '</div>' +
                '<div class="card-footer">' +
                    '<button type="button" class="delete-item-btn" data-id="' + item.id + '">Delete Item</button>' +
                '</div>';

            // Appends the newly assembled countdown card into the countdown list container
            countdownList.appendChild(card);
        }
    }

    // Updates the summary counter text to reflect visible and total counts
    counterSummary.textContent = "Showing " + visibleItemCount + " of " + academicItems.length + " total event(s)";

    // If no items matched current filter or array is empty, display empty state box
    if (visibleItemCount === 0) {
        // Creates empty state notice div
        var emptyNotice = document.createElement("div");
        // Assigns empty state styling class
        emptyNotice.className = "empty-state";
        // Provides helpful friendly message explaining why list is blank
        emptyNotice.textContent = "No academic countdown items match your current filter selection. Add an event or deadline above!";
        // Appends notice into the list container
        countdownList.appendChild(emptyNotice);
    }

    // Attaches click event listeners to all newly rendered Delete buttons
    attachDeleteButtonListeners();
}

// ==============================================================================
// FUNCTION: attachDeleteButtonListeners
// WHAT IT DOES: Finds all Delete buttons on the page and links them to deleteItemHandler
// WHY IT IS NEEDED: Allows students to click "Delete Item" on any card cleanly
// ==============================================================================
function attachDeleteButtonListeners() {
    // Selects all buttons currently on the page that have the delete-item-btn class
    var deleteButtons = document.querySelectorAll(".delete-item-btn");
    // Loops through each delete button found in the DOM
    for (var i = 0; i < deleteButtons.length; i++) {
        // Adds click event listener to each individual delete button
        deleteButtons[i].addEventListener("click", handleDeleteButtonClick);
    }
}

// ==============================================================================
// FUNCTION: handleDeleteButtonClick
// WHAT IT DOES: Reads the unique ID stored on the clicked button and deletes the item
// WHY IT IS NEEDED: Identifies exact item clicked by the user to remove it
// ==============================================================================
function handleDeleteButtonClick(event) {
    // Reads the data-id attribute value stored on the clicked delete button
    var itemIdToDelete = event.target.getAttribute("data-id");
    // Confirms with the user before deleting the item
    var confirmDelete = confirm("Are you sure you want to delete this countdown item?");
    // Only proceed if student confirms deletion
    if (confirmDelete === true) {
        // Calls our helper function to remove the item with this specific ID
        removeItemById(itemIdToDelete);
    }
}

// ==============================================================================
// FUNCTION: removeItemById
// WHAT IT DOES: Removes an item matching the given ID from academicItems array
// WHY IT IS NEEDED: Updates the array, saves to localStorage, and refreshes the UI
// ==============================================================================
function removeItemById(targetId) {
    // Creates a new empty array to hold the remaining items
    var updatedItems = [];
    // Loops through all current items in memory
    for (var i = 0; i < academicItems.length; i++) {
        // Converts id to string comparison so types match reliably
        if (String(academicItems[i].id) !== String(targetId)) {
            // Keeps any item whose ID does not match the target to delete
            updatedItems.push(academicItems[i]);
        }
    }
    // Replaces the old array with the filtered updated array
    academicItems = updatedItems;
    // Persists the updated array to browser localStorage
    saveItemsToLocalStorage();
    // Re-renders the UI immediately to reflect removal
    renderCountdownList();
}

// ==============================================================================
// FUNCTION: handleFormSubmit
// WHAT IT DOES: Validates form input, creates new item object, saves and resets form
// WHY IT IS NEEDED: Handles student adding a new Lecture, Test, Exam, or Assignment
// ==============================================================================
function handleFormSubmit(event) {
    // Prevents standard browser page reload behavior on form submission
    event.preventDefault();

    // Hides any previous error message and clears text
    formErrorMessage.style.display = "none";
    formErrorMessage.textContent = "";

    // Reads and trims whitespace from category dropdown selection
    var categoryValue = categoryInput.value.trim();
    // Reads and trims whitespace from course title input field
    var titleValue = titleInput.value.trim();
    // Reads and trims whitespace from venue input field (optional)
    var venueValue = venueInput.value.trim();
    // Reads date value chosen by student
    var dateValue = dateInput.value;
    // Reads time value chosen by student
    var timeValue = timeInput.value;

    // Validation Check 1: Ensure Category is selected
    if (categoryValue === "") {
        formErrorMessage.textContent = "Please select a category (Lecture, Test, Examination, or Assignment).";
        formErrorMessage.style.display = "block";
        return;
    }

    // Validation Check 2: Ensure Course Title is filled
    if (titleValue === "") {
        formErrorMessage.textContent = "Please enter a course code or event/assignment title.";
        formErrorMessage.style.display = "block";
        return;
    }

    // Validation Check 3: Ensure Date is selected
    if (dateValue === "") {
        formErrorMessage.textContent = "Please select a valid event date or due date.";
        formErrorMessage.style.display = "block";
        return;
    }

    // Validation Check 4: Ensure Time is selected
    if (timeValue === "") {
        formErrorMessage.textContent = "Please select a valid start time or due time.";
        formErrorMessage.style.display = "block";
        return;
    }

    // Creates a new academic item object with a unique timestamp ID
    var newItem = {
        id: Date.now(),
        category: categoryValue,
        title: titleValue,
        venue: venueValue,
        date: dateValue,
        time: timeValue
    };

    // Adds the new item to the beginning of the academicItems array (newest first)
    academicItems.unshift(newItem);

    // Saves the updated array to browser localStorage
    saveItemsToLocalStorage();

    // Re-renders the countdown cards immediately so the new item appears
    renderCountdownList();

    // Resets all input fields on the form back to empty
    trackerForm.reset();
}

// ==============================================================================
// FUNCTION: handleClearAll
// WHAT IT DOES: Prompts confirmation, clears array, wipes localStorage, and re-renders
// WHY IT IS NEEDED: Allows student to reset all items cleanly at once
// ==============================================================================
function handleClearAll() {
    // Checks if there are even any items to clear
    if (academicItems.length === 0) {
        alert("There are no countdown items to clear.");
        return;
    }

    // Asks user for explicit confirmation before wiping all records
    var confirmed = confirm("Are you sure you want to clear ALL academic countdown items? This cannot be undone.");
    // Only proceed if user clicked OK
    if (confirmed === true) {
        // Resets the items array back to an empty array
        academicItems = [];
        // Saves the now-empty array to localStorage
        saveItemsToLocalStorage();
        // Re-renders the display to show empty state
        renderCountdownList();
    }
}

// ==============================================================================
// INITIALIZATION & EVENT LISTENERS
// WHAT IT DOES: Hooks up buttons, form submissions, filters, and timer loop
// WHY IT IS NEEDED: Wires all user interactions and starts live 1-second countdowns
// ==============================================================================

// Event Listener: Runs when DOM content is fully loaded by the browser
document.addEventListener("DOMContentLoaded", function() {
    // Loads any previously saved items from localStorage into memory
    loadItemsFromLocalStorage();

    // Renders initial countdown list from loaded items
    renderCountdownList();

    // Starts an interval timer running every 1000 milliseconds (1 second)
    // to recalculate and refresh live countdown times on all active cards
    setInterval(renderCountdownList, 1000);
});

// Event Listener: Triggers handleFormSubmit when user submits the form
trackerForm.addEventListener("submit", handleFormSubmit);

// Event Listener: Re-renders the list whenever the Category filter dropdown changes
categoryFilter.addEventListener("change", renderCountdownList);

// Event Listener: Re-renders the list whenever the Status filter dropdown changes
statusFilter.addEventListener("change", renderCountdownList);

// Event Listener: Triggers handleClearAll when student clicks Clear All button
clearAllBtn.addEventListener("click", handleClearAll);
