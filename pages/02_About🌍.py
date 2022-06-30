import streamlit as st
from PIL import Image
import webbrowser

st.set_page_config(
    page_title = "About",
    page_icon = "🏎",
    layout = "wide",
    initial_sidebar_state = "auto",
)
hide_footer = """
            <style>
            footer {visibility:hidden;}
            </style>
            """
st.markdown(hide_footer, unsafe_allow_html = True)
st.snow()
st.header("About This Project")
st.markdown(f"""
    <b>Hi there I am the creater of this app. </b><br>
    This is a data visualization app that present used car data in U.S. with features like: compare statistical data of used car in different states, viewing data in differnt interactive maps, scatter plots, and pie chars. There are more than 365k valid data in the dataset I used for this webapp. The data is from used car listing on {'<a href="craigslist.org">craigslist.org</a>'}<br><br>
    At June 7th 2022, I had a random idea to visualize a lot of used car listing in USA. I thought it would be really cool. So I decided to make it come true.
    I had put a lot of time into it to make is as good as possible and I am proud of it. If you have any suggestion plese do not hazetate to contact me by {'<a href="mailto:13520759678@163.com">email</a>'}.
""", unsafe_allow_html = True)
audio_file = open('piano.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes)
st.markdown(f"""
    Music by {'<a href="/users/zakharvalaha-22836301/?tab=audio&amp;utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=audio&amp;utm_content=9784">ZakharValaha</a>'} from {'<a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=9784">Pixabay</a>'}
    """, unsafe_allow_html = True)