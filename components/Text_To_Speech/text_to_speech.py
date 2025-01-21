import pyttsx3
import os
import sys

class TextToSpeech:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

    from components.properties_Reader import PropertiesReader as pr

    def __init__(self):
        # Carregar as propriedades
        props = self.pr.load_properties(os.path.join(os.path.dirname(__file__), "tts.properties"))

        # Converta para os tipos corretos com valores padrão
        rate = int(props.get("rate", "250"))  # Valor padrão: 200
        volume = float(props.get("volume", "0.8"))  # Valor padrão: 0.8
        voice = int(props.get("voice", "0"))  # Valor padrão: 0

        print(f"Rate: {rate}, Volume: {volume}, Voice: {voice}")

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        self.engine.setProperty('voice', self.engine.getProperty('voices')[voice].id)

    def speak(self, text):
        self.engine.say(text.replace("*", ""))
        self.engine.runAndWait()

def main():
    tts = TextToSpeech()
    tts.speak("Olá, mundo!")

if __name__ == "__main__":
    main()
