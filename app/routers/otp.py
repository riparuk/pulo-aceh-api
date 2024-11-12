from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyotp
import time
from fastapi import APIRouter, FastAPI, HTTPException, Depends
from pydantic import BaseModel
import smtplib

from sqlalchemy.orm import Session
from app.dependencies import SECRET_KEY, GMAIL_EMAIL, GMAIL_PASSWORD
from app.db.crud import create_otp, delete_otp_by_email, verify_otp_by_email
from app.db.database import get_db
from email_validator import validate_email, EmailNotValidError

SECRET = SECRET_KEY  # Rahasia OTP

router = APIRouter(
    prefix="/otp",
    tags=["otps"],
    responses={404: {"description": "Not Found"}}
)

def send_email(subject, body, recipient):
    password = GMAIL_PASSWORD
    sender = GMAIL_EMAIL
    # Create a multipart message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    message = body

    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.send_message(msg)
    print("Message sent!")
    
@router.post("/send-otp")
def send_otp(email: str, db: Session = Depends(get_db)):
    email = email.lower()
    try:
        # Validate email
        v = validate_email(email)
        email = v["email"]  # replace with normalized form
    except EmailNotValidError as e:
        # email is not valid, raise an exception
        raise HTTPException(status_code=400, detail=str(e))
    totp = pyotp.TOTP(SECRET)
    otp = totp.now()
    try:
        # Simpan OTP di database dengan expiry 30 detik
        create_otp(db=db, email=email, otp=otp, expires_in_minutes=2)
    except Exception as e:
        # Cetak atau log exception yang terjadi
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save OTP: {e}")
    
    # Kirim OTP ke email pengguna
    subject = "Pulo-Aceh OTP Code"
    body = f"Your OTP is {otp}."
    recipient = email
    
    send_email(subject, body, recipient)
    
    return {"message": "OTP sent successfully, 2 minutes expiry."}
    