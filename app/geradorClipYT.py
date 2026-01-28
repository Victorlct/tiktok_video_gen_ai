import moviepy.editor as mp
import os
import random

class VideoClipper:
    def __init__(self, video_source_folder):
        self.video_source_folder = video_source_folder

    def get_random_video_path(self):
        videos = [f for f in os.listdir(self.video_source_folder) if f.endswith('.mp4')]
        if videos:
            video_filename = random.choice(videos)
            return os.path.join(self.video_source_folder, video_filename)
        else:
            raise FileNotFoundError("Nenhum arquivo de vídeo .mp4 encontrado no diretório fornecido.")

    def clip_video(self, duration, output_path):
        try:
            # Obter um vídeo aleatório do diretório
            video_source_path = self.get_random_video_path()

            # Carrega o vídeo
            video_clip = mp.VideoFileClip(video_source_path)

            # Determina a duração máxima do corte
            max_duration = video_clip.duration - duration

            # Escolhe um ponto de início aleatório dentro do intervalo permitido
            start_time = random.uniform(0, max_duration)

            # Corta o vídeo a partir do ponto de início aleatório
            clip = video_clip.subclip(start_time, start_time + duration)

            # Remove o áudio
            clip = clip.without_audio()

            # Define o caminho de saída para o clipe
            output_path = output_path + "_bottom.mp4"

            # Salva o clipe
            clip.write_videofile(output_path, codec="libx264")

            print("Clipe criado com sucesso!")
        except Exception as e:
            print("Ocorreu um erro ao criar o clipe:", str(e))

# Exemplo de uso:
# video_source_folder = "YoutubeVideos"  # Caminho da pasta de vídeos
# output_folder = "HistoriaFilosofia"  # Nome do tema para o diretório de saída
# output_filename = "HistoriaFilosofia_clipped.mp4"  # Nome do arquivo final
# duration_seconds = 75  # Duração desejada do clipe em segundos

# clipper = VideoClipper(video_source_folder)
# clipper.clip_video(duration_seconds, output_folder, output_filename)
