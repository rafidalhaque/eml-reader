# ui_design.py
from cmath import exp
from textwrap import fill

import customtkinter as ctk
import parse_email

class EmailViewUI(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.email_ui()

    def email_ui(self):
        self.label_font = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        self.subject_label = ctk.CTkLabel(self, text="Subject: ", font=self.label_font, anchor="w")
        self.subject_label.pack(fill="x", expand=True)
        self.from_label = ctk.CTkLabel(self, text="From: ", font=self.label_font, anchor="w")
        self.from_label.pack(fill="x", expand=True)
        self.to_label = ctk.CTkLabel(self, text="To: ", font=self.label_font, anchor="w")
        self.to_label.pack(fill="x", expand=True)
        self.date_label = ctk.CTkLabel(self, text="Date: ", font=self.label_font, anchor="w")
        self.date_label.pack(fill="x", expand=True)
        self.body_textbox = ctk.CTkTextbox(self, height=500, font=self.label_font)
        self.body_textbox.pack(pady=10, fill="both", expand=True)
        self.body_textbox.configure(state="disabled")

    def update_email(self, email_data):
        self.subject_label.configure(text=f"Subject: {email_data['subject']}")
        self.from_label.configure(text=f"From: {email_data['from']}")
        self.to_label.configure(text=f"To: {email_data['to']}")
        self.date_label.configure(text=f"Date: {email_data['date']}")
        self.body_textbox.configure(state="normal")
        self.body_textbox.delete("1.0", "end")
        self.body_textbox.insert("1.0", email_data['body'])
        self.body_textbox.configure(state="disabled")

class RecentFilesView(ctk.CTkFrame):
    def __init__(self, master, on_file_select, **kwargs):
        super().__init__(master, **kwargs)
        self.on_file_select = on_file_select
        self.font_family = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        self.recent_files_frame = ctk.CTkScrollableFrame(self, label_text="Recent Files", fg_color="transparent", label_font=self.font_family, label_fg_color="transparent")
        self.recent_files_frame.pack(fill="both", expand=True)

    def populate_recent_files(self, recent_files):
        for widget in self.recent_files_frame.winfo_children():
            widget.destroy()

        for file in recent_files:
            id, filename, file_path, opened_at = file
            hidden_btn = ctk.CTkButton(
                self.recent_files_frame,
                text=f"{filename}\t\t{opened_at}\n{file_path}",
                font=(self.font_family, 13),
                command=lambda p=file_path: self.on_file_select(p)
            )
            hidden_btn.pack(fill="x", pady=5)

class ErrorDialogue(ctk.CTkToplevel):
    def __init__(self, parent, title="Error", message="An Error Occured", **kwargs):
        super().__init__(parent, **kwargs)
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        self.grab_set()

        self.label_font = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        self.message_label = ctk.CTkLabel(self, text=message, font=self.label_font, anchor="w", wraplength=300)
        self.message_label.pack(padx=20, pady=(20, 5),expand=True)
        self.ok_button = ctk.CTkButton(self, text="OK", font=self.label_font, command=self.destroy)
        self.ok_button.pack(pady=(0, 20))

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.geometry("400x300")
        self.label = ctk.CTkLabel(self, text="Top")
        self.label.pack(fill="x", expand=True)

    def show_error(self, title, message):
        ErrorDialogue(self, title=title, message=message)

