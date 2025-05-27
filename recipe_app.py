import streamlit as st
import requests
import os
import json
import time

# Set page config as the first Streamlit command
st.set_page_config(page_title="Cook it Like There!", layout="centered")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
UNSPLASH_ACCESS_KEY = st.secrets["UNSPLASH_ACCESS_KEY"]

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GROQ_API_KEY}"
}

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def query_groq(prompt):
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a professional chef who gives authentic regional recipes, adapts ingredients based on user location, and provides cultural facts and images."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(GROQ_URL, headers=HEADERS, data=json.dumps(data))
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def fetch_unsplash_images(query):
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "client_id": UNSPLASH_ACCESS_KEY,
        "per_page": 5
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()["results"]
        return [img["urls"]["regular"] for img in results]
    else:
        return []

def run_recipe_app():
    st.markdown("""
    <div style='text-align: center;'>
        <p style='font-size: 1.1em; font-style: italic; margin-bottom: 1em;'>
        I know you crave those unforgettable flavors from around the world — what if you could recreate them right from where you are? 🌍<br>
        Let’s bring authentic tastes to your kitchen using what’s locally available — and have some fun learning about the dish too!
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center;'>🍲 Cook it Like There!</h2>", unsafe_allow_html=True)

    dish_name = st.text_input("Enter a dish name:")
    user_location = st.text_input("Where are you located? (Country or City)")

    if st.button("Get Regional Recipe") and dish_name and user_location:
        with st.spinner("Cooking up the recipe..."):
            prompt = f"""
            I want a recipe for {dish_name}. I live in {user_location}, so please use ingredient substitutes that are locally available. 
            Also include 2-3 fun facts about this dish.
            """
            try:
                result = query_groq(prompt)
                st.markdown(result)

                images = fetch_unsplash_images(dish_name)
                if images:
                    st.markdown("### 🍽️ Dish Images")
                    if 'img_index' not in st.session_state:
                        st.session_state.img_index = 0
                    if 'last_update_time' not in st.session_state:
                        st.session_state.last_update_time = time.time()

                    if time.time() - st.session_state.last_update_time > 5:
                        st.session_state.img_index = (st.session_state.img_index + 1) % len(images)
                        st.session_state.last_update_time = time.time()

                    st.image(images[st.session_state.img_index], use_container_width=False, width=400)

                    dots = ["●" if i == st.session_state.img_index else "○" for i in range(len(images))]
                    st.markdown("<div style='text-align: center;'>" + " ".join(dots) + "</div>", unsafe_allow_html=True)
                else:
                    st.info("No images found for this dish on Unsplash.")

            except Exception as e:
                st.error("Something went wrong while fetching the recipe. Please try again.")
                st.exception(e)

    st.markdown("""
    <hr style='margin-top: 2em;'>
    <p style='font-size: 0.9em; text-align: center;'>✨ Recipes powered by LLaMA through Groq API. Images via Unsplash.</p>
    """, unsafe_allow_html=True)

# Tabs layout
about_tab, app_tab = st.tabs(["About Me", "Cook it Like There!"])

with about_tab:
    st.markdown("## About Me")
    st.markdown("Hi! I'm the creator of 'Cook it Like There!'. This app helps you recreate authentic regional recipes with local ingredients and shares fun cultural tidbits too!")

with app_tab:
    run_recipe_app()

# Optional styling
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #e6ccff;
        color: black;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)
