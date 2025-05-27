import streamlit as st
from PIL import Image

def show_about_me():
    #st.subheader("👋 About Me")

    col1, col2 = st.columns([1, 2])

    with col1:
        image = Image.open("me.jpg")
        st.image(image, width=250, use_container_width =False)

    with col2:
        st.markdown("""
        ### Hi, I'm Diya!

        I'm a passionate foodie and an explorer at heart, always on the lookout for authentic flavors and cultural experiences from around the world. My culinary journey started with travels across **20+ Indian states**, where I fell in love with the diversity of local cuisines—each with its own story and soul.

        Beyond India, my adventures have taken me to **Dubai**, where the fusion of Middle Eastern spices fascinated me, and most recently to **Japan**, a dream come true. From sampling street-side yakitori in Tokyo to enjoying peaceful bowls of ramen in Kyoto, Japan deeply influenced my appreciation for balance, freshness, and presentation in food.

        🍲 Whether it’s savoring home-cooked meals in remote villages or uncovering hidden food gems in bustling cities, **food and culture fuel my creativity**.

        > **Cook it Like There!** was born from my desire to help others recreate these incredible experiences in their own kitchens—no matter where they are.

        Let’s cook, explore, and celebrate real flavors together!
        """)
