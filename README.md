# Academic Countdown Tracker (Lectures, Tests, Examinations, and Assignments)

A simple, beginner-friendly academic countdown web application built strictly with **pure HTML5, CSS3, and vanilla JavaScript**. It serves as a single source of truth for students to track upcoming **Lectures**, **Tests**, **Examinations**, and **Assignment Submission Deadlines** with real-time countdown clocks, audio alerts, and persistent browser storage.

---

## 🌟 Key Features

1. **Four Academic Categories**:
   - 🔵 **Lecture**: Blue accent styling and badge.
   - 🟠 **Test**: Amber accent styling and badge.
   - 🔴 **Examination**: Red accent styling and badge.
   - 🟣 **Assignment Submission**: Purple accent styling and badge for homework/project due dates.

2. **Real-Time Live Countdown & Audio Alert**:
   - Calculates time remaining down to the exact second (`Days`, `Hours`, `Minutes`, `Seconds`) using `setInterval()` updating every 1000ms.
   - **Audible Notification Alert**: Automatically plays a clean, synthesized two-tone bell chime using the browser's native **Web Audio API** (no external audio files needed) the instant a countdown reaches zero.
   - **🔊 Test Sound Button**: Allows students and lecturers to preview the audio alert on demand.
   - Status indicators:
     - 🟢 **Upcoming**: Normal scheduled events/deadlines in the future.
     - 🟠 **Starting Soon**: Events starting or due within the next 30 minutes (< 30m).
     - ⚪ **Passed**: Events or deadlines whose scheduled time has elapsed.

3. **Filtering & Searching**:
   - Filter by **Category**: All Categories, Lectures Only, Tests Only, Examinations Only, Assignments Only.
   - Filter by **Status**: All Statuses, Upcoming Only, Starting Soon Only, Passed Only.
   - Real-time counter showing visible vs. total saved events.

4. **Add & Manage Events**:
   - Form with input validation for required fields (Category, Title, Date, Time) and optional venue/submission portal notes.
   - Delete individual events with confirmation.
   - Clear All events button with confirmation warning.

5. **Data Persistence (`localStorage`)**:
   - All events are stored in the browser's `localStorage` as JSON.
   - Events remain saved after refreshing, closing, or reopening the browser tab on desktop or mobile.

6. **Fully Commented for Academic Defense**:
   - **Every single line** of HTML, CSS, and JavaScript is thoroughly commented in plain English explaining what the line does and why it is needed.

---

## 📂 Project Structure

```text
tracker/
├── index.html       # HTML5 structure with semantic sections and line-by-line comments
├── style.css        # Responsive CSS styling with color badges and line-by-line comments
├── app.js           # Vanilla JavaScript logic, audio synthesizer, timers, filters
└── README.md        # Project documentation and lecturer defense guide
```

---

## 🚀 How to Run the Project

No build tools, bundlers, or package managers (npm/yarn) are required.

### Option 1: Direct File Open
1. Double-click `index.html` or right-click and choose **Open With -> Chrome / Firefox / Edge / Safari**.

### Option 2: Using Python HTTP Server or Live Server
```bash
# If using Python:
python -m http.server 8000
# Then open http://localhost:8000 in your browser
```

---

## 🎓 Group Defense / Presentation Guide

If your lecturer asks you about how the application works, here is a quick cheat sheet:

1. **How does the countdown timer work?**
   - In `app.js`, `calculateCountdownInfo()` takes the event's date and time strings and builds a JavaScript `new Date()` object.
   - It subtracts the current timestamp (`new Date().getTime()`) from the target timestamp (`targetDate.getTime()`).
   - The difference in milliseconds is converted to Days, Hours, Minutes, and Seconds using `Math.floor()` and the modulo `%` operator.
   - `setInterval(renderCountdownList, 1000)` runs every second to update the numbers on screen continuously.

2. **How does the Audio Alert work?**
   - `playNotificationSound()` uses the built-in browser `AudioContext` (Web Audio API).
   - It creates two sine wave oscillators (`880Hz` and `1108.73Hz`) with gentle gain decay envelopes to produce a clean two-tone chime without relying on external mp3 files or network downloads.
   - When an active countdown crosses below `0ms`, it plays the chime once and sets `item.hasAlerted = true` so it doesn't repeat every second.

3. **How does data stay saved when refreshing?**
   - The browser provides a built-in storage API called `localStorage`.
   - When an item is added or deleted, `saveItemsToLocalStorage()` calls `JSON.stringify(academicItems)` and stores it.
   - When the page loads (`DOMContentLoaded`), `loadItemsFromLocalStorage()` reads the string with `localStorage.getItem()` and converts it back to an array using `JSON.parse()`.

4. **How does filtering work?**
   - When you change either the Category or Status dropdown, `categoryFilter.addEventListener("change", renderCountdownList)` triggers immediately.
   - The function loops through the array and only displays cards that match both chosen criteria.

---

## 👤 Author
- GitHub: [ademikelz19-hub](https://github.com/ademikelz19-hub)
- Repository: [lecturetracker](https://github.com/ademikelz19-hub/lecturetracker)
