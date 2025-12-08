import streamlit as st
import google.generativeai as genai
import os

# 1. SETUP: Get the API Key safely
# We try to get it from Streamlit Secrets first
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🚨 API Key is missing! Please add it to Streamlit Secrets.")
    st.stop()

# 2. CONFIGURE AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. THE APP INTERFACE
st.set_page_config(page_title="Homework Hero", page_icon="🦸")

st.title("🦸 Homework Hero")
st.write("Turn boring homework into an epic adventure!")

# Input 1: The Homework Image
uploaded_file = st.file_uploader("📸 Upload a photo of the homework", type=["jpg", "png", "jpeg"])

# Input 2: The Theme
theme = st.text_input("🎭 Choose a theme (e.g., Ninjas, Frozen, Minecraft)", "Superheroes")

# Button to start the magic
if st.button("🚀 Start Adventure") and uploaded_file and theme:
    with st.spinner("Summoning the Storyteller..."):
        try:
            # Load the image
            from PIL import Image
            image = Image.open(uploaded_file)
            
            # The Prompt for Gemini
            prompt = f"""
            Role: You are an exciting storyteller for kids.
            Task: Look at this homework image. Create a short, funny story based on the theme '{theme}'.
            The hero of the story is the child.
            The hero faces a villain/obstacle that relates to the homework.
            To defeat the villain, the child must solve ONE question from the image.
            
            Output:
            1. The Story Scene (keep it exciting!).
            2. The Challenge (Ask the specific homework question).
            """
            
            # Get the response
            response = model.generate_content([prompt, image])
            
            # Show the result
            st.markdown("### 📜 Your Adventure Begins...")
            st.write(response.text)
            
            st.success("Now, answer the question above to defeat the villain!")
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")
