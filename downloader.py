import os
from yt_dlp import YoutubeDL
from utils.yt_utils import validate_youtube_url

# FFmpeg path
FFMPEG_PATH = r"C:\Users\Kalhara\Downloads\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\bin\ffmpeg.exe"

# Folder to save downloads
DOWNLOADS = "downloads"
os.makedirs(DOWNLOADS, exist_ok=True)

def download_youtube(url, is_audio=True, quality="Best", progress_hook=None):
    """
    Download YouTube video/audio.
    is_audio=True -> MP3
    is_audio=False -> MP4
    quality: Audio "192 kbps", Video "1080p", "Best", etc.
    progress_hook: optional function for GUI progress
    """
    if not validate_youtube_url(url):
        print("Invalid YouTube URL!")
        return

    filename_template = os.path.join(DOWNLOADS, "%(title)s.%(ext)s")

    ydl_opts = {
        'outtmpl': filename_template,
        'ffmpeg_location': FFMPEG_PATH,
        'progress_hooks': [progress_hook] if progress_hook else []
    }

    if is_audio:
        bitrate = int(quality.split()[0])
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': str(bitrate),
            }],
        })
    else:
        if quality == "Best":
            video_format = "bestvideo+bestaudio/best"
        else:
            height = int(quality.replace("p",""))
            video_format = f"bestvideo[height<={height}]+bestaudio/best"
        ydl_opts.update({
            'format': video_format,
            'merge_output_format': 'mp4',
        })

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Download failed: {e}")
