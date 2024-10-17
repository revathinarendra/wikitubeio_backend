import pytube
import subprocess
import os

def download_youtube_audio(url, output_path='audio'):
    """
    Download the YouTube video as audio.
    """
    youtube = pytube.YouTube(url)
    video_stream = youtube.streams.filter(only_audio=True).first()
    audio_file = video_stream.download(output_path=output_path)
    return audio_file

def convert_to_mp3(input_file, output_file):
    """
    Convert the audio file to mp3 using ffmpeg.
    """
    command = ['ffmpeg', '-i', input_file, output_file]
    subprocess.run(command)
    return output_file

def cleanup_files(*file_paths):
    """
    Delete the temporary files after upload.
    """
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
