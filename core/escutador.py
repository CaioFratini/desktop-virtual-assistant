import speech_recognition as sr
from core.ativador import verificar_ativacao
from core.comandos import processar_comando

mensagem_anterior = ""

def mostrar_mensagem_unica(interface, mensagem):
    global mensagem_anterior
    if mensagem != mensagem_anterior:
        interface.mostrar_mensagem(mensagem)
        mensagem_anterior = mensagem

def iniciar_escuta(interface):
    reconhecedor = sr.Recognizer()
    mic = sr.Microphone()

    mostrar_mensagem_unica(interface, "link")

    while True:
        with mic as source:
            reconhecedor.adjust_for_ambient_noise(source, duration=1)
            mostrar_mensagem_unica(interface, "...")
            audio = reconhecedor.listen(source, phrase_time_limit=5)

        try:
            comando = reconhecer_audio(reconhecedor, audio)
            if comando and verificar_ativacao(comando):
                mostrar_mensagem_unica(interface, "whats up?")

                with mic as source:
                    reconhecedor.adjust_for_ambient_noise(source, duration=0.5)
                    audio = reconhecedor.listen(source, phrase_time_limit=6)

                comando = reconhecer_audio(reconhecedor, audio)
                if comando:
                    processar_comando(comando, interface)

                mostrar_mensagem_unica(interface, "chilling in the wired")

        except KeyboardInterrupt:
            mostrar_mensagem_unica(interface, "Encerrado pelo usuário.")
            break

def reconhecer_audio(reconhecedor, audio):
    try:
        return reconhecedor.recognize_google(audio, language="pt-BR").lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Erro ao acessar o serviço de reconhecimento.")
        return ""
