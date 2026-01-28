import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

class TikTokVideoEditor:
    def __init__(self, audio_path, image_folder, script):
        self.audio_path = audio_path
        self.image_folder = image_folder
        self.script = script

    def edit_video(self, output_path):
        # Remove a primeira linha e qualquer linha após o último número
        script_lines = self.extract_script_lines()

        # Carregar o arquivo de áudio
        audio_clip = AudioFileClip(self.audio_path)

        # Inicializar lista de clips de imagem
        image_clips = []

        # Adicionar uma imagem de preenchimento no início do vídeo
        filler_image_duration_start = 4.5
        filler_image_start = ImageClip("./imgFixa/gato.jpg").set_duration(filler_image_duration_start)
        image_clips.append(filler_image_start)

        for i, line in enumerate(script_lines[:-1]):  # Iterar até a penúltima linha
            duration = self.calculate_image_duration(line)
            # Ajustar o índice da linha para começar em 1
            line_index = i + 1
            images_for_line = self.load_images_for_line(line_index, duration)
            image_clips.extend(images_for_line)

        # Adicionar uma imagem de preenchimento entre a penúltima e a última linha
        filler_image_duration_middle = 2.8
        filler_image_middle = ImageClip("./imgFixa/bonus.jpg").set_duration(filler_image_duration_middle)
        image_clips.append(filler_image_middle)

        # Carregar a última linha do roteiro
        last_line = script_lines[-1]
        duration_last_line = self.calculate_image_duration(last_line)
        last_line_images = self.load_images_for_line(len(script_lines), duration_last_line)
        image_clips.extend(last_line_images)

        # Concatenar clips de imagem
        final_clip = concatenate_videoclips(image_clips, method="compose")

        # Adicionar áudio ao vídeo
        final_clip = final_clip.set_audio(audio_clip)

        # Redimensionar o vídeo para ocupar toda a altura mantendo a proporção
        final_clip = self.resize_video(final_clip, height=1920)

        # Definir o caminho para salvar o vídeo
        output_folder = os.path.join("videos", output_path)
        os.makedirs(output_folder, exist_ok=True)
        output_file_path = os.path.join(output_folder, f"{output_path}_top.mp4")

        # Salvar vídeo de saída
        final_clip.write_videofile(output_file_path, codec='libx264', audio=self.audio_path, remove_temp=True, fps=24)

    def extract_script_lines(self):
        # Encontrar o número total de linhas do roteiro
        total_lines = len(self.script)
        
        # Encontrar o número de linhas normais (excluindo a primeira e a última)
        normal_lines = total_lines - 3
        
        # Excluir a primeira linha e extrair as linhas normais
        script_lines = self.script[1:normal_lines + 1]
        
        # Extrair a última linha
        last_line = self.script[-1]
        
        # Adicionar a última linha à lista de linhas
        script_lines.append(last_line)
        
        return script_lines

    def calculate_image_duration(self, line):
        # Aplicar a fórmula à linha do script para determinar a duração do áudio
        num_chars = len(line)
        num_commas = line.count(',')
        num_periods = line.count('.')
        duration = (num_chars / 14) + (num_commas * 0.05) + (num_periods * 0.1)
        return duration

    def load_images_for_line(self, line_index, duration):
        # Adicionar zeros à esquerda ao número da linha
        line_number_padded = str(line_index).zfill(3)

        # Obter lista de imagens para a linha
        image_files = [os.path.join(self.image_folder, f"linha_{line_number_padded}_img_{i}.jpg") for i in range(6)]
        
        # Calcular a duração de cada imagem
        image_duration = duration / 6
        
        # Carregar os clips de imagem para a linha
        image_clips = []
        for image_file in image_files:
            image_clip = ImageClip(image_file, duration=image_duration)
            # Redimensionar a imagem para ocupar toda a altura mantendo a proporção
            image_clip = image_clip.resize(height=1920)
            image_clips.append(image_clip)

        return image_clips

    def resize_video(self, video_clip, height):
        # Redimensionar o vídeo mantendo a proporção
        return video_clip.resize(height=height)

# Exemplo de uso da classe
# if __name__ == "__main__":
#     # Caminho para o arquivo de áudio
#     audio_path = "./audios/audio_A história da filosofia_147.mp3"
    
#     # Caminho para a pasta com as imagens
#     image_folder = "img/A história da filosofia"

#     # Nome do vídeo de saída
#     output_path = "HistoriaFilosofia"

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

#     # Caminho do vídeo de saída
#     video_path = "./videos/HistoriaFilosofiaImg"

#     editor = TikTokVideoEditor(audio_path, image_folder, script)
#     editor.edit_video(output_path)
