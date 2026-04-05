# ui_design.py
import customtkinter as ctk
import parse_email

class EmailViewUI(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.email_ui()

    def email_ui(self):
        self.subject_label = ctk.CTkLabel(self, text="Subject: ")
        self.subject_label.pack()
        self.from_label = ctk.CTkLabel(self, text="From: ")
        self.from_label.pack()
        self.to_label = ctk.CTkLabel(self, text="To: ")
        self.to_label.pack()
        self.date_label = ctk.CTkLabel(self, text="Date: ")
        self.date_label.pack()
        self.body_textbox = ctk.CTkTextbox(self, width=380, height=200)
        self.body_textbox.pack(pady=10)

    def update_email(self, email_data):
        self.subject_label.configure(text=f"Subject: {email_data['subject']}")
        self.from_label.configure(text=f"From: {email_data['from']}")
        self.to_label.configure(text=f"To: {email_data['to']}")
        self.date_label.configure(text=f"Date: {email_data['date']}")
        self.body_textbox.configure(state="normal")
        self.body_textbox.delete("1.0", "end")
        self.body_textbox.insert("1.0", email_data['body'])
        self.body_textbox.configure(state="disabled")

