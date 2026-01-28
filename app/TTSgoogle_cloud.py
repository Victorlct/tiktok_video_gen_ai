import os
from google.cloud import texttospeech

credentials_path = os.path.abspath("google-cloud-credentials.json")

# Define o caminho absoluto para as credenciais de serviço
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

def gerar_audio(theme_name, theme_id, text):
    """Sintetiza o texto em áudio."""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        name="pt-BR-Wavenet-B",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    # Define o caminho para a pasta "audios"
    audios_folder = "audios"
    # Verifica se a pasta existe, se não, a cria
    if not os.path.exists(audios_folder):
        os.makedirs(audios_folder)

    # Define o nome do arquivo de áudio com base no theme_name e theme_id
    audio_file_name = f"audio_{theme_name}_{theme_id}.mp3"
    # Define o caminho completo para o arquivo de áudio na pasta "audios"
    audio_file_path = os.path.join(audios_folder, audio_file_name)

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # Salva o áudio em um arquivo
    with open(audio_file_path, "wb") as out:
        out.write(response.audio_content)
    print(f'Áudio salvo como "{audio_file_name}" na pasta audios')

def list_voices():
    """Lists the available voices."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    # Realiza a solicitação de listagem de vozes
    voices = client.list_voices(language_code="pt-BR")

    print("Vozes disponíveis em português (pt-BR):")
    for voice in voices.voices:
        # Exibe o nome da voz
        print(f"Nome: {voice.name}")

        # Exibe os códigos de idioma suportados para esta voz
        for language_code in voice.language_codes:
            print(f"Código de idioma suportado: {language_code}")

        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # Exibe o gênero da voz SSML
        print(f"Gênero da voz SSML: {ssml_gender.name}")

        # Exibe a taxa de amostragem natural em hertz para esta voz
        print(f"Taxa de amostragem natural em Hertz: {voice.natural_sample_rate_hertz}\n")