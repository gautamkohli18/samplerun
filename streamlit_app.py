import os
import logging
import random
import itertools
import streamlit as st

# Try importing google.generativeai and handle missing package
try:
    import google.generativeai as genai
except ModuleNotFoundError:
    st.error("Missing required package: google-generativeai. Install it using 'pip install google-generativeai'.")
    raise

# Initialize Gemini API
api_key = os.getenv("GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    },
)

# Setup logging
logging.basicConfig(filename="script_generation.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Define domains and roles
domains = {
    "BFSI": ["Bank Representative", "Customer"],
    "E-commerce": ["Customer Support", "Buyer"],
    "Health-tech": ["Doctor", "Patient"],
    "Food-tech": ["Delivery Executive", "Customer"],
    "Ed-tech": ["Teacher", "Student"],
}

companies = {
    "BFSI": ["HDFC Bank", "ICICI Bank"],
    "E-commerce": ["Amazon", "Flipkart"],
    "Health-tech": ["Practo", "PharmEasy"],
    "Food-tech": ["Swiggy", "Zomato"],
    "Ed-tech": ["BYJU'S", "Unacademy"],
}

def generate_script(language, domain, company, role1, role2, emotion1, emotion2, gender, script_number):
    prompt = f"""
    Create a realistic call centre conversation script for a TTS dataset. The script should last at least 10 minutes.
   
    Language: {language}
    Domain: {domain}
    Company: {company}
    Roles: {role1} and {role2}
    Emotions: {role1} - {emotion1}, {role2} - {emotion2}
    Gender: {gender}
   
    The conversation should be natural, structured, and contain varied sentence patterns.
    """

    try:
        response = model.generate_content(prompt)
        script = response.text
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        st.error("Error communicating with Gemini API. Check logs for details.")
        return None
   
    filename = f"scripts/script_{language}_{domain}_{company}_{script_number}.txt"
    os.makedirs("scripts", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(script)
   
    logging.info(f"Saved: {filename}")
    return filename

# Function to generate multiple scripts
def generate_all_scripts(language="English"):
    script_number = 1
    for domain, roles in domains.items():
        for company in companies[domain]:
            role1, role2 = roles
            emotion1, emotion2 = random.choice([("Polite", "Frustrated"), ("Happy", "Neutral"), ("Serious", "Concerned")])
            gender = random.choice(["Male", "Female"])
            generate_script(language, domain, company, role1, role2, emotion1, emotion2, gender, script_number)
            script_number += 1

def main():
    st.title("Script Generator")
    if st.button("Generate Scripts"):
        generate_all_scripts()
        st.success("Scripts generated successfully!")

if __name__ == "__main__":
    main()
