# email_sender.py
import os
from gmail_api_sender import gmail_login, send_email

class EmailSender:
    def __init__(self):
        # do NOT call gmail_login() here (lazy init)
        self.service = None
        self.resume_path = 'attachments/resume.pdf'
        # Skills from your resume (based on uploaded resume files)
        self.skill_keywords = {
            "c", "java", "python", "django", "jdbc", "hibernate",
            "html", "css", "bootstrap", "javascript", "react", "react.js",
            "firebase", "mysql", "angular", "laravel"
        }

    def _ensure_service(self):
        if self.service is None:
            self.service = gmail_login()

    def extract_skills(self, text):
        text_lower = text.lower()
        found = []
        for skill in self.skill_keywords:
            # use simple substring match, check word boundaries for languages with dot
            key = skill.lower()
            if key in text_lower and key not in found:
                found.append(skill)
        return found

    def build_subject(self, position):
        pos = position.strip()
        if pos == "":
            pos = "[Position]"
        # If user already provided a full subject, don't double-wrap
        if pos.lower().startswith("application for"):
            return pos
        return f"Application for {pos} - Sayed Gouse Jaheer"

    def send_job_application(self, hr_email, job_description, position):
        try:
            self._ensure_service()
            skills_found = self.extract_skills(job_description)
            skills_sentence = ", ".join(skills_found) if skills_found else "relevant web development skills"

            subject = self.build_subject(position)

            html_body = f"""
            <p>Dear Hiring Manager,</p>
            <p>I am eager to bring my knowledge of {skills_sentence} and my passion for building efficient, user-friendly applications to your team. Through my academic projects and internships, I gained hands-on experience developing responsive web applications, solving real problems, and adapting quickly to new tools and workflows.</p>
            <p>As a quick learner and motivated fresher, I am confident in my ability to contribute value from day one and continue growing under the guidance of experienced colleagues. I write clean, maintainable code and approach challenges with a practical, problem-solving mindset.</p>
            <p>Please find my resume attached for your consideration. I would welcome the opportunity to discuss how I can contribute to your team.</p>
            <p>Thank you for your time and consideration.</p>
            <p>Best regards,<br>Sayed Gouse Jaheer<br>+91 9398611047<br>gousezahir100@gmail.com</p>
            """

            send_email(
                self.service,
                to=hr_email,
                subject=subject,
                html_body=html_body,
                attachment_path=self.resume_path
            )
            return True, "Email with resume sent successfully via Gmail API!"
        except Exception as e:
            return False, f"Error sending email via Gmail API: {str(e)}"
