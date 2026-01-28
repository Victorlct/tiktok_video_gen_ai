from pytube import YouTube
import os

class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.video = YouTube(url)

    def download_video(self, output_dir=None):
        try:
            if output_dir:
                output_path = os.path.join(output_dir, self.video.title + ".mp4")
                self.video.streams.get_highest_resolution().download(output_path=output_path)
            else:
                self.video.streams.get_highest_resolution().download()
            print("Download concluído!")
        except Exception as e:
            print("Ocorreu um erro durante o download:", str(e))

# Exemplo de uso:
url = "https://www.youtube.com/watch?v=VS3D8bgYhf4&ab_channel=DopeGameplays"  # URL do vídeo do YouTube
output_directory = "YoutubeVideos"  # Diretório de saída personalizado
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

downloader = YouTubeDownloader(url)
downloader.download_video(output_dir=output_directory)
