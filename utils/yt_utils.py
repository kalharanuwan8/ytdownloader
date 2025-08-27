import re

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
