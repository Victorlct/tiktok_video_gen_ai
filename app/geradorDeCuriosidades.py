import json
import google.generativeai as genai

class APIService:
    def __init__(self, config_file="./config/appsettings.json"):
        with open(config_file) as f:
            config = json.load(f)
        self.api_key = config["api_key"]
        genai.configure(api_key=self.api_key)
        self.model_name = "gemini-pro"  # Escolha do modelo apropriado

    def generate_video_script(self, theme):
        # Construir o prompt com base no tema
        prompt = f'Gere 6 curiosidades resumidas sobre {theme} e mais uma curiosidade bonus mais surpreendente que as outras, assuma que as curiosidades geradas serão um roteiro para a gravação de um vídeo, então dê um titulo, por exemplo, "6 curiosidades incriveis sobre {theme} que você não vai acreditar". Certifique-se de não incluir palavras como: Titulo, introducao e despidida, visto que é um roteiro pronto para ser lido.'

        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(prompt)
        response_text = response.text
        return self.clean_text(response_text)  # Retorna o texto gerado

    def clean_text(self, raw_text):
        # Remover caracteres indesejados
        cleaned_text = raw_text.replace('**', '')  # Remover marcação de negrito
        cleaned_text = cleaned_text.replace('\n\n', '\n')  # Remover linhas em branco extras
        cleaned_text = cleaned_text.replace('\n', '\n\n')  # Adicionar duas quebras de linha entre cada curiosidade

        # Dividir o texto em curiosidades separadas
        curiosities = cleaned_text.split('\n\n')
        
        return curiosities
