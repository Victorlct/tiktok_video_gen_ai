from moviepy.editor import VideoFileClip, clips_array

class VideoJoiner:
    def __init__(self, video1_path, video2_path):
        self.video1 = VideoFileClip(video1_path)
        self.video2 = VideoFileClip(video2_path)

    def join_videos(self, output_path):
        # Redimensionar os vídeos para 1080x960 (metade da altura)
        self.video1 = self.video1.resize(height=960)
        self.video2 = self.video2.resize(height=960)

        # Juntar os vídeos verticalmente
        final_clip = clips_array([[self.video1], [self.video2]])

        # Salvar o vídeo final
        final_clip.write_videofile(output_path, fps=24)

# Caminhos dos vídeos de entrada
# video1_path = "videos/HistoriaFilosofia/HistoriaFilosofia.mp4"
# video2_path = "videos/HistoriaFilosofia/HistoriaFilosofia_clipped.mp4"

# # Criar uma instância da classe VideoJoiner
# joiner = VideoJoiner(video1_path, video2_path)

# # Caminho para o vídeo de saída
# output_path = "videos/HistoriaFilosofia/HistoriaFilosofia_final.mp4"

# # Juntar os vídeos e salvar o resultado
# joiner.join_videos(output_path)
