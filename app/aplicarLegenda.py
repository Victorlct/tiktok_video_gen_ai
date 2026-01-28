from os.path import  splitext
import math
from moviepy.editor import TextClip
from moviepy.editor import CompositeVideoClip
from moviepy.editor import VideoFileClip


class geradorLegenda:
    def __init__(self, script_lines):
        self.script_lines = script_lines

    def generate_subtitles(self, video_path, output_path):
        # Carregar o clipe de vídeo
        video_clip = VideoFileClip(video_path)

        # Calcula a duração total do vídeo
        total_duration = video_clip.duration

        # Inicializa lista para armazenar os clipes de texto
        text_clips = []

        # Calcula o tempo inicial para cada linha de legenda
        start_time = 0
        for line in self.script_lines:
            # Calcula o tempo de exibição da linha
            duration = self.calculate_duration(line)
            
            # Divide a linha em clipes de no máximo 4 palavras
            words = line.split()
            num_clips = math.ceil(len(words) / 4)
            clip_duration = duration / num_clips
            
            for i in range(num_clips):
                start = start_time + i * clip_duration
                end = min(start_time + (i + 1) * clip_duration, total_duration)
                clip_words = ' '.join(words[i * 4 : (i + 1) * 4])

                # Verifica se a legenda precisa ser dividida em duas linhas
                if len(clip_words) > 26:
                    half_length = len(clip_words) // 2
                    # Procura pelo espaço mais próximo para dividir a string
                    space_index = clip_words.rfind(' ', 0, half_length)
                    # Divide a string no espaço mais próximo
                    first_line = clip_words[:space_index]
                    second_line = clip_words[space_index + 1:]
                    # Cria clipes de texto para cada linha
                    first_clip = (TextClip(first_line, fontsize=100, color='black', stroke_color='white', stroke_width=8, font="Porky")
                                .set_duration(clip_duration)
                                .set_position(('center', 830))  # Define a posição do primeiro texto como centro superior
                                .set_start(start)
                                .set_end(end))
                    second_clip = (TextClip(second_line, fontsize=100, color='black', stroke_color='white', stroke_width=8, font="Porky")
                                .set_duration(clip_duration)
                                .set_position(('center', 950))  # Define a posição do segundo texto como centro inferior
                                .set_start(start)
                                .set_end(end))
                    # Adiciona os clipes de texto à lista
                    text_clips.append(first_clip)
                    text_clips.append(second_clip)
                else:
                    # Cria um clipe de texto com a legenda no topo centralizado
                    text_clip = (TextClip(clip_words, fontsize=100, color='black', stroke_color='white', stroke_width=8, font="Porky")
                                    .set_duration(clip_duration)
                                    .set_position(('center'))  # Define a posição do texto como centro superior
                                    .set_start(start)
                                    .set_end(end))
                    # Adiciona o clipe de texto à lista
                    text_clips.append(text_clip)
            
            start_time += duration
        
        # Combina os clipes de texto com o vídeo original
        video_with_subtitles = CompositeVideoClip([video_clip] + text_clips)

        # Salva o vídeo com legendas
        video_with_subtitles.write_videofile(output_path, codec='libx264', remove_temp=True)

    def calculate_duration(self, line):
        # Aplicar a fórmula à linha do script para determinar a duração do áudio
        num_chars = len(line)
        num_commas = line.count(',')
        num_periods = line.count('.')
        duration = (num_chars / 14) + (num_commas * 0.05) + (num_periods * 0.1)
        return duration


# Exemplo de uso da classe
# if __name__ == "__main__":
#     # Script do vídeo
#     script = [
#         "6 Curiosidades Inacreditáveis sobre a História da Filosofia",
#         "1. Pitágoras acreditava na transmigração da alma, o que significa que sua alma poderia retornar em um animal após a morte.",
#         "2. Sócrates ensinou seus alunos fazendo perguntas em vez de dar palestras, um método conhecido como método socrático.",
#         "3. Platão acreditava que havia um mundo perfeito de Formas que não podia ser percebido pelos sentidos.",
#         "4. Aristóteles argumentou que a felicidade é o objetivo principal da vida humana e que ela pode ser alcançada através da virtude.",
#         "5. Epicuro acreditava que o prazer era a coisa mais importante na vida e que a felicidade podia ser alcançada evitando a dor.",
#         "6. René Descartes é famoso por sua declaração \"Penso, logo existo\", que se tornou um princípio fundamental da filosofia moderna.",
#         "Curiosidade Bônus Surpreendente:",
#         "O filósofo grego Diógenes, também conhecido como Diógenes, o Cínico, viveu em um barril e desprezava as convenções sociais, acreditando que a verdadeira felicidade vinha da simplicidade e da autossuficiência."
#     ]

#     video_path = "./videos/HistoriaFilosofia/video_final.mp4"
#     subtitle_generator = geradorLegenda(script)
#     subtitle_generator.generate_subtitles(video_path, video_path)
