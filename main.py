import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
from email_sender import EmailSender
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class JobApplicationApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Automated Job Application Sender")
        self.window.geometry("800x800")

        self.email_sender = EmailSender()
        self.resume_path = "attachments/resume.pdf"

        self.setup_ui()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        title_label = ctk.CTkLabel(
            main_frame,
            text="Automated Job Application Sender",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))

        email_label = ctk.CTkLabel(main_frame, text="HR Email Address:")
        email_label.pack(anchor="w", padx=40, pady=(10, 5))

        self.email_entry = ctk.CTkEntry(
            main_frame,
            width=400,
            placeholder_text="hr@company.com"
        )
        self.email_entry.pack(pady=(0, 20))

        subject_label = ctk.CTkLabel(main_frame, text="Email Subject:")
        subject_label.pack(anchor="w", padx=40, pady=(10, 5))

        self.subject_entry = ctk.CTkEntry(
            main_frame,
            width=400,
            placeholder_text="Application for [Position] - [Your Name]"
        )
        self.subject_entry.pack(pady=(0, 20))

        job_desc_label = ctk.CTkLabel(main_frame, text="Job Description:")
        job_desc_label.pack(anchor="w", padx=40, pady=(10, 5))

        self.job_desc_text = ctk.CTkTextbox(
            main_frame,
            width=600,
            height=200
        )
        self.job_desc_text.pack(pady=(0, 20))

        resume_frame = ctk.CTkFrame(main_frame)
        resume_frame.pack(pady=(0, 20), fill="x", padx=40)

        self.resume_label = ctk.CTkLabel(
            resume_frame,
            text=f"Resume: {os.path.basename(self.resume_path)}"
        )
        self.resume_label.pack(side="left", padx=10, pady=10)

        browse_button = ctk.CTkButton(
            resume_frame,
            text="Browse",
            command=self.browse_resume,
            width=100
        )
        browse_button.pack(side="right", padx=10, pady=10)

        send_button = ctk.CTkButton(
            main_frame,
            text="Send Application",
            command=self.send_application,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        send_button.pack(pady=30)

        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Ready to send applications",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(0, 20))

    def browse_resume(self):
        filename = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.resume_path = filename
            self.resume_label.configure(text=f"Resume: {os.path.basename(filename)}")
            self.email_sender.resume_path = filename

    def send_application(self):
        hr_email = self.email_entry.get().strip()
        subject = self.subject_entry.get().strip()
        job_description = self.job_desc_text.get("1.0", "end-1c").strip()

        if not hr_email or not job_description:
            messagebox.showerror("Error", "Please fill in all required fields!")
            return

        if "@" not in hr_email:
            messagebox.showerror("Error", "Please enter a valid email address!")
            return

        if not messagebox.askyesno("Confirm", f"Send application to {hr_email}?"):
            return

        self.status_label.configure(text="Sending email...")
        self.window.update()

        thread = threading.Thread(
            target=self.send_email_thread,
            args=(hr_email, job_description, subject)
        )
        thread.daemon = True
        thread.start()

    def send_email_thread(self, hr_email, job_description, subject):
        success, message = self.email_sender.send_job_application(
            hr_email, job_description, subject
        )
        self.window.after(0, self.update_status, success, message)

    def update_status(self, success, message):
        if success:
            self.status_label.configure(text="✅ Email sent successfully!")
            messagebox.showinfo("Success", message)
            self.email_entry.delete(0, "end")
            self.job_desc_text.delete("1.0", "end")
        else:
            self.status_label.configure(text="❌ Failed to send email")
            messagebox.showerror("Error", message)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = JobApplicationApp()
    app.run()
