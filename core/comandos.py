from util.busca_executavel import encontrar_executavel
from subprocess import Popen
import os
import re
from core.spotify import tocar_playlist_por_nome, proxima_musica, musica_anterior, definir_volume

def interpretar_comando_volume(comando):
    comando = comando.lower()
    if "volume máximo" in comando:
        return 100
    elif "volume mínimo" in comando:
        return 0
    elif "aumentar volume" in comando:
        return "up"
    elif "diminuir volume" in comando:
        return "down"
    elif "volume" in comando:
        match = re.search(r"volume\s*(\d+)", comando)
        if match:
            valor = int(match.group(1))
            return min(100, max(0, valor))
    return None

def processar_comando(comando: str, interface):
    comando = comando.strip().lower()

    if comando.startswith("abrir "):
        app_name = comando.replace("abrir ", "", 1)
        caminho = encontrar_executavel(app_name)
        if caminho:
            interface.mostrar_mensagem(f"Abrindo {app_name.capitalize()} → {caminho}")
            Popen(f'start "" "{caminho}"', shell=True)
        else:
            interface.mostrar_mensagem(f"Não encontrei nenhum executável parecido com '{app_name}'.")

    elif comando.startswith("tocar playlist "):
        nome_playlist = comando.replace("tocar playlist ", "", 1)
        tocar_playlist_por_nome(nome_playlist, interface)

    elif comando in ["proxima musica", "próxima música", "pular música"]:
        proxima_musica(interface)

    elif comando in ["musica anterior", "música anterior", "voltar música"]:
        musica_anterior(interface)

    elif comando in ["sair", "encerrar", "desligar"]:
        interface.mostrar_mensagem("Encerrando assistente...")
        os._exit(0)

    elif "volume" in comando:
        valor = interpretar_comando_volume(comando)
        if valor is not None:
            definir_volume(valor, interface)
        else:
            interface.mostrar_mensagem("Comando de volume não reconhecido.")

    else:
        interface.mostrar_mensagem("theres not such thing ")
