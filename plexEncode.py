from os import path, makedirs, getenv, walk
from subprocess import call
import shutil

class Encoder:

    def __init__(self):

        self.FFMPEG_PATH = self.find_ffmpeg('ffmpeg.exe')
        self.OVERWRITE = '-y'
        self.VSYNC = '0'
        self.HWACCEL = 'cuda'
        self.METADATA_STRIP_TITLE = 'title='
        self.METADATA_STRIP_COMMENT = 'comment='
        self.VIDEO_NVIDIA_ENCODE = 'h264_nvenc'
        self.PIXFMT = 'yuv420p'
        self.AUDIO_ENCODE = 'aac'
        self.CHANNEL = '2'
        self.OUTPUT_FILE_EXTENSION = 'mp4'
        self.OUTPUT_DIRECTORY = 'encoded'

    def find_ffmpeg(self, filename):
        result = str
        pathVar = getenv('Path').split(";")
        
        for loc in pathVar:
            for root, folder, files in walk(loc):
                if filename in files:
                    # directory format for Windows
                    result = path.join(root + "\\" + filename)                
                else:
                    continue
                break
            else:
                continue
            break
        return result
        
    def plex_encoder(self, input_file_path, output_directory):

        output_file_path = output_directory + self.compile_output_file_name(input_file_path)
        call([
            self.FFMPEG_PATH,
            self.OVERWRITE,
            '-vsync', self.VSYNC,
            '-hwaccel', self.HWACCEL,
            '-hwaccel_output_format', self.HWACCEL,
            '-i', input_file_path,
            '-f', self.OUTPUT_FILE_EXTENSION,            
            '-c:a', self.AUDIO_ENCODE,
            '-ac', self.CHANNEL,
            '-c:v', self.VIDEO_NVIDIA_ENCODE,
            '-metadata', self.METADATA_STRIP_TITLE,
            '-metadata', self.METADATA_STRIP_COMMENT,
            output_file_path
        ])

    def compile_output_file_name(self, input_file_path):

        input_file_name = path.basename(input_file_path)
        input_file_name_without_extension = path.splitext(input_file_name)[0]
        return input_file_name_without_extension + '.' + self.OUTPUT_FILE_EXTENSION

    def clean_directory(self, dir_path):

        shutil.rmtree(dir_path, ignore_errors=True)
        makedirs(dir_path)
