import os
from yt_dlp import YoutubeDL
from utils.yt_utils import validate_youtube_url
import imageio_ffmpeg as ffmpeg  # automatically provides ffmpeg executable path

# Folder to save downloads
DOWNLOADS = "downloads"
os.makedirs(DOWNLOADS, exist_ok=True)

# Get FFmpeg executable path dynamically (works on local & cloud)
FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()

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
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ratelimit": None,
        "format_sort": ["res:1080", "res:720", "res:480", "res:360", "res:240"],
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    if is_audio:
        # Extract numeric bitrate safely
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

    # Perform download
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)

        # Normalize extension for audio/video
        if is_audio:
            filepath = os.path.splitext(filepath)[0] + ".mp3"
        else:
            filepath = os.path.splitext(filepath)[0] + ".mp4"

        return filepath
