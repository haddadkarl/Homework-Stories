import os
from flask import Flask, render_template, request
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

# SETUP API KEY
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    story = ""
    challenge = ""

    if request.method == "POST":
        theme = request.form.get("theme")
        uploaded_file = request.files.get("file")

        if uploaded_file and theme and api_key:
            try:
                img = Image.open(uploaded_file)
                model = genai.GenerativeModel('gemini-1.5-flash')

                prompt = f"""
                Role: Narrator for a kid's adventure. Theme: {theme}.
                Task: Analyze image. Write a short Scene 1 where the hero faces a villain related to the homework.
                End with a specific question from the homework image that the user must solve to continue.
                Format: 
                STORY: [The story text]
                CHALLENGE: [The math/homework question]
                """

                response = model.generate_content([prompt, img])
                text = response.text

                # Simple parsing (assuming Gemini follows format)
                if "CHALLENGE:" in text:
                    parts = text.split("CHALLENGE:")
                    story = parts[0].replace("STORY:", "").strip()
                    challenge = parts[1].strip()
                else:
                    story = text

            except Exception as e:
                story = f"Error: {e}"

    return render_template("index.html", story=story, challenge=challenge)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
