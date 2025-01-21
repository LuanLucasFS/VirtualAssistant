import sys
import os
import requests
from components.Text_To_Speech.text_to_speech import TextToSpeech
from components.properties_Reader import PropertiesReader

class aiConn:
    # Adiciona o diretório raiz ao sys.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

    # Inicializa a instância de TextToSpeech
    tts = TextToSpeech()

    # Carregar as propriedades
    props = PropertiesReader.load_properties("components/AI/ai.properties")
    BASE_URL = props.get("BASE_URL")
    HEADERS = props.get("HEADERS")

    global frase
    # Ignorar palavras comuns
    ignore_words = ["por", "favor", "o", "a", "é", "os", "as", "que", "tadeu"]

    def __init__(self):
        self.session = requests.Session()

    def set_frase(self, f):
        """Divide a frase e remove as palavras comuns."""
        frase = [word for word in f.lower().split() if word not in aiConn.ignore_words]
        return ' '.join(frase)

    @staticmethod
    def send_request(message, temperature=0.4, max_tokens=500):
        """Envia uma solicitação para o serviço de AI e retorna a resposta."""
        payload = {
            "messages": [
                {"role": "system", "content": "Você é um assistente chamado tadeu"},
                {"role": "user", "content": message}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            response = requests.post(aiConn.BASE_URL, headers=aiConn.HEADERS, json=payload)
            response.raise_for_status()  # Lança exceção para códigos de erro HTTP
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def main(self):
        """Função principal que interage com o usuário."""
        user_input = frase  # Você pode substituir isso por input() se necessário
        if user_input.lower() == 'quit':
            print("Exiting the chatbot. Goodbye!")
            return
        response = aiConn.send_request(user_input)
        if "error" in response:
            print("Bot:", response["error"])
        else:
            bot_response = response.get("choices", [{}])[0].get("message", {}).get("content", "No response available.")
            self.tts.speak(bot_response)
            print("Bot:", bot_response)
            

if __name__ == "__main__":
    ai_instance = aiConn()
    ai_instance.main()
