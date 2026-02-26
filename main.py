import threading
from core.interface import LainInterface
from core.escutador import iniciar_escuta

def iniciar():
    interface = LainInterface()
    interface.mostrar_mensagem("connect to the wired")

    threading.Thread(target=iniciar_escuta, args=(interface,), daemon=True).start()

    interface.iniciar()

if __name__ == "__main__":
    iniciar()
