import yt_dlp
import os
import imageio_ffmpeg

QUALITY_MAP = {
    "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "audio": "bestaudio"
}

FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()


def download_video(link: str, quality: str, save_path: str, progress_callback=None):
    """
    Pobiera film z YouTube przy użyciu yt-dlp.
    save_path — folder zapisu
    progress_callback(percent) — callback postępu
    """

    def hook(d):
        if d["status"] == "downloading":
            if progress_callback:
                try:
                    percent = d.get("_percent_str", "0%").replace("%", "").strip()
                    progress_callback(float(percent))
                except:
                    pass

    try:
        os.makedirs(save_path, exist_ok=True)

        ydl_opts = {
            "format": QUALITY_MAP[quality],
            "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
            "progress_hooks": [hook],
            "ffmpeg_location": FFMPEG_PATH,   # <-- KLUCZOWE!
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        return True, "Download complete"

    except Exception as e:
        return False, str(e)
