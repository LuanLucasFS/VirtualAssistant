import components.VoiceRecognizer.voice_recognizer as voice_recognizer
import components.Ai.test_ai_conn as ai_connection
import components.Text_To_Speech.text_to_speech as text_to_speech

def main():
    recognizer = voice_recognizer.VoiceRecognizer()  # Inicializa o reconhecedor de voz
    ai = ai_connection.aiConn()  # Inicializa a conexão com o serviço de AI
    tts = text_to_speech.TextToSpeech() # Inicializa o sintetizador de voz

    while True:
        audio = recognizer.listen()  # Captura o áudio

        # recognizer.save_audio(audio)  # Salva o áudio capturado, apenas para testes

        # Tenta reconhecer o áudio e imprime o texto
        user_input = recognizer.recognize(audio)
        print("User:", user_input)
        if(user_input != "Could not understand audio"):
            if user_input.lower() == 'sair':
                tts.speak("Saindo do chatbot. Adeus!")
                print("Saindo do chatbot. Adeus!")
                break

            # Envia a solicitação para o serviço de AI e imprime a resposta
            response = ai.send_request(user_input)
            if "error" in response:
                print("Bot:", response["error"])
            else:
                bot_response = response.get("choices", [{}])[0].get("message", {}).get("content", "No response available.")
                
                print("Bot:", bot_response)
                
            

if __name__ == "__main__":
    main()