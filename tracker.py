# ==============================================================================
# ACADEMIC COUNTDOWN TRACKER - PYTHON DESKTOP APPLICATION
# Built with pure standard Python (Tkinter GUI, JSON storage, and winsound alarm)
# Every single line has an explanatory comment describing what it does and why.
# ==============================================================================

# Standard Library: Imports the Tkinter graphical user interface library
import tkinter as tk
# Standard Library: Imports modern themed Tkinter widgets for dropdowns and tables
from tkinter import ttk
# Standard Library: Imports message box dialogs for alerts, errors, and alarms
from tkinter import messagebox
# Standard Library: Imports datetime and timedelta for date/time parsing and countdown math
from datetime import datetime
# Standard Library: Imports json module to read and write saved events to disk
import json
# Standard Library: Imports os module to check if storage file exists on the computer
import os
# Standard Library: Imports platform module to detect the operating system (Windows/Mac/Linux)
import platform

# Global List: Stores all academic event dictionaries in memory while the app runs
academic_items = []

# Constant: File path where saved items are stored persistently on the hard drive
DATA_FILE = "academic_tracker.json"

# ==============================================================================
# FUNCTION: trigger_alarm_sound
# WHAT IT DOES: Plays an audible beep alarm through the computer speakers
# WHY IT IS NEEDED: Alerts students with sound when a deadline or event time is up
# ==============================================================================
def trigger_alarm_sound():
    # Checks if the user is running Microsoft Windows
    if platform.system() == "Windows":
        # Imports the built-in Windows sound module
        import winsound
        # Plays a chime sound tone at 1000 Hertz for 500 milliseconds (half second)
        winsound.Beep(1000, 500)
        # Plays a second slightly higher chime tone at 1400 Hertz for 600 milliseconds
        winsound.Beep(1400, 600)
    else:
        # Cross-platform fallback: Sends the terminal bell character (\a) to beep speaker
        print("\a")

# ==============================================================================
# FUNCTION: load_data_from_file
# WHAT IT DOES: Reads saved JSON data from disk into the global academic_items list
# WHY IT IS NEEDED: Preserves user events across app restarts and computer reboots
# ==============================================================================
def load_data_from_file():
    # Declares academic_items as global so we can update the shared list
    global academic_items
    # Checks if our data file already exists in the current directory
    if os.path.exists(DATA_FILE):
        # Safely opens the file in read mode with UTF-8 encoding
        with open(DATA_FILE, "r", encoding="utf-8") as file_handle:
            # Parses the JSON string from the file back into Python list of dictionaries
            academic_items = json.load(file_handle)
    else:
        # If the file does not exist yet, initializes with an empty list
        academic_items = []

# ==============================================================================
# FUNCTION: save_data_to_file
# WHAT IT DOES: Writes the academic_items list to disk as formatted JSON
# WHY IT IS NEEDED: Ensures newly added or deleted items are permanently saved
# ==============================================================================
def save_data_to_file():
    # Opens the data file in write mode, creating it if it does not exist
    with open(DATA_FILE, "w", encoding="utf-8") as file_handle:
        # Dumps the list into the file formatted with 4 spaces for readability
        json.dump(academic_items, file_handle, indent=4)

# ==============================================================================
# FUNCTION: calculate_time_remaining
# WHAT IT DOES: Compares event date/time string with current clock time
# WHY IT IS NEEDED: Calculates days, hours, minutes, seconds, and status (Upcoming/Passed)
# ==============================================================================
def calculate_time_remaining(date_str, time_str):
    # Combines date and time into standard format (e.g., '2026-11-25 14:30')
    datetime_combined = date_str + " " + time_str
    # Parses the combined string into a Python datetime object
    target_dt = datetime.strptime(datetime_combined, "%Y-%m-%d %H:%M")
    # Gets the current exact date and time right now
    now_dt = datetime.now()
    # Calculates the difference between target time and now
    delta = target_dt - now_dt
    # Converts the total time difference into total seconds
    total_seconds = int(delta.total_seconds())

    # Checks if the target time has already arrived or passed in the past
    if total_seconds <= 0:
        # Returns Passed status, a friendly label, and remaining seconds
        return "Passed", "Event/Deadline Elapsed", total_seconds
    else:
        # Calculates full days remaining by dividing seconds by seconds in a day (86400)
        days = total_seconds // 86400
        # Calculates remaining hours after subtracting full days
        hours = (total_seconds % 86400) // 3600
        # Calculates remaining minutes after subtracting full hours
        minutes = (total_seconds % 3600) // 60
        # Calculates remaining seconds after subtracting full minutes
        seconds = total_seconds % 60

        # Formats countdown string with 2-digit padding e.g. '02d 04h 15m 30s'
        countdown_str = f"{days:02d}d {hours:02d}h {minutes:02d}m {seconds:02d}s"

        # Checks if event starts within the next 30 minutes (30 mins * 60 secs = 1800 secs)
        if total_seconds <= 1800:
            # Returns Starting Soon status
            return "Starting Soon", countdown_str, total_seconds
        else:
            # Returns standard Upcoming status
            return "Upcoming", countdown_str, total_seconds

