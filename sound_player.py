import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import pafy
import vlc

def play_music1():
    url = "https://youtu.be/St-H0-xc-sc?list=LL"
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url

    Instance = vlc.Instance("--vout=dummy")
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.audio_set_volume(50)
    player.play()
    while True:
        pass