from pytube import YouTube

def Download(link):
    youtubObject = YouTube(link)
    youtubObject = youtubObject.streams.get_highest_resolution()
    try:
        youtubObject.download()
    except:
        print('ERROR,ERROR,ERROR')
    print('SUCCESS, YOU PLUNDER THE YOUTUBE')



link = input("LINK GOES HIRE: ")

Download(link)