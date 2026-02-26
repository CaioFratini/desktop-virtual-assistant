import os
import subprocess
import difflib
import winreg
from pathlib import Path

def _buscar_no_registro(nome_exe: str) -> str | None:
    chaves = [
        (winreg.HKEY_CURRENT_USER,  r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths")
    ]
    for root, sub in chaves:
        try:
            with winreg.OpenKey(root, fr"{sub}\{nome_exe}.exe") as k:
                caminho, _ = winreg.QueryValueEx(k, None)
                if Path(caminho).is_file():
                    return caminho
        except FileNotFoundError:
            continue
    return None

def _atalhos_menu_iniciar() -> list[Path]:
    pastas = [
        Path(os.getenv("APPDATA", r"")) / r"Microsoft\Windows\Start Menu\Programs",
        Path(os.getenv("PROGRAMDATA", r"")) / r"Microsoft\Windows\Start Menu\Programs"
    ]
    links = []
    for pasta in pastas:
        if pasta.exists():
            links.extend(pasta.rglob("*.lnk"))
    return links

def _resolver_atalho(lnk: Path) -> str | None:
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        caminho = Path(shell.CreateShortcut(str(lnk)).Targetpath)
        return str(caminho) if caminho.is_file() else None
    except Exception:
        return None

def _scan_pastas_bem_conhecidas(nome_exe: str) -> str | None:
    candidatos = []
    bases = [
        Path(os.getenv("ProgramFiles",  r"C:\Program Files")),
        Path(os.getenv("ProgramFiles(x86)", r"C:\Program Files (x86)")),
        Path(os.getenv("LOCALAPPDATA", r""))
    ]
    for base in bases:
        if base.exists():
            for exe in base.rglob("*.exe"):
                candidatos.append(exe)
    base_names = [exe.stem.lower() for exe in candidatos]
    possivel = difflib.get_close_matches(nome_exe.lower(), base_names, n=1, cutoff=0.8)
    if possivel:
        idx = base_names.index(possivel[0])
        return str(candidatos[idx])
    return None

_cache: dict[str, str] = {}

def encontrar_executavel(alvo: str) -> str | None:
    alvo = alvo.lower()
    if alvo in _cache:
        return _cache[alvo]

    caminho = _buscar_no_registro(alvo)
    if not caminho:
        nomes = []
        mapa = {}
        for lnk in _atalhos_menu_iniciar():
            nome = lnk.stem.lower()
            destino = _resolver_atalho(lnk)
            if destino:
                nomes.append(nome)
                mapa[nome] = destino
        possivel = difflib.get_close_matches(alvo, nomes, n=1, cutoff=0.8)
        if possivel:
            caminho = mapa[possivel[0]]
    if not caminho:
        caminho = _scan_pastas_bem_conhecidas(alvo)

    if caminho:
        _cache[alvo] = caminho
    return caminho

#