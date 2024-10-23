"""
 * This file is part of Jira Logger App.
 *
 * Jira Logger App is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Jira Logger App is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with Jira Logger App. If not, see <http://www.gnu.org/licenses/>.
"""

import tkinter as tk
from tkinter import Tk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from api import JiraAPI
from color_scheme import Color
from custom_style import CustomStyle
from datetime import datetime
import pytz, webbrowser
from use_json import data

class JiraLoggerApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x560")
        self.master.overrideredirect(True)
        self.set_window_position(1300, 120)

        # Initialize files
        self.jira_api = JiraAPI()
        self.custom_style = CustomStyle()
        self.color = Color()
        self.data = data

        self.master.wm_attributes("-transparentcolor", "#FBF5DF")

        # Create the canvas
        self.canvas = tk.Canvas(self.master, bg="#FBF5DF", highlightthickness=0, borderwidth=0)
        self.canvas.pack(expand=True, fill='both')

        # Draw a rounded rectangle on the canvas that fills the window
        self.rounded_rect = self.create_rounded_rectangle(20, 0, 380, 560, 10, fill=self.color.secondary_bg)

        # Create an outer frame that will hold all the widgets
        self.outer_frame = tk.Frame(self.canvas, bg=self.color.secondary_bg, borderwidth=0, width=50, padx=5)
        self.canvas.create_window((200, 255 + 20), window=self.outer_frame)

        # Title frame
        self.title_frame = tk.Frame(self.outer_frame, bg=self.color.secondary_bg, borderwidth=0)
        self.title_frame.pack(fill=tk.X)

        # Title label
        self.title_label = tk.Label(self.title_frame, text="Ticket Manager", bg=self.color.secondary_bg, fg="#0D92F4", font=("Arial", 16))
        self.title_label.pack(side=tk.LEFT, padx=5, pady=10)

        # Close button setup
        self.original_icon = Image.open("close.png")
        self.resized_icon = self.original_icon.resize((20, 20), Image.LANCZOS)
        self.close_icon = ImageTk.PhotoImage(self.resized_icon)

        self.close_button = tk.Button(self.title_frame, image=self.close_icon, bg=self.color.secondary_bg, borderwidth=0, command=self.close_window)
        self.close_button.pack(side="right", padx=5, pady=10)
        self.close_button.configure(cursor="hand2")

        # Create a frame for the notebook inside the outer frame
        self.frame = ttk.Frame(self.outer_frame, style="Custom.TFrame")
        self.frame.pack(expand=True, fill='both')

        # Create a Notebook and style it
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(expand=True, fill='both')

        self.custom_style.apply_style()

        # Create frames for each tab with the custom style
        self.search_frame = ttk.Frame(self.notebook, style="CustomFrame.TFrame")
        self.search_frame.configure(padding=5)
        self.time_log_frame = ttk.Frame(self.notebook, style="CustomFrame.TFrame")
        self.create_ticket = ttk.Frame(self.notebook, style="CustomFrame.TFrame")
        self.comment_ticket = ttk.Frame(self.notebook, style="CustomFrame.TFrame")

        # Add frames to the notebook
        self.notebook.add(self.search_frame, text="Search")
        self.notebook.add(self.time_log_frame, text="Log Time")
        self.notebook.add(self.create_ticket, text="Create Ticket")
        self.notebook.add(self.comment_ticket, text="Comment Ticket")

        self.setup_search_ui()
        self.setup_time_log_ui()
        self.setup_create_ticket_ui()
        self.setup_comment_ticket_ui()

        # Bind mouse events for dragging the window
        self.title_frame.bind("<ButtonPress-1>", self.on_press)
        self.title_frame.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def setup_search_ui(self):
        # Create a frame to hold the label and help icon together
        self.jql_frame = tk.Frame(self.search_frame, bg=self.color.primary_bg)
        
        # Search Query Label
        self.jql_label = tk.Label(self.jql_frame, text="Enter your JQL query:", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        
        # Help Icon Setup
        self.help_icon = Image.open("help.png")
        self.resized_help_icon = self.help_icon.resize((15, 15), Image.LANCZOS)
        self.help_icon_photo = ImageTk.PhotoImage(self.resized_help_icon)

        self.help_label = tk.Label(self.jql_frame, image=self.help_icon_photo, bg=self.color.primary_bg, cursor="hand2")
        self.help_label.bind("<Button-1>", lambda e: webbrowser.open(self.data['jira-help-link']))

        self.jql_label.pack(side=tk.LEFT, padx=(100, 0))
        self.help_label.pack(side=tk.RIGHT, padx=(0, 70))

        self.jql_frame.pack(pady=(15, 2), fill=tk.X, padx=5)

        self.jql_entry = tk.Text(self.search_frame, width=40, height=3, pady=5, padx=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")
        
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.perform_jql_search, padding=(10, 5))
        self.search_button.configure(cursor="hand2")

        # Pack the JQL Entry and Search Button
        self.jql_entry.pack(pady=2)
        self.search_button.pack(pady=20)

    
    def perform_jql_search(self):
        jql_query = self.jql_entry.get("1.0", tk.END).strip()
        
        if not jql_query:
            messagebox.showerror("Error", "JQL query cannot be empty.")
            return
        try:
            issues = self.jira_api.search_jira(jql_query)
            self.display_search_results(issues)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_search_results(self, issues):
        results_window = tk.Toplevel(self.master)
        results_window.title("Search Results")
        results_window.geometry("500x500+700+120")
        results_window.configure(bg=self.color.primary_bg)

        # Add a search bar for filtering results
        search_label = tk.Label(results_window, text="Filter Results:", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        search_label.pack(pady=(10, 10))

        # Customize the search entry to make it flat
        search_entry = ttk.Entry(results_window)
        search_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Style the Entry widget to be flat
        entry_style = ttk.Style()
        entry_style.configure("TEntry", relief='flat', borderwidth=0, background=self.color.secondary_bg, foreground=self.color.quaternary_fg, padding=5)
        search_entry.configure(style="TEntry")

        total_results_label = tk.Label(results_window, text=f"Total Results: {len(issues)}", bg=self.color.primary_bg, fg="#A39BBA")
        total_results_label.pack(pady=(5, 5))

        # Listbox to display the results
        results_listbox = tk.Listbox(results_window, height=15, bg=self.color.secondary_bg, fg=self.color.secondary_fg)
        results_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for issue in issues:
            results_listbox.insert(tk.END, issue)

        def update_total_results(count):
            total_results_label.config(text=f'Total Results: {count}')

        def filter_results(event):
            search_term = search_entry.get().lower()
            results_listbox.delete(0, tk.END)
            filtered_issues = []
            for issue in issues:
                if search_term in issue.lower():
                    results_listbox.insert(tk.END, issue)
                    filtered_issues.append(issue)
            
            update_total_results(len(filtered_issues))

        search_entry.bind("<KeyRelease>", filter_results)

        def on_issue_select(event):
            selected_index = results_listbox.curselection()
            if selected_index:
                selected_issue = results_listbox.get(selected_index)
                self.jira_api.redirect_to_jira_issue(selected_issue)

        results_listbox.bind("<<ListboxSelect>>", on_issue_select)


    def setup_time_log_ui(self):
        self.issue_key_label = tk.Label(self.time_log_frame, text="Enter Issue Key (e.g., PRD-123):", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        self.issue_key_entry = tk.Text(self.time_log_frame, width=20, height=1, pady=5, padx=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")

        self.fetch_issue_button = ttk.Button(self.time_log_frame, text="Fetch Issue", command=self.fetch_issue)
        self.fetch_issue_button.configure(cursor="hand2")
        self.success_message_label = tk.Label(self.time_log_frame, text="", fg="green", bg=self.color.primary_bg)

        # Time and Comment Inputs
        self.time_label = tk.Label(self.time_log_frame, text="Time Spent (e.g., 1h 30m):", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        self.time_entry = tk.Text(self.time_log_frame, width=20, height=1, pady=5, padx=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")

        self.time_started_label = tk.Label(self.time_log_frame, text="Time Started (e.g., YYYY-MM-DD HH:MM):", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        self.date_started_entry = tk.Text(self.time_log_frame, width=20, height=1, pady=5, padx=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")
        self.time_started_entry = tk.Text(self.time_log_frame, width=20, height=1, pady=5, padx=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")

        self.comment_label = tk.Label(self.time_log_frame, text="Work Description:", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        self.log_comment_entry = tk.Text(self.time_log_frame, width=40, height=5, padx=5, pady=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")

        self.perform_button = ttk.Button(self.time_log_frame, text="Create", command=self.log_time_on_existing_ticket, padding=(10, 5))
        self.perform_button.pack(side=tk.BOTTOM, pady=(2, 20))
        self.perform_button.configure(cursor="hand2")

        # Pack all relevant widgets for time logging
        self.issue_key_label.pack(pady=(15, 2))
        self.issue_key_entry.pack(pady=5)
        self.fetch_issue_button.pack(pady=5)
        self.time_label.pack(pady=2)
        self.time_entry.pack(pady=5)

        self.time_started_label.pack(pady=2)
        self.date_started_entry.pack(pady=2)
        self.time_started_entry.pack(pady=5)

        self.comment_label.pack(pady=2)
        self.log_comment_entry.pack(pady=5)
        self.success_message_label.pack(pady=5)

    def setup_create_ticket_ui(self):
        # Labels and Entries for creating a new ticket
        self.project_key_label = tk.Label(self.create_ticket, text="Enter Project Key (e.g., PRD):", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        self.project_key_entry = tk.Text(self.create_ticket, width=20, height=1, pady=5, padx=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")

        self.issue_type_label = tk.Label(self.create_ticket, text="Enter Issue Type (e.g., Bug):", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        self.issue_type_entry = tk.Text(self.create_ticket, width=20, height=1, pady=5, padx=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")

        self.summary_label = tk.Label(self.create_ticket, text="Summary:", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        self.summary_entry = tk.Text(self.create_ticket, width=40, height=1, padx=5, pady=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")

        self.description_label = tk.Label(self.create_ticket, text="Description:", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        self.description_entry = tk.Text(self.create_ticket, width=40, height=5, padx=5, pady=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")

        self.perform_button = ttk.Button(self.create_ticket, text="Create", command=self.create_new_ticket, padding=(10, 5))
        self.perform_button.pack(side=tk.BOTTOM, pady=(2, 20))
        self.perform_button.configure(cursor="hand2")

        self.created_issue_label = tk.Label(self.create_ticket, text="", fg="green", bg=self.color.primary_bg, width=40)

        # Pack all relevant widgets for time logging
        self.project_key_label.pack(pady=(15, 2))
        self.project_key_entry.pack(pady=5)
        self.issue_type_label.pack(pady=2)
        self.issue_type_entry.pack(pady=5)
        self.summary_label.pack(pady=2)
        self.summary_entry.pack(pady=5)
        self.description_label.pack(pady=2)
        self.description_entry.pack(pady=5)
        self.created_issue_label.pack(pady=5)

    def setup_comment_ticket_ui(self):
        self.comment_issue_key_label = tk.Label(self.comment_ticket, text="Enter Issue Key (e.g., PRD-123):", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        self.comment_issue_key_entry = tk.Text(self.comment_ticket, width=20, height=1, pady=5, padx=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")

        self.comment_fetch_issue_button = ttk.Button(self.comment_ticket, text="Fetch Issue", command=self.comment_fetch_issue)
        self.comment_fetch_issue_button.configure(cursor="hand2")

        self.comment_label = tk.Label(self.comment_ticket, text="Comment:", bg=self.color.primary_bg, fg=self.color.secondary_fg)
        self.comment_entry = tk.Text(self.comment_ticket, width=40, height=5, padx=5, pady=5, bg=self.color.secondary_bg, fg=self.color.secondary_fg, borderwidth=0, relief="flat")

        self.perform_button = ttk.Button(self.comment_ticket, text="Add Comment", command=self.add_comment_to_issue, padding=(10, 5))
        self.perform_button.pack(side=tk.BOTTOM, pady=(2, 20))
        self.perform_button.configure(cursor="hand2")

        self.comment_success_message_label = tk.Label(self.comment_ticket, text="", fg="green", bg=self.color.primary_bg)

        self.comment_issue_key_label.pack(pady=(15, 2))
        self.comment_issue_key_entry.pack(pady=5)
        self.comment_fetch_issue_button.pack(pady=5)
        self.comment_label.pack(pady=2)
        self.comment_entry.pack(pady=5)
        self.comment_success_message_label.pack(pady=5)

    def fetch_issue(self):
        issue_key = self.issue_key_entry.get("1.0", tk.END).strip()
        if not issue_key:
            messagebox.showerror("Error", "Issue key cannot be empty.")
            return
        try:
            issue = self.jira_api.search_jira_issues(issue_key)
            if issue:
                self.success_message_label.config(text=f"Issue {issue_key} fetched successfully!")
            else:
                messagebox.showerror("Error", f"Issue {issue_key} not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def comment_fetch_issue(self):
        issue_key = self.comment_issue_key_entry.get("1.0", tk.END).strip()
        if not issue_key:
            messagebox.showerror("Error", "Issue key cannot be empty.")
            return
        try:
            issue = self.jira_api.search_jira_issues(issue_key)
            if issue:
                self.comment_success_message_label.config(text=f"Issue {issue_key} fetched successfully!")
            else:
                messagebox.showerror("Error", f"Issue {issue_key} not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_comment_to_issue(self):
        issue_key = self.comment_issue_key_entry.get("1.0", tk.END).strip()
        comment_text = self.comment_entry.get("1.0", tk.END).strip()

        if not issue_key or not comment_text:
            messagebox.showerror("Error", "Issue key and comment cannot be empty.")
            return
        try:
            response = self.jira_api.add_comment(issue_key, comment_text)
            if response:
                self.comment_success_message_label.config(text=f"Comment added to {issue_key} successfully!")
            else:
                messagebox.showerror("Error", f"Failed to add comment to {issue_key}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def log_time_on_existing_ticket(self):
        issue_key = self.issue_key_entry.get("1.0", tk.END).strip()
        time_spent = self.time_entry.get("1.0", tk.END).strip()
        work_description = self.log_comment_entry.get("1.0", tk.END).strip()

        time_started_date = self.date_started_entry.get("1.0", tk.END).strip()
        time_started_time = self.time_started_entry.get("1.0", tk.END).strip()

        if not issue_key or not time_spent:
            messagebox.showerror("Error", "Issue key and time spent cannot be empty.")
            return

        try:
            local_tz = pytz.timezone('Asia/Manila')

            if time_started_date and time_started_time:
                time_started = f"{time_started_date} {time_started_time}"
                time_started = datetime.strptime(time_started, "%Y-%m-%d %H:%M")
                time_started = local_tz.localize(time_started)
            elif time_started_date:
                time_started = f"{time_started_date} 00:00"
                time_started = datetime.strptime(time_started, "%Y-%m-%d %H:%M")
                time_started = local_tz.localize(time_started)
            elif time_started_time:
                today_date = datetime.now().strftime("%Y-%m-%d")
                time_started = f"{today_date} {time_started_time}"
                time_started = datetime.strptime(time_started, "%Y-%m-%d %H:%M")
                time_started = local_tz.localize(time_started)
            else:
                time_started = datetime.now(local_tz)

            time_started_utc = time_started.astimezone(pytz.utc)
            time_started_str = time_started_utc.strftime("%Y-%m-%dT%H:%M:%S.000+0000")

            self.jira_api.log_time(issue_key, time_spent, work_description, time_started_str)
            
            self.success_message_label.config(text=f"Time logged successfully for issue {issue_key}")

        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid date or time format: {ve}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_new_ticket(self):
        project_key = self.project_key_entry.get("1.0", tk.END).strip()
        issue_type = self.issue_type_entry.get("1.0", tk.END).strip()
        summary = self.summary_entry.get("1.0", tk.END).strip()
        description = self.description_entry.get("1.0", tk.END).strip()

        if not project_key or not issue_type or not summary:
            messagebox.showerror("Error", "All fields are required to create a new ticket.")
            return

        try:
            issue_key = self.jira_api.create_jira_issue(summary, description, issue_type, project_key)
            self.created_issue_label.config(text=f"Issue {issue_key} created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def close_window(self):
        self.master.destroy()

    def set_window_position(self, x, y):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def on_press(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        x = self.master.winfo_x() - self.x + event.x
        y = self.master.winfo_y() - self.y + event.y
        self.master.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = Tk()
    app = JiraLoggerApp(root)
    root.mainloop()
