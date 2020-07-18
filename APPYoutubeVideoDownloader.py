import pytube
import os
from bs4 import BeautifulSoup
import requests
cwd = os.getcwd()
def remove_signs(string):  # this removes signs that doesnt work with file names and spaces to make it work always
    newstring = ''
    for char in string:
        if char in '\/<>*:?"|':
            char=' '
        newstring = newstring + char
    return newstring
class YoutubeVideoDownloader:
    try:
        with open(os.path.expanduser('~') + '\Documents\YoutubeVideoDownloader\output_path.txt', 'r') as f:
            path = f.read().strip()
            default_output_path = path
    except:
        pass

    def __init__(self,YtbUrl,downloadProgress,downloadComplete,downloadProgress2,downloadComplete2):
        self.video = pytube.YouTube(YtbUrl, on_progress_callback=downloadProgress,
                                    on_complete_callback=downloadComplete)
        self.audio = pytube.YouTube(YtbUrl, on_progress_callback=downloadProgress2,
                                    on_complete_callback=downloadComplete2)
        self.n = 0
        self.time1 = None
        self.time2 = None
        self.old_remaining = 0
        self.output_path= self.default_output_path
        self.downloaded_path=''
        self.video_streams_dict=dict()
        self.audio_streams_dict=dict()
        self.download_speed = 0
        self.download_percent = 0
        self.filesize = 1
        self.video_title = ''
        self.video_streams_all = None
        self.desired_stream = None
        self.audio_stream = self.audio.streams.get_audio_only()
        self.videoTitleFinder(YtbUrl)
        self.video_labels_list = []
        self.audio_buttons_list = []
        self.video_buttons_list = []
        self.audio_labels_list = []






    def download(self,stream):
        filename = 'video'
        self.downloaded_path=stream.download(output_path=self.output_path, filename=filename)

    def resetVideoStreamsDict(self):
        self.video_streams_dict = dict()
    def resetAudioStreamsDict(self):
        self.audio_streams_dict = dict()

    def resetVideoLists(self):
        self.video_labels_list = []
        self.video_buttons_list = []
    def resetAudioLists(self):
        self.audio_labels_list = []
        self.audio_buttons_list = []

    def getVideoStreams(self):
        self.video_streams_all = self.video.streams.filter(type='video')
    def applyFilterVideo(self,file_extension:str):

        video_streams = self.video_streams_all.filter(file_extension=file_extension).order_by(
            'resolution').desc()
        video_streams_both = video_streams.filter(progressive=True)
        video_only_streams = video_streams.filter(adaptive=True)

        if video_only_streams != None:
            for stream in video_only_streams:
                stream_str = stream.__str__()
                stream_label = stream_str.split(' ')[3].split('\"')[1]
                if stream_str.split(' ')[4].split('\"')[1] == '60fps':
                    stream_label += '60fps'
                self.video_streams_dict[stream_label] = stream


        if video_streams_both != None:

            for stream in video_streams_both:
                stream_str = stream.__str__()
                stream_label = stream_str.split(' ')[3].split('\"')[1]
                if stream_str.split(' ')[4].split('\"')[1] == '60fps':
                    stream_label += '60fps'
                self.video_streams_dict[stream_label] = stream



    def getAudioOnlyStreams(self):
        self.audio_streams = self.video.streams.filter(only_audio=True)

    def applyFilterAudio(self,file_extension:str):
        audio_streams = self.audio_streams.filter(file_extension=file_extension).order_by('abr').desc()
        if audio_streams != None:
            for stream in audio_streams:
                stream_str = stream.__str__()
                stream_label = stream_str.split(' ')[3].split('\"')[1]
                self.audio_streams_dict[stream_label] = stream


    def downloadAudioDirectly(self):
        filename = 'audio'
        self.filesize = self.audio_stream.filesize
        self.audio_stream.download(output_path=self.output_path , filename=filename)





    def mergeVideoAudio(self,video_without_audio:str,audio:str):   #the absolute path for the video without audio and the audio
        self.merge_output = self.output_path + '\output.mp4'

        try:
            os.system(f'ffmpeg -i {video_without_audio} -i {audio} -codec copy {self.merge_output}')
            print('1st')
        except Exception as e:
            print(e)
            print('2nd')
            os.system(f'ffmpeg-folder\\bin\\ffmpeg -i {video_without_audio} -i {audio} -codec copy {self.merge_output}')
        os.remove(video_without_audio)
        os.remove(audio)

    def videoTitleFinder(self,url):
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        name = soup.find('meta', itemprop="name").__str__()[15:-19]
        self.video_title = name


class PlaylistDownloader():
    def __init__(self,PlaylistUrl,downloadProgress3,downloadComplete3):
        self.playlist = pytube.Playlist(PlaylistUrl)
        self.video_streams=None
        self.urls = self.playlist.video_urls
        self.video = None
        self.resolutions=['720p','360p']
        self.downloadProgress3 = downloadProgress3
        self.downloadComplete3 = downloadComplete3
        self.k = 0
        self.video_count = len(self.urls)
        self.digits = len(str(len(self.urls)))
        self.playlist_title = self.playlist.title()

        try:
            with open(os.path.expanduser('~') + '\Documents\YoutubeVideoDownloader\output_path.txt', 'r') as f:
                path = f.read().strip()
                self.output_path = path
        except:
            pass
        self.n = 0
        self.time1 = None
        self.time2 = None
        self.old_remaining = 0
        self.download_speed = 0
        self.download_percent = 0
        self.filesize = 1
        self.video_titles = (self.videoTitleFinder(link) for link in self.urls)

    def downloadPlaylist(self,i):
        for link in self.urls:

            self.video = pytube.YouTube(link,on_progress_callback=self.downloadProgress3,on_complete_callback=self.downloadComplete3)
            video_streams_all = self.video.streams.filter(type='video')
            self.video_streams = video_streams_all.filter(file_extension='mp4',progressive=True).order_by('resolution').desc()
            try:
                i = int(i)
                stream=self.video_streams.get_by_resolution(self.resolutions[i])
                if stream==None:
                    if i ==0:
                        stream = self.video_streams.get_highest_resolution()
                    if i == 1:
                        stream = self.video_streams.get_by_resolution(self.resolutions[0])
                    if stream==None:
                        stream = self.video_streams.get_highest_resolution()
                        if stream == None:
                            stream = self.video.streams.get_lowest_resolution()
                            if stream == None:
                                continue
            except:

                stream = self.video.streams.get_audio_only()
                if stream ==None:
                    continue

            self.filesize = stream.filesize
            prefix = str(self.k+1).zfill(self.digits)+'-'
            if not os.path.exists(self.output_path+'\\'+remove_signs(self.playlist_title)+'/'):
                os.mkdir(self.output_path+'\\'+remove_signs(self.playlist_title))
            output_path = self.output_path+'\\'+remove_signs(self.playlist_title)
            stream.download(output_path=output_path,filename_prefix=prefix,skip_existing=True)


    @staticmethod
    def videoTitleFinder(url):
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        name = soup.find('meta', itemprop="name").__str__()[15:-19]
        return name