import re
import os
from yt_dlp import YoutubeDL

# Folder to save downloads
DOWNLOADS = "downloads"
os.makedirs(DOWNLOADS, exist_ok=True)  # Ensure folder exists

# Path to your FFmpeg executable
FFMPEG_PATH = r"C:\Users\Kalhara\Downloads\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\bin\ffmpeg.exe"


def validate_youtube_url(url):
    """
    Validate if the provided URL is a proper YouTube link.
    Returns True if valid, False otherwise.
    """
    youtube_regex = (
        r'^(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/.+$'
    )
    return re.match(youtube_regex, url) is not None

def download_video(url, is_audio=True):
    """
    Download video/audio from YouTube using yt-dlp.
    is_audio=True -> MP3
    is_audio=False -> MP4
    Returns the saved filename.
    """
    filename_template = os.path.join(DOWNLOADS, "%(title)s.%(ext)s")

    if is_audio:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filename_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': r"C:\Users\Kalhara\Downloads\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\bin\ffmpeg.exe",
        }
    else:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': filename_template,
            'merge_output_format': 'mp4',
            'ffmpeg_location': r"C:\Users\Kalhara\Downloads\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\bin\ffmpeg.exe",
        }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
