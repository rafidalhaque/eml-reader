# main.py
import customtkinter as ctk
import pathlib
import parse_email
import ui_design


project_root = pathlib.Path(__file__).parent


app = ctk.CTk()

def open_file(widgets):
    file_path = ctk.filedialog.askopenfilename(filetypes=[("Email files", "*.eml")])
    if file_path:
        email_data = parse_email.parse_email(file_path)
        widgets["subject_label"].configure(text=f"Subject: {email_data['subject']}")
        widgets["from_label"].configure(text=f"From: {email_data['from']}")
        widgets["to_label"].configure(text=f"To: {email_data['to']}")
        widgets["date_label"].configure(text=f"Date: {email_data['date']}")
        widgets["body_textbox"].configure(state="normal")
        widgets["body_textbox"].delete("1.0", "end")
        widgets["body_textbox"].insert("1.0", email_data['body'])
        widgets["body_textbox"].configure(state="disabled")


# import ui from ui_design.py
ui_design.main_ui(app)
ctk.set_default_color_theme(f"{project_root}/assets/theme.json")
ui_widgets = ui_design.email_ui(app)
ui_design.open_file_ui(app, ctk, open_file, ui_widgets)
app.mainloop()