# ==============================================================================
# FUNCTION: refresh_items_display
# WHAT IT DOES: Clears and repopulates the visual listbox/treeview with current items
# WHY IT IS NEEDED: Keeps countdown clocks ticking live on screen every single second
# ==============================================================================
def refresh_items_display():
    # Gets selected category filter value from the dropdown
    selected_cat = category_filter_var.get()
    # Gets selected status filter value from the dropdown
    selected_status = status_filter_var.get()

    # Removes all existing rows from the Treeview table before reloading
    for child in tree.get_children():
        tree.delete(child)

    # Counter to track how many items match the current active filters
    visible_count = 0
    # Flag to track if any item's alarm triggered so we save storage
    needs_save = False

    # Loops through all items currently stored in memory
    for item in academic_items:
        # Computes remaining time and status for this item
        status, countdown_str, remaining_seconds = calculate_time_remaining(item["date"], item["time"])

        # Check if the item reached zero, time is up, and alarm has not fired yet
        if remaining_seconds <= 0 and item.get("has_alerted") is not True:
            # If the event expired within the last 15 seconds, play audible alarm
            if remaining_seconds > -15:
                # Triggers the two-tone speaker beep
                trigger_alarm_sound()
                # Shows a visible graphical alarm notification dialog
                messagebox.showwarning("Academic Alarm!", f"Time is UP for: {item['title']} ({item['category']})")
            # Marks item as alerted so sound does not repeat every second
            item["has_alerted"] = True
            # Flags that data needs saving
            needs_save = True

        # Category Filter matching logic
        matches_cat = (selected_cat == "All" or selected_cat == item["category"])
        # Status Filter matching logic
        matches_status = (selected_status == "All" or selected_status == status)

        # Only insert row into display if BOTH category and status match
        if matches_cat and matches_status:
            # Increments visible count
            visible_count += 1
            # Formats venue or note display text
            venue_text = item["venue"] if item["venue"] else "Not specified"
            # Inserts row into Treeview table with item ID as row iid
            tree.insert("", "end", iid=str(item["id"]), values=(
                item["category"],
                item["title"],
                venue_text,
                f"{item['date']} {item['time']}",
                status,
                countdown_str
            ))

    # If any item's alert flag changed, save updated data to file
    if needs_save:
        save_data_to_file()

    # Updates summary counter label text at bottom of window
    summary_label.config(text=f"Showing {visible_count} of {len(academic_items)} total event(s)")

    # Schedules this refresh function to run again after 1000 milliseconds (1 second)
    root.after(1000, refresh_items_display)

