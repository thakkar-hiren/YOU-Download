from flask import Flask, render_template,request
from pytube import YouTube
import os

app = Flask(__name__)

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

@app.route("/", methods=['GET','POST'])
def you_download():
    if request.method == 'POST':
        video_link = request.form['video']
        videos = YouTube(video_link)
        video = videos.streams.get_highest_resolution()
        download_location = get_download_path()
        video.download(download_location)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

