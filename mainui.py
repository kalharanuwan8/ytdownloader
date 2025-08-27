import streamlit as st
from downloader import download_youtube
from utils.yt_utils import validate_youtube_url
import os

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="YouTube Downloader", page_icon="🎵", layout="centered")
st.title("🎵 YouTube Downloader")
st.markdown("Download YouTube videos or audio directly from your browser!")

# Input
url = st.text_input("YouTube URL:")
format_choice = st.radio("Select format:", ("MP3", "MP4"))

quality = st.selectbox(
    "Select Quality:",
    ["192 kbps", "256 kbps", "320 kbps"] if format_choice == "MP3" else ["Best", "1080p", "720p", "480p", "360p"]
)

status_text = st.empty()
progress_bar = st.progress(0)

# Streamlit-safe progress hook
def progress_hook(d):
    if d.get("status") == "downloading":
        downloaded = d.get("downloaded_bytes", 0)
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
        progress = int(downloaded / total * 100)
        progress_bar.progress(progress)
        status_text.info(f"⬇ Downloading... {progress}%")
    elif d.get("status") == "finished":
        progress_bar.progress(100)
        status_text.success("✅ Download finished, processing file...")

# Download button
if st.button("⬇ Start Download"):
    if not url:
        st.error("⚠ Please enter a YouTube URL")
    elif not validate_youtube_url(url):
        st.error("❌ Invalid YouTube URL")
    else:
        # Show alert that it's queued
        st.info("📌 Added to download queue... Please wait!")

        try:
            filename = download_youtube(
                url, 
                is_audio=(format_choice == "MP3"), 
                quality=quality, 
                progress_hook=progress_hook
            )
            if filename and os.path.exists(filename):
                status_text.success(f"✅ Download complete: {os.path.basename(filename)}")
                with open(filename, "rb") as f:
                    st.download_button(
                        label="📥 Download File",
                        data=f,
                        file_name=os.path.basename(filename),
                        mime="application/octet-stream"
                    )
            else:
                st.error("❌ File not found after download. Something went wrong.")
        except Exception as e:
            st.error(f"❌ Download failed: {e}")
