document.addEventListener("DOMContentLoaded", function() {
    
 
    const accordionItems = document.querySelectorAll(".accordion-item");

    accordionItems.forEach(item => {
        const header = item.querySelector(".accordion-header");
        
        header.addEventListener("click", () => {
            // Check if currently active
            const isActive = item.classList.contains("active");

            // Close all items
            accordionItems.forEach(el => {
                el.classList.remove("active");
                const icon = el.querySelector(".fa-chevron-up");
                if (icon) {
                    icon.classList.remove("fa-chevron-up");
                    icon.classList.add("fa-chevron-down");
                }
            });

            // If it wasn't active, open it
            if (!isActive) {
                item.classList.add("active");
                const icon = item.querySelector(".fa-chevron-down");
                if (icon) {
                    icon.classList.remove("fa-chevron-down");
                    icon.classList.add("fa-chevron-up");
                }
            }
        });
    });

    //  Form Submission Logic 
    const form = document.querySelector(".lead-form-card form");
    
    if (form) {
        form.addEventListener("submit", async function(event) {
            // Prevent the page from reloading
            event.preventDefault();

            const submitBtn = form.querySelector("button[type='submit']");
            
            // SECURITY CHECK: Prevent double-clicking
            if (submitBtn.disabled) return; 

            // Get the values from the input fields
            const inputs = form.querySelectorAll("input, select");
            
            const formData = {
                name: inputs[0].value,
                email: inputs[1].value,
                phone: inputs[2].value,
                country: inputs[3].value,
                course: inputs[4].value
            };

            try {
                // Change the button text and DISABLE it so the user can't click twice
                const originalBtnText = submitBtn.innerText;
                submitBtn.innerText = "Sending...";
                submitBtn.disabled = true;
                submitBtn.style.opacity = "0.7";
                submitBtn.style.cursor = "not-allowed";

                // Send the data to Python backend
                const response = await fetch("http://127.0.0.1:8000/api/contact-submit", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (result.success) {
                    alert("Thank you! Your form has been submitted and saved to the file.");
                    form.reset(); // Clear the form
                } else {
                    alert("Error saving form: " + result.message);
                }

                // Reset button text
                submitBtn.innerText = originalBtnText;

            } catch (error) {
                console.error("Error:", error);
                alert("Could not connect to the server. Is your Python backend running?");
            } finally {
                // ALWAYS re-enable the button when finished, even if there was an error
                submitBtn.disabled = false;
                submitBtn.style.opacity = "1";
                submitBtn.style.cursor = "pointer";
            }
        });
    }
});