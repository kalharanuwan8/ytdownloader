import os
from yt_dlp import YoutubeDL
from utils.yt_utils import validate_youtube_url

# Folder to save downloads
DOWNLOADS = "downloads"
os.makedirs(DOWNLOADS, exist_ok=True)

# Path to your FFmpeg bin folder (must contain ffmpeg.exe and ffprobe.exe)
FFMPEG_PATH = r"C:\Users\Kalhara\Downloads\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\bin"

def download_youtube(url, is_audio=True, quality="Best", progress_hook=None):
    """
    Download YouTube video/audio using yt-dlp.

    Parameters:
    - url: str, YouTube video URL
    - is_audio: bool, True for MP3, False for MP4
    - quality: str, e.g., "Best", "1080p", "192 kbps"
    - progress_hook: optional function for GUI progress updates

    Returns:
    - filepath of downloaded file
    """
    if not validate_youtube_url(url):
        raise ValueError("Invalid YouTube URL!")

    filename_template = os.path.join(DOWNLOADS, "%(title)s.%(ext)s")

    # Base yt-dlp options
    ydl_opts = {
        "outtmpl": filename_template,
        "ffmpeg_location": FFMPEG_PATH,
        "progress_hooks": [progress_hook] if progress_hook else [],
        "quiet": True,  # prevents messy console output
        "no_warnings": True,
    }

    if is_audio:
        # Extract audio bitrate safely
        try:
            bitrate = int("".join([c for c in quality if c.isdigit()]))
        except Exception:
            bitrate = 192  # default

        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": str(bitrate),
            }],
        })
    else:
        # Handle video quality safely
        if quality.lower() == "best":
            video_format = "bestvideo+bestaudio/best"
        else:
            try:
                height = int(quality.replace("p", "").strip())
                video_format = f"bestvideo[height<={height}]+bestaudio/best"
            except Exception:
                video_format = "bestvideo+bestaudio/best"

        ydl_opts.update({
            "format": video_format,
            "merge_output_format": "mp4",
        })

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)

        # If audio → replace .webm/.m4a with .mp3
        if is_audio:
            filepath = os.path.splitext(filepath)[0] + ".mp3"
        else:
            filepath = os.path.splitext(filepath)[0] + ".mp4"

        return filepath
