import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_username = os.getenv('EMAIL_USERNAME')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        
        if not all([self.email_username, self.email_password]):
            logging.warning("Email credentials not configured - emails will be logged only")
    
    def send_ticket_feedback(self, ticket_data, analysis_result, recipient_emails):
        """Send feedback email about ticket quality"""
        try:
            subject = f"Ticket Quality Feedback: {ticket_data['key']} - {ticket_data['summary'][:50]}..."
            body = self._build_email_body(ticket_data, analysis_result)
            
            if not self.email_username or not self.email_password:
                # Log email instead of sending for MVP
                logging.info(f"Email would be sent to: {recipient_emails}")
                logging.info(f"Subject: {subject}")
                logging.info(f"Body:\n{body}")
                return True
            
            return self._send_email(recipient_emails, subject, body)
            
        except Exception as e:
            logging.error(f"Error sending feedback email: {str(e)}")
            return False
    
    def _build_email_body(self, ticket_data, analysis_result):
        """Build email body with ticket feedback"""
        return f"""
        Hello,
        
        The automated ticket quality checker has analyzed ticket {ticket_data['key']} and found some areas for improvement.
        
        Ticket Details:
        - Title: {ticket_data['summary']}
        - Type: {ticket_data['issue_type']}
        - Reporter: {ticket_data['reporter']}
        - Quality Score: {analysis_result['quality_score']}/10
        
        Issues Found:
        {chr(10).join(f"• {issue}" for issue in analysis_result['issues'])}
        
        Suggested Improvements:
        {chr(10).join(f"• {suggestion}" for suggestion in analysis_result['suggestions'])}
        
        Summary: {analysis_result['summary']}
        
        Please update the ticket with the suggested improvements to help the development team better understand the requirements.
        
        View ticket: {os.getenv('JIRA_URL', 'https://your-jira-instance.com')}/browse/{ticket_data['key']}
        
        Best regards,
        Automated Ticket Quality Checker
        """
    
    def _send_email(self, recipients, subject, body):
        """Send email via SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_username
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_username, self.email_password)
            server.send_message(msg)
            server.quit()
            
            logging.info(f"Email sent successfully to: {recipients}")
            return True
            
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            return False