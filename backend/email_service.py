import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional
import logging
from models import ContactRequest

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("EMAIL_PORT", "587"))
        self.email_user = os.getenv("EMAIL_USER", "contact@emptymug.fr")
        self.email_password = os.getenv("EMAIL_PASSWORD", "")
        
    async def send_contact_email(self, contact_data: ContactRequest) -> bool:
        """Send contact form email to contact@emptymug.fr"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.email_user
            msg["To"] = "contact@emptymug.fr"
            msg["Subject"] = f"New Contact Form Submission from {contact_data.fullName}"
            
            # Create HTML body
            html_body = self._create_email_template(contact_data)
            msg.attach(MIMEText(html_body, "html"))
            
            # Send email
            await aiosmtplib.send(
                msg,
                hostname=self.smtp_host,
                port=self.smtp_port,
                start_tls=True,
                username=self.email_user,
                password=self.email_password,
            )
            
            logger.info(f"Contact email sent successfully for {contact_data.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send contact email: {str(e)}")
            return False
    
    def _create_email_template(self, contact_data: ContactRequest) -> str:
        """Create formatted HTML email template"""
        phone_info = ""
        if contact_data.phoneNumber:
            phone_info = f"""
            <tr>
                <td style="padding: 8px 0; font-weight: bold; color: #374151;">Phone:</td>
                <td style="padding: 8px 0; color: #4b5563;">{contact_data.countryCode} {contact_data.phoneNumber}</td>
            </tr>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>New Contact Form Submission</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">New Contact Form Submission</h1>
                <p style="color: #e0f2fe; margin: 10px 0 0 0; font-size: 16px;">From EmptyMug Website</p>
            </div>
            
            <div style="background: #fff; padding: 30px; border: 1px solid #e5e7eb; border-top: none; border-radius: 0 0 10px 10px;">
                <h2 style="color: #1f2937; margin-top: 0; font-size: 22px;">Contact Details</h2>
                
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold; color: #374151; width: 100px;">Name:</td>
                        <td style="padding: 8px 0; color: #4b5563;">{contact_data.fullName}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold; color: #374151;">Email:</td>
                        <td style="padding: 8px 0; color: #4b5563;"><a href="mailto:{contact_data.email}" style="color: #0ea5e9; text-decoration: none;">{contact_data.email}</a></td>
                    </tr>
                    {phone_info}
                </table>
                
                <h3 style="color: #1f2937; margin-top: 25px; margin-bottom: 10px; font-size: 18px;">Message</h3>
                <div style="background: #f9fafb; padding: 20px; border-radius: 8px; border-left: 4px solid #0ea5e9;">
                    <p style="margin: 0; color: #4b5563; white-space: pre-line;">{contact_data.message}</p>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 14px;">
                    <p style="margin: 0;">This email was sent from the contact form on <strong>emptymug.fr</strong></p>
                    <p style="margin: 5px 0 0 0;">Please reply directly to this email to respond to the inquiry.</p>
                </div>
            </div>
        </body>
        </html>
        """

# Global email service instance
email_service = EmailService()