# ==============================================================================
# FUNCTION: handle_add_item
# WHAT IT DOES: Validates form fields, builds new item dictionary, saves and refreshes
# WHY IT IS NEEDED: Allows students to add new Lectures, Tests, Exams, and Deadlines
# ==============================================================================
def handle_add_item():
    # Reads and strips category selection
    category = category_entry_var.get().strip()
    # Reads and strips course title
    title = title_entry.get().strip()
    # Reads and strips venue or portal note
    venue = venue_entry.get().strip()
    # Reads and strips event date
    date_val = date_entry.get().strip()
    # Reads and strips event time
    time_val = time_entry.get().strip()

    # Validation: Ensures category is selected
    if not category:
        messagebox.showerror("Validation Error", "Please select an Academic Category.")
        return

    # Validation: Ensures course title is provided
    if not title:
        messagebox.showerror("Validation Error", "Please enter a Course Code / Title.")
        return

    # Validation: Checks that date is in valid YYYY-MM-DD format
    try:
        datetime.strptime(date_val, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Validation Error", "Date must be in YYYY-MM-DD format (e.g. 2026-11-25).")
        return

    # Validation: Checks that time is in valid HH:MM format
    try:
        datetime.strptime(time_val, "%H:%M")
    except ValueError:
        messagebox.showerror("Validation Error", "Time must be in 24-hour HH:MM format (e.g. 14:30).")
        return

    # Checks if entered event is already in the past
    status, _, remaining_seconds = calculate_time_remaining(date_val, time_val)
    # If already passed, set has_alerted to True so it doesn't immediately beep
    initial_alert = (remaining_seconds <= 0)

    # Builds new academic event dictionary with a millisecond timestamp id
    new_event = {
        "id": int(datetime.now().timestamp() * 1000),
        "category": category,
        "title": title,
        "venue": venue,
        "date": date_val,
        "time": time_val,
        "has_alerted": initial_alert
    }

    # Adds new event to the top of the academic items list
    academic_items.insert(0, new_event)
    # Saves updated list to file
    save_data_to_file()
    # Clears entry input boxes for next event entry
    title_entry.delete(0, tk.END)
    venue_entry.delete(0, tk.END)
    # Displays confirmation success message
    messagebox.showinfo("Success", f"{category} '{title}' added successfully!")

# ==============================================================================
# FUNCTION: handle_delete_selected
# WHAT IT DOES: Deletes the selected row from the Treeview and list
# WHY IT IS NEEDED: Allows students to remove completed or cancelled items
# ==============================================================================
def handle_delete_selected():
    # Gets list of currently selected items in the Treeview
    selected_rows = tree.selection()
    # Checks if user forgot to select an item first
    if not selected_rows:
        messagebox.showwarning("Selection Required", "Please select an item from the table to delete.")
        return

    # Asks student for confirmation before deleting
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected item?")
    # Only proceeds if user clicked 'Yes'
    if confirm:
        # Gets the ID of the selected row
        selected_id = int(selected_rows[0])
        # Filters out the item matching this selected ID
        global academic_items
        academic_items = [item for item in academic_items if item["id"] != selected_id]
        # Saves changes to file
        save_data_to_file()

# ==============================================================================
# FUNCTION: handle_clear_all
# WHAT IT DOES: Deletes all items from memory and storage after confirmation
# WHY IT IS NEEDED: Provides a one-click clean reset for students
# ==============================================================================
def handle_clear_all():
    # Checks if there are any items to delete
    if not academic_items:
        messagebox.showinfo("Info", "There are no countdown items to clear.")
        return

    # Asks confirmation before wiping all items
    confirm = messagebox.askyesno("Confirm Clear All", "Are you sure you want to delete ALL academic countdowns? This cannot be undone.")
    # Only proceeds if confirmed
    if confirm:
        # Clears list
        academic_items.clear()
        # Saves empty list to disk
        save_data_to_file()

# ==============================================================================
# MAIN GUI WINDOW SETUP
# WHAT IT DOES: Builds the desktop application window layout and buttons
# WHY IT IS NEEDED: Provides an intuitive visual interface for the user and lecturer
# ==============================================================================

# Creates the primary root Tkinter window
root = tk.Tk()
# Sets window title bar text
root.title("Academic Countdown Tracker (Python Desktop Edition)")
# Sets default window dimensions (width x height in pixels)
root.geometry("880x680")
# Sets minimum window size so controls never get squished
root.minsize(780, 560)
# Sets pleasant light background color for main window
root.configure(bg="#f1f5f9")

# Header Frame: Holds application title and subtitle
header_frame = tk.Frame(root, bg="#f1f5f9", pady=10)
# Packs header frame at top of window with horizontal fill
header_frame.pack(fill=tk.X)

# Main Title Label: Large bold heading
title_label = tk.Label(header_frame, text="Academic Countdown Tracker", font=("Segoe UI", 18, "bold"), fg="#1e3a8a", bg="#f1f5f9")
# Packs title label
title_label.pack()

# Subtitle Label: Describes covered categories
subtitle_label = tk.Label(header_frame, text="Track Lectures, Tests, Examinations, & Assignment Deadlines with Real-Time Alarms", font=("Segoe UI", 9), fg="#64748b", bg="#f1f5f9")
# Packs subtitle label
subtitle_label.pack()

# Form Frame: Grouped frame containing all input fields to add a new event
form_frame = tk.LabelFrame(root, text=" Add New Academic Event / Deadline ", font=("Segoe UI", 10, "bold"), fg="#0f172a", bg="#ffffff", padx=16, pady=12)
# Packs form frame with padding
form_frame.pack(fill=tk.X, padx=16, pady=6)

# Category Label and Dropdown Combobox
tk.Label(form_frame, text="Category *:", font=("Segoe UI", 9, "bold"), bg="#ffffff").grid(row=0, column=0, sticky=tk.W, pady=4)
# Variable holding chosen category
category_entry_var = tk.StringVar(value="Lecture")
# Dropdown menu for category selection
category_combobox = ttk.Combobox(form_frame, textvariable=category_entry_var, state="readonly", values=["Lecture", "Test", "Examination", "Assignment"])
# Positions category combobox
category_combobox.grid(row=0, column=1, sticky=tk.EW, padx=8, pady=4)

# Course Title Label and Text Entry Box
tk.Label(form_frame, text="Title / Course *:", font=("Segoe UI", 9, "bold"), bg="#ffffff").grid(row=0, column=2, sticky=tk.W, pady=4)
# Text entry box for course name
title_entry = tk.Entry(form_frame, font=("Segoe UI", 9))
# Positions title entry box
title_entry.grid(row=0, column=3, sticky=tk.EW, padx=8, pady=4)

# Venue / Notes Label and Text Entry Box
tk.Label(form_frame, text="Venue / Notes:", font=("Segoe UI", 9), bg="#ffffff").grid(row=1, column=0, sticky=tk.W, pady=4)
# Text entry box for venue
venue_entry = tk.Entry(form_frame, font=("Segoe UI", 9))
# Positions venue entry box
venue_entry.grid(row=1, column=1, sticky=tk.EW, padx=8, pady=4)

# Date Label and Text Entry Box (Defaulting to today's date)
tk.Label(form_frame, text="Date (YYYY-MM-DD) *:", font=("Segoe UI", 9, "bold"), bg="#ffffff").grid(row=1, column=2, sticky=tk.W, pady=4)
# Gets current date formatted as YYYY-MM-DD
today_str = datetime.now().strftime("%Y-%m-%d")
# Date entry box with today's date prefilled
date_entry = tk.Entry(form_frame, font=("Segoe UI", 9))
# Inserts today's date as helpful default
date_entry.insert(0, today_str)
# Positions date entry box
date_entry.grid(row=1, column=3, sticky=tk.EW, padx=8, pady=4)

# Time Label and Text Entry Box
tk.Label(form_frame, text="Time (HH:MM 24hr) *:", font=("Segoe UI", 9, "bold"), bg="#ffffff").grid(row=2, column=0, sticky=tk.W, pady=4)
# Time entry box
time_entry = tk.Entry(form_frame, font=("Segoe UI", 9))
# Prefills with a sample time
time_entry.insert(0, "12:00")
# Positions time entry box
time_entry.grid(row=2, column=1, sticky=tk.EW, padx=8, pady=4)

# Add Button: Triggers handle_add_item on click
add_button = tk.Button(form_frame, text="+ Add Countdown Item", font=("Segoe UI", 9, "bold"), bg="#2563eb", fg="#ffffff", padx=12, pady=4, command=handle_add_item)
# Positions add button across remaining column
add_button.grid(row=2, column=2, columnspan=2, sticky=tk.EW, padx=8, pady=6)

# Configures column weights so entry inputs expand proportionally
form_frame.columnconfigure(1, weight=1)
form_frame.columnconfigure(3, weight=1)

# Controls & Filter Bar Frame
controls_frame = tk.Frame(root, bg="#f1f5f9", padx=16, pady=4)
# Packs controls frame
controls_frame.pack(fill=tk.X)

# Filter by Category Label
tk.Label(controls_frame, text="Filter Category:", font=("Segoe UI", 9, "bold"), bg="#f1f5f9").pack(side=tk.LEFT)
# Variable holding category filter selection
category_filter_var = tk.StringVar(value="All")
# Category filter combobox
category_filter_cb = ttk.Combobox(controls_frame, textvariable=category_filter_var, state="readonly", width=14, values=["All", "Lecture", "Test", "Examination", "Assignment"])
# Packs category filter combobox
category_filter_cb.pack(side=tk.LEFT, padx=6)

# Filter by Status Label
tk.Label(controls_frame, text="Filter Status:", font=("Segoe UI", 9, "bold"), bg="#f1f5f9").pack(side=tk.LEFT, padx=(12, 0))
# Variable holding status filter selection
status_filter_var = tk.StringVar(value="All")
# Status filter combobox
status_filter_cb = ttk.Combobox(controls_frame, textvariable=status_filter_var, state="readonly", width=14, values=["All", "Upcoming", "Starting Soon", "Passed"])
# Packs status filter combobox
status_filter_cb.pack(side=tk.LEFT, padx=6)

# Test Sound Alarm Button: Lets student preview alarm for lecturer
test_sound_btn = tk.Button(controls_frame, text="🔊 Test Alarm", font=("Segoe UI", 9), bg="#0d9488", fg="#ffffff", command=trigger_alarm_sound)
# Packs test alarm button
test_sound_btn.pack(side=tk.LEFT, padx=10)

# Delete Selected Item Button
delete_btn = tk.Button(controls_frame, text="Delete Selected", font=("Segoe UI", 9), bg="#ef4444", fg="#ffffff", command=handle_delete_selected)
# Packs delete button to right side
delete_btn.pack(side=tk.RIGHT, padx=4)

# Clear All Items Button
clear_all_btn = tk.Button(controls_frame, text="Clear All", font=("Segoe UI", 9), bg="#64748b", fg="#ffffff", command=handle_clear_all)
# Packs clear all button to right side
clear_all_btn.pack(side=tk.RIGHT, padx=4)

# Table Frame: Holds the Treeview countdown table
table_frame = tk.Frame(root, padx=16, pady=6, bg="#f1f5f9")
# Packs table frame expanding to fill remaining window space
table_frame.pack(fill=tk.BOTH, expand=True)

# Treeview Columns definition
columns = ("Category", "Title", "Venue", "Scheduled Time", "Status", "Countdown Remaining")
# Creates Treeview widget with defined columns
tree = ttk.Treeview(table_frame, columns=columns, show="headings")

# Sets column headings and column widths
tree.heading("Category", text="Category")
tree.column("Category", width=110, anchor=tk.CENTER)

tree.heading("Title", text="Course / Title")
tree.column("Title", width=220, anchor=tk.W)

tree.heading("Venue", text="Venue / Notes")
tree.column("Venue", width=160, anchor=tk.W)

tree.heading("Scheduled Time", text="Scheduled Date & Time")
tree.column("Scheduled Time", width=160, anchor=tk.CENTER)

tree.heading("Status", text="Status")
tree.column("Status", width=110, anchor=tk.CENTER)

tree.heading("Countdown Remaining", text="Countdown Clock")
tree.column("Countdown Remaining", width=160, anchor=tk.CENTER)

# Vertical Scrollbar for the table
scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
# Configures treeview to use scrollbar
tree.configure(yscroll=scrollbar.set)
# Packs scrollbar to right of table
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# Packs treeview table filling frame
tree.pack(fill=tk.BOTH, expand=True)

# Footer Summary Label: Displays active item counter
summary_label = tk.Label(root, text="Showing 0 of 0 total events", font=("Segoe UI", 9), fg="#64748b", bg="#f1f5f9", pady=6)
# Packs footer summary label
summary_label.pack()

# Loads any existing saved data from disk on startup
load_data_from_file()

# Starts the live 1-second countdown refresh loop
refresh_items_display()

# Starts the Tkinter main event listening loop to display GUI
root.mainloop()
