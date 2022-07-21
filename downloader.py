import ffmpeg    #to merge audio/video streaams
import pytube    #to download video from YouTube
import time      #to measure download time


output_folder = ''   # Change output for Windows system to this format: C:\Users\Admin\Downloads\

def clean_filename(name):
        """Ensures each file name does not contain forbidden characters and is within the character limit"""
        forbidden_chars = '"*\\/\'.|?:<>'
        filename = (''.join([char if char not in forbidden_chars else '' for char in name])).replace('  ', ' ').strip()
        if len(filename) >= 176:
            filename = filename[:170] + '...'
        return filename 


def get_video_info(yt):
    print('Title:', yt.title)
    print('Author:', yt.author)
    print('Published date:', yt.publish_date.strftime("%Y-%m-%d"))
    print('Number of views:', yt.views)
    print('Length of video:', yt.length, 'sec')


def download_streams(yt):
    """
    Downloads Video and Audio Streams
    """
    try:
        yt.streams.filter(res='1080p', progressive=False).first().download(filename='video.mp4')
        yt.streams.filter(abr='160kbps', progressive=False).first().download(filename='audio.mp3')
        res = '1080p'
        

    except:
        
        try:
            yt.streams.filter(res='720p', progressive=False).first().download(filename='video.mp4')
            yt.streams.filter(abr='128kbps', progressive=False).first().download(filename='audio.mp3')
            res = '720p'
        
        except:
            yt.streams.filter(res='480p', progressive=False).first().download(filename='video.mp4')
            yt.streams.filter(abr='128kbps', progressive=False).first().download(filename='audio.mp3')
            res = '480p'
        
    return res
        

def combine_streams(yt):
    """Combines audio and video stream into new video"""
    audio = ffmpeg.input('audio.mp3')
    video = ffmpeg.input('video.mp4')
    filename = output_folder + clean_filename(yt.title) + '.mp4'    
    ffmpeg.output(audio, video, filename).run(overwrite_output=True)

def run_downloader(link):
    """
    Abstracts the above utility functions into a simple one liner
    """
    ti = time.time()
    yt = pytube.YouTube(link, use_oauth=True, allow_oauth_cache=True)

    get_video_info(yt)
    res = download_streams(yt)    # returns the resolution value of our stream
    combine_streams(yt)


    print(res, 'video successfully downloaded from', link)
    print('Time taken: {:.0f} sec'.format(time.time() - ti))


def download_video(link):
    run_downloader(link)

def download_playlist(playlist_link):
    """
    Downloads an entire playlist

    Param:
        link (str): The link to a youtube playlist or video contained within one. 
    """
    _playlist = pytube.Playlist(playlist_link)

    print(f'Downloading playlist: {_playlist.title}')

    for video in _playlist.video_urls:
        run_downloader(video)

def download_channel(channel_link):

    _channel = pytube.Channel(link)

    print(f'Downloading Channel: {_channel.channel_name}')

    for video in _channel.video_urls:
        run_downloader(video)
        print(video)


def input_check(user_input):
    try:
        return int(user_input)
    except:
        main_prompt = input('Input: ')
        return input_check(main_prompt)

if __name__ == '__main__':
    
    main_prompt = input(
        """
        YOUTUBE DOWNLOADER

        0: Video     1: Playlist     2: Channel
        """
    )

    main_prompt = input_check(main_prompt)
    link = input('Youtube Link: ')
    
    if main_prompt == 0:
        download_video(link)
        # print('download video')
    elif main_prompt == 1:
        download_playlist(link)
        # print('download playlist')
    elif main_prompt == 2:
        download_channel(link)
        # print('download channel')
    else:
        print('Error: Option Not Available')
