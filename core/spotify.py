import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

SCOPE = (
    "user-read-playback-state user-modify-playback-state user-read-currently-playing "
    "playlist-read-private playlist-read-collaborative streaming"
)

if not CLIENT_ID or not CLIENT_SECRET:
    raise RuntimeError(
        "Spotify credentials não encontradas. Crie um arquivo .env na raiz com:\n"
        "SPOTIFY_CLIENT_ID=...\nSPOTIFY_CLIENT_SECRET=...\nSPOTIFY_REDIRECT_URI=..."
    )

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    open_browser=True
))

def _musica_atual():
    faixa = sp.current_playback()
    if faixa and faixa.get("item"):
        nome = faixa["item"]["name"]
        artistas = ", ".join([a["name"] for a in faixa["item"]["artists"]])
        return f"playing now: {nome} - {artistas}"
    return "Nenhuma música está tocando no momento."

def tocar_playlist_por_nome(nome_playlist: str, interface=None):
    try:
        playlists = []
        resultado = sp.current_user_playlists()
        while resultado:
            playlists.extend(resultado["items"])
            if resultado.get("next"):
                resultado = sp.next(resultado)
            else:
                break

        nome_playlist_l = nome_playlist.lower().strip()
        playlist_uri = None
        for playlist in playlists:
            if playlist["name"].lower().strip() == nome_playlist_l:
                playlist_uri = playlist["uri"]
                break

        if not playlist_uri:
            msg = f"Nenhuma playlist chamada '{nome_playlist}' foi encontrada."
            (interface.mostrar_mensagem(msg) if interface else print(msg))
            return

        devices = sp.devices()
        if not devices.get("devices"):
            msg = "Nenhum dispositivo do Spotify ativo foi encontrado. Abra o app do Spotify em algum lugar."
            (interface.mostrar_mensagem(msg) if interface else print(msg))
            return

        device = devices["devices"][0]
        device_id = device["id"]

        sp.transfer_playback(device_id, force_play=True)
        sp.start_playback(device_id=device_id, context_uri=playlist_uri)

        msg = f"Tocando playlist '{nome_playlist}' no dispositivo '{device['name']}'."
        (interface.mostrar_mensagem(msg) if interface else print(msg))

    except Exception as e:
        msg = f"Erro ao tentar tocar a playlist: {e}"
        (interface.mostrar_mensagem(msg) if interface else print(msg))

def proxima_musica(interface=None):
    try:
        devices = sp.devices()
        if not devices.get("devices"):
            msg = "Nenhum dispositivo ativo do Spotify foi encontrado."
            (interface.mostrar_mensagem(msg) if interface else print(msg))
            return

        sp.next_track()
        time.sleep(1)
        msg = _musica_atual()
        (interface.mostrar_mensagem(msg) if interface else print(msg))

    except Exception as e:
        msg = f"Erro ao tentar pular a música: {e}"
        (interface.mostrar_mensagem(msg) if interface else print(msg))

def musica_anterior(interface=None):
    try:
        devices = sp.devices()
        if not devices.get("devices"):
            msg = "Nenhum dispositivo ativo do Spotify foi encontrado."
            (interface.mostrar_mensagem(msg) if interface else print(msg))
            return

        sp.previous_track()
        time.sleep(1)
        msg = _musica_atual()
        (interface.mostrar_mensagem(msg) if interface else print(msg))

    except Exception as e:
        msg = f"Erro ao tentar voltar a música: {e}"
        (interface.mostrar_mensagem(msg) if interface else print(msg))

def definir_volume(valor, interface=None):
    try:
        estado = sp.current_playback()
        if not estado or not estado.get("device"):
            msg = "Nenhum dispositivo ativo foi encontrado no Spotify."
            (interface.mostrar_mensagem(msg) if interface else print(msg))
            return

        volume_atual = estado["device"]["volume_percent"]

        if isinstance(valor, int):
            novo_volume = max(0, min(100, valor))
        elif valor == "up":
            novo_volume = min(100, volume_atual + 10)
        elif valor == "down":
            novo_volume = max(0, volume_atual - 10)
        else:
            msg = "Comando de volume inválido."
            (interface.mostrar_mensagem(msg) if interface else print(msg))
            return

        sp.volume(novo_volume)
        msg = f"Volume ajustado para {novo_volume}%."
        (interface.mostrar_mensagem(msg) if interface else print(msg))

    except Exception as e:
        msg = f"Erro ao ajustar volume: {e}"
        (interface.mostrar_mensagem(msg) if interface else print(msg))