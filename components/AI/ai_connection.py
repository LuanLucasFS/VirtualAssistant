import sys
import os
import requests

class aiConn:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

    BASE_URL="http://localhost:1234/v1/chat/completions"
    HEADERS={"Content-Type": "application/json"}

    global frase
    ignore_words = ["por", "favor", "o", "a", "é", "os", "as", "que", "tadeu"]

    def __init__(self):
        self.session = requests.Session()
        # Histórico inicial com a mensagem do 'system' (não com o papel de 'user')
        self.conversation_history = [{"role": "system", "content": "Você é um assistente chamado Tadeu."}]
        print(f"Initial history: {self.conversation_history}")  # Debug: Mostra o histórico inicial

    def set_frase(self, f):
        frase = [word for word in f.lower().split() if word not in aiConn.ignore_words]
        return ' '.join(frase)

    def add_to_conversation_history(self, role, content):
        """Adiciona a mensagem do usuário ou do bot ao histórico de conversa."""
        self.conversation_history.append({"role": role, "content": content})
        print(f"History updated: {self.conversation_history}")  # Debug: Mostra o histórico atualizado

    def send_request(self, message, temperature=0.4, max_tokens=500):
        """Envia uma solicitação para o serviço de AI com o histórico de mensagens."""
        print(f"Sending message with history: {self.conversation_history}")  # Debug: Mostra o histórico enviado
        payload = {
            "messages": self.conversation_history + [{"role": "user", "content": message}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            # Adiciona a mensagem do usuário ao histórico
            self.add_to_conversation_history("user", message)

            # Envia a requisição ao serviço de IA
            response = requests.post(aiConn.BASE_URL, headers=aiConn.HEADERS, json=payload)
            response.raise_for_status()
            response_data = response.json()

            # Extrai a resposta da IA
            bot_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response available.")

            # Adiciona a resposta da IA ao histórico
            self.add_to_conversation_history("assistant", bot_response)

            return response_data
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}


    def main(self):
        # Pergunta ou frase do usuário, pode ser fornecida via input()
        user_input = "Qual é o tema da conversa?"  # Exemplo de pergunta. Alterar conforme necessário.

        # Adiciona a pergunta do usuário ao histórico
        self.add_to_conversation_history("user", user_input)

        # Envia a solicitação com o histórico completo
        response = self.send_request(user_input)
        if "error" in response:
            print("Bot:", response["error"])
        else:
            bot_response = response.get("choices", [{}])[0].get("message", {}).get("content", "No response available.")
            # Adiciona a resposta do bot ao histórico
            self.add_to_conversation_history("assistant", bot_response)

            # Responde ao usuário com a voz e o texto
            print("Bot:", bot_response)

if __name__ == "__main__":
    ai_instance = aiConn()
    ai_instance.main()
