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
        self.subject_label = ctk.CTkLabel(self, text="Subject: ", font=self.label_font)
        self.subject_label.pack(fill="both", expand=True)
        self.from_label = ctk.CTkLabel(self, text="From: ", font=self.label_font)
        self.from_label.pack(fill="both", expand=True)
        self.to_label = ctk.CTkLabel(self, text="To: ", font=self.label_font)
        self.to_label.pack()
        self.date_label = ctk.CTkLabel(self, text="Date: ", font=self.label_font)
        self.date_label.pack()
        self.body_textbox = ctk.CTkTextbox(self, height=500, font=self.label_font)
        self.body_textbox.pack(pady=10, fill="both", expand=True)

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

