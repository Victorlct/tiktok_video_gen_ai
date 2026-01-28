import json
import os
import string
import random
from datetime import datetime
from aplicarLegenda import geradorLegenda
from juntarVideos import VideoJoiner
from geradorClipYT import VideoClipper
from moviepy.editor import VideoFileClip 
from editarClipFoto import TikTokVideoEditor
from geradorDeCuriosidades import APIService
from TTSgoogle_cloud import gerar_audio
from geradorDeImagensBing import download_images_bing, geradorPromptImagens

def carregar_temas_utilizados():
    try:
        with open("./temas/temas_usados.json", "r", encoding="utf-8") as used_themes_file:
            used_themes = json.load(used_themes_file)
            if not isinstance(used_themes, list):
                used_themes = []  # Se não for uma lista, inicialize como uma lista vazia
    except FileNotFoundError:
        used_themes = []  # Se o arquivo não existir, inicialize como uma lista vazia
    return used_themes

def carregar_roteiros_prontos():
    try:
        with open("./roteiros/roteiros_prontos.json", "r", encoding="utf-8") as roteiros_prontos_file:
            roteiros_prontos = json.load(roteiros_prontos_file)
            if not isinstance(roteiros_prontos, list):
                roteiros_prontos = []  # Se não for uma lista, inicialize como uma lista vazia
    except FileNotFoundError:
        roteiros_prontos = []  # Se o arquivo não existir, inicialize como uma lista vazia
    return roteiros_prontos

def carregar_temas_disponiveis():
    with open("./temas/temas.json", "r", encoding="utf-8") as themes_file:
        themes = json.load(themes_file)
    return themes

def escolher_tema_aleatorio(available_themes):
    return random.choice(available_themes)

def marcar_tema_utilizado(used_themes, theme_id, theme_name):
    used_theme_entry = {
        "id": theme_id,
        "nome_tema": theme_name,
        "data_utilizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    used_themes.append(used_theme_entry)
    with open("./temas/temas_usados.json", "w", encoding="utf-8") as used_themes_file:
        json.dump(used_themes, used_themes_file, indent=4, ensure_ascii=False)

def gerar_roteiro(theme_name):
    api_service = APIService()
    script = api_service.generate_video_script(theme_name)
    return script

def salvar_roteiro_gerado(roteiros_prontos, theme_id, theme_name, script):
    roteiro_pronto_entry = {
        "id": theme_id,
        "tema": theme_name,
        "texto_roteiro": script,
        "data_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "utilizado": False
    }
    roteiros_prontos.append(roteiro_pronto_entry)
    with open("./roteiros/roteiros_prontos.json", "w", encoding="utf-8") as roteiros_prontos_file:
        json.dump(roteiros_prontos, roteiros_prontos_file, indent=4, ensure_ascii=False)

def gerar_imagens(roteiros_prontos, theme_name, gerador_prompt_imagens):
    for roteiro in roteiros_prontos:
        i = 1
        if roteiro["tema"] == theme_name:
            texto_roteiro = roteiro["texto_roteiro"]
            # Ignora a primeira e a penúltima linha
            for line in texto_roteiro[1:-1]:
                translator = str.maketrans('', '', string.punctuation + '""\'\'*/:')
                first_seven_words = " ".join(line.translate(translator).split()[:7])
                sequence_number = str(i).zfill(3)
                prompt = gerador_prompt_imagens.gerarPromptImagem(first_seven_words)
                download_images_bing(prompt, 6, theme_name, sequence_number)
                i += 1

            # Última linha
            last_line = texto_roteiro[-1]
            first_seven_words_last_line = " ".join(last_line.split()[:7])
            sequence_number = str(i).zfill(3)
            prompt = gerador_prompt_imagens.gerarPromptImagem(first_seven_words_last_line)
            download_images_bing(prompt, 6, theme_name, sequence_number)

def editar_video(theme_name, theme_id, script):
    audio_path = f"./audios/audio_{theme_name}_{theme_id}.mp3"
    image_folder = f"img/{theme_name}"
    editor = TikTokVideoEditor(audio_path, image_folder, script)
    editor.edit_video(theme_name)

def main():
    used_themes = carregar_temas_utilizados()
    roteiros_prontos = carregar_roteiros_prontos()
    themes = carregar_temas_disponiveis()

    available_themes = [theme for theme in themes if theme["id"] not in [theme_entry["id"] for theme_entry in used_themes]]

    if not available_themes:
        print("Todos os temas já foram utilizados.")
        return

    selected_theme = escolher_tema_aleatorio(available_themes)
    theme_id = selected_theme["id"]
    theme_name = selected_theme["tema"]

    marcar_tema_utilizado(used_themes, theme_id, theme_name)

    script = gerar_roteiro(theme_name)

    if "error" in script:
        print("Erro ao gerar o roteiro:", script["error"])
    else:
        salvar_roteiro_gerado(roteiros_prontos, theme_id, theme_name, script)
        print("Roteiro gerado com sucesso")
        gerar_audio(theme_name, theme_id, '.\n'.join(script) + '.')

        gerador_prompt_imagens = geradorPromptImagens()
        gerar_imagens(roteiros_prontos, theme_name, gerador_prompt_imagens)

        # Editar o vídeo e obter a duração do vídeo gerado
        editar_video(theme_name, theme_id, script)
        duration_seconds = obter_duracao_video(theme_name)

        # Agora, vamos chamar o VideoClipper para o vídeo inferior
        video_source_folder = "YoutubeVideos"  # Caminho da pasta de vídeos
        output_folder = f"videos/{theme_name}/{theme_name}"  # Nome do tema para o diretório de saída
        clipper = VideoClipper(video_source_folder)
        clipper.clip_video(duration_seconds, output_folder)

        # Agora, vamos unir os vídeos
        video1_path = f"videos/{theme_name}/{theme_name}_top.mp4"
        video2_path = f"videos/{theme_name}/{theme_name}_bottom.mp4"
        output_merge_path = f"videos/{theme_name}/{theme_name}_merge.mp4"

        joiner = VideoJoiner(video1_path, video2_path)
        joiner.join_videos(output_merge_path)

        output_merge_with_subtitles_path = f"videos/{theme_name}/{theme_name}_final.mp4"

        subtitle_generator = geradorLegenda(script)
        subtitle_generator.generate_subtitles(output_merge_path, output_merge_with_subtitles_path)

def obter_duracao_video(output_path):
    video_path = f"videos/{output_path}/{output_path}_top.mp4"
    if os.path.exists(video_path):
        video_clip = VideoFileClip(video_path)
        duration_seconds = video_clip.duration
        return duration_seconds
    else:
        print(f"O vídeo {output_path}.mp4 não foi encontrado. Erro ao obter duracao do video top.")
        return None

if __name__ == "__main__":
    main()
