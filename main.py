import yt_dlp

def Download(link, quality="best"):
    ydl_opts = {
        "format": quality,
        "outtmpl": "%(title)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


link = input("LINK: ")
Download(link)
