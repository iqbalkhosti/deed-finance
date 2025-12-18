"""
Email utilities for Deed Leisure.
Handles verification code generation and email sending.
In development mode, codes are printed to console instead of sent via email.
"""
import random
import string
from datetime import datetime, timedelta
from flask import current_app
from flask_mail import Mail, Message

mail = Mail()

# Development mode flag - set to False when you have SMTP configured
DEV_MODE = True


def generate_verification_code():
    """Generate a 6-digit verification code."""
    return ''.join(random.choices(string.digits, k=6))


def get_code_expiry():
    """Get expiration time for verification code (10 minutes from now)."""
    return datetime.utcnow() + timedelta(minutes=10)


def send_verification_email(email, code, first_name):
    """
    Send verification email with 6-digit code.
    In DEV_MODE, prints to console instead of sending email.
    """
    if DEV_MODE:
        print("\n" + "=" * 50)
        print("📧 VERIFICATION EMAIL (Dev Mode)")
        print("=" * 50)
        print(f"To: {email}")
        print(f"Subject: Verify your Deed account")
        print("-" * 50)
        print(f"Hi {first_name},")
        print(f"\nYour verification code is: {code}")
        print(f"\nThis code expires in 10 minutes.")
        print("=" * 50 + "\n")
        return True
    
    # Production email sending
    try:
        msg = Message(
            subject="Verify your Deed account",
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@deed.com'),
            recipients=[email]
        )
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #667eea;">Welcome to Deed!</h2>
            <p>Hi {first_name},</p>
            <p>Your verification code is:</p>
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; 
                        font-size: 32px; 
                        font-weight: bold; 
                        text-align: center; 
                        padding: 20px; 
                        border-radius: 10px; 
                        letter-spacing: 8px;
                        margin: 20px 0;">
                {code}
            </div>
            <p style="color: #666;">This code expires in 10 minutes.</p>
            <p style="color: #999; font-size: 12px;">
                If you didn't create an account with Deed, please ignore this email.
            </p>
        </div>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
