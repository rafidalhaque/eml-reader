# ui_design.py
import customtkinter as ctk
import parse_email


def main_ui(app):
    x=1177
    y=625
    app.title("Email Reader")
    app.geometry(f"{x}x{y}")

def open_file_ui(app, ctk, open_file, widgets):
    open_file_btn = ctk.CTkButton(app, text="Open file", command=lambda: open_file(widgets))
    open_file_btn.pack(pady=100)

def email_ui(app):
    widgets = {}
    widgets["subject_label"] = ctk.CTkLabel(app, text="Subject: ")
    widgets["subject_label"].pack()
    widgets["from_label"] = ctk.CTkLabel(app, text="From: ")
    widgets["from_label"].pack()
    widgets["to_label"] = ctk.CTkLabel(app, text="To: ")
    widgets["to_label"].pack()
    widgets["date_label"] = ctk.CTkLabel(app, text="Date: ")
    widgets["date_label"].pack()
    widgets["body_textbox"] = ctk.CTkTextbox(app, width=380, height=200)
    widgets["body_textbox"].pack(pady=10)
    return widgets

# def main_theme(ctk, app):
#     ctk.set_default_color_theme(f"{project_root}/assets/theme.json")
#     open_file_btn = ctk.CTkButton(app, text="Open file", command=open_file)
#     open_file_btn.pack(pady=100)

