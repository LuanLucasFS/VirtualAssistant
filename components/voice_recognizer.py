import speech_recognition as sr

class VoiceRecognizer: 
    def __init__(self): 
        self.recognizer = sr.Recognizer() # Inicializa o reconhecedor de voz

    def recognize(self, audio):
        try:
            print("Recognizing...")
            return self.recognizer.recognize_google(audio, language="pt-BR") # Reconhece o áudio
        except sr.UnknownValueError: # Se não entendeu o áudio
            return "Could not understand audio"
        except sr.RequestError as e: # Se não conseguiu acessar o serviço de reconhecimento de voz
            return f"Could not request results; {e}"

    def listen(self):
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...") 
            self.recognizer.adjust_for_ambient_noise(source, duration=1) # Ajusta o reconhecimento de voz para o ruído ambiente
            print("Say something!")
            audio = self.recognizer.listen(source) # Captura o áudio
            print("Audio captured!")
        return audio

    # Utilizar apenas para testes
    def save_audio(self, audio, filename="captured_audio.wav"):
        # Salva o áudio capturado em um arquivo WAV
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data()) # Escreve o áudio no arquivo
        print(f"Audio saved as {filename}")

def main():
    recognizer = VoiceRecognizer() # Inicializa o reconhecedor de voz
    audio = recognizer.listen()  # Captura o áudio

    # recognizer.save_audio(audio)  # Salva o áudio capturado, apenas para testes

    # Tenta reconhecer o áudio e imprime o texto
    print(recognizer.recognize(audio))

if __name__ == "__main__":
    main()

