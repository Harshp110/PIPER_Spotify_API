import streamlit as st
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="PIPER",
    layout="wide"
)

# ------------------ BACKGROUND CSS ------------------
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
    background-image: url("https://t3.ftcdn.net/jpg/05/50/05/52/360_F_550055239_zK6qJTCOfodrftSLJM7bjcoUnF6lIl6Y.jpg");
    background-size: cover;
}
[data-testid="stHeader"]{
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# -------- FORCE TEXT VISIBILITY --------
st.markdown("""
<style>
h1, h2, h3, h4, h5, h6, p, span, div, a {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SPOTIFY CONFIG ------------------
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"
REDIRECT_URI = "https://piperspotifyapi-pl7d2mwxy9va4vud6qkfzz.streamlit.app/"

SCOPE = [
    "user-read-email",
    "playlist-read-collaborative"
]

# --------- SECRETS (DO NOT HARD CODE) ----------
SPOTIFY_CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]


# ------------------ FUNCTIONS ------------------
def login():
    spotify = OAuth2Session(
        CLIENT_ID,
        scope=SCOPE,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = spotify.authorization_url(AUTH_URL)
    st.markdown(f"### 👉 [Login with Spotify]({auth_url})")

def callback():
    code = st.text_input("Paste the **code** from the callback URL")
    if st.button("Submit") and code:
        response = requests.post(
            TOKEN_URL,
            auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
        )
        data = response.json()
        if "access_token" in data:
            st.session_state.access_token = data["access_token"]
            st.success("Login successful!")
        else:
            st.error("Failed to authenticate.")

def get_user():
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}"
    }
    r = requests.get(API_BASE_URL + "me", headers=headers)
    user = r.json()
    st.success(f"Logged in as **{user['display_name']}**")

# ------------------ UI ------------------
st.title("Welcome to the **PIPER App** 🎧")

st.write(
    "Send your Spotify email if you need API allowlist access."
)
st.write("📧 Contact: **harshpandav110@gmail.com**")

st.markdown("---")

if "access_token" not in st.session_state:
    login()
    callback()
else:
    get_user()

st.markdown("---")
st.markdown("Built with ❤️ by **Harsh S. Pandav**")
