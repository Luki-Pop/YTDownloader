import yt_dlp

QUALITY_MAP = {
    "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "audio": "bestaudio"
}

def download_video(link: str, quality: str):
    """
    Pobiera film z YouTube przy użyciu yt-dlp.
    Zwraca: (success: bool, message: str)
    """

    try:
        ydl_opts = {
            "format": QUALITY_MAP[quality],
            "outtmpl": "%(title)s.%(ext)s",
            "merge_output_format": "mp4"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        return True, "Download complete"

    except Exception as e:
        return False, str(e)
