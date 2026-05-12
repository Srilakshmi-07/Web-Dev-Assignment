from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import csv
import os
from datetime import datetime

# Initialize the FastAPI app
app = FastAPI()

# Allow the frontend (HTML) to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (good for local testing)
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

# Define the API Endpoint
@app.post("/api/contact-submit")
def save_form_to_file(form_data: ContactForm):
    # Name of the file where we will store the data
    filename = "form_submissions.csv"
    
    # Check if the file already exists so we know if we need to write headers
    file_exists = os.path.isfile(filename)
    
    try:
        # Open the file in "append" mode ('a') so it adds to the bottom
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # If the file is brand new, write the column headers first
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