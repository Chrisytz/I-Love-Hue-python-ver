import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import pafy
import vlc

url = "https://youtu.be/wTowEKjDGkU"
video = pafy.new(url)
best = video.getbest()
playurl = best.url

Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new(playurl)
Media.get_mrl()
player.set_media(Media)
player.play()
while True:
    pass