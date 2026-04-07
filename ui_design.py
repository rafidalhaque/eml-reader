# ui_design.py
from cmath import exp
from textwrap import fill

import customtkinter as ctk
import webbrowser

from tkinterweb import HtmlFrame


class EmailViewUI(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.email_ui()

    def email_ui(self):
        self.label_font = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        self.subject_label = ctk.CTkLabel(self, text="Subject: ", font=self.label_font, anchor="w")
        self.subject_label.pack(fill="x", expand=True, padx=10)
        self.from_label = ctk.CTkLabel(self, text="From: ", font=self.label_font, anchor="w")
        self.from_label.pack(fill="x", expand=True, padx=10)
        self.to_label = ctk.CTkLabel(self, text="To: ", font=self.label_font, anchor="w")
        self.to_label.pack(fill="x", expand=True, padx=10)
        self.date_label = ctk.CTkLabel(self, text="Date: ", font=self.label_font, anchor="w")
        self.date_label.pack(fill="x", expand=True, padx=10)
        self.body_html = HtmlFrame(self, messages_enabled=False)
        self.body_html.pack(padx=10, pady=10, fill="both", expand=True)

    def update_email(self, email_data):
        self.subject_label.configure(text=f"Subject: {email_data["subject"]}")
        self.from_label.configure(text=f"From: {email_data["from"]}")
        self.to_label.configure(text=f"To: {email_data["to"]}")
        self.date_label.configure(text=f"Date: {email_data["date"]}")
        self.body_html.load_html(email_data["body_html"])

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

class AboutDialogue(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Email Reader")
        self.geometry("400x300")
        self.resizable(True, True)
        self.grab_set()

        self.label_font = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        self.heading = ctk.CTkLabel(self, text="About Email Reader", font=(self.label_font, 18), anchor="n", wraplength=250)
        self.heading.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        self.text = """
        Email Reader is a GUI software build with python3 and customtkinter. It allows user to read .eml file. 
        """
        self.about_text = ctk.CTkLabel(self, text=self.text, font=self.label_font, wraplength=250, anchor="n", justify="left")
        self.about_text.grid(row=1, column=0, columnspan=2, pady=(20, 10))
        self.developer_btn = self.hyperlink_btn(parent=self, text="Developer: rafidalhaque", fg_color="blue", url="https://rafidalhaque.github.io")
        self.developer_btn.grid(row=2, column=0, padx=20, pady=5)
        self.github_repo = self.hyperlink_btn(parent=self, text="GitHub Repository", fg_color="black", url="https://github.com/rafidalhaque/eml-reader")
        self.github_repo.grid(row=2, column=1, padx=20, pady=5)

    def hyperlink_btn(self, parent, text, url, fg_color, **kwargs):
        return ctk.CTkButton(parent, text=text, font=self.label_font, fg_color=fg_color, command=lambda: webbrowser.open(url), **kwargs)

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

