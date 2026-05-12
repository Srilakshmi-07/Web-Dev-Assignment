from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import csv
import os
from datetime import datetime


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what the incoming form data should look like
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: int
    country: str
    course: str


@app.post("/api/contact-submit")
def save_form_to_file(form_data: ContactForm):
    # Name of the file where we will store the data
    filename = "form_submissions.csv"
    
   
    file_exists = os.path.isfile(filename)
    
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(["Timestamp", "Name", "Email", "Phone", "Country", "Course"])
            
            # Write the actual form data as a new row
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([
                current_time,
                form_data.name,
                form_data.email,
                form_data.phone,
                form_data.country,
                form_data.course
            ])
            
        return {"success": True, "message": "Form submitted successfully"}
        
    except Exception as e:
        return {"success": False, "message": f"Failed to save data: {str(e)}"}