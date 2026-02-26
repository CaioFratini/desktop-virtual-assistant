# Desktop Virtual Assistant

Desktop Virtual Assistant is a voice-controlled desktop application built with Python.  
It integrates with the Spotify Web API and provides a custom terminal-style graphical interface for real-time interaction.

This project was developed as a practical demonstration of API integration, modular architecture, desktop automation, and voice command processing.

---

## Version

Current version: v0.1.0  
Status: Active development (MVP)

This is a functional Minimum Viable Product. The architecture was designed to allow future feature expansion and structural improvements.

---

## Features

- Voice activation system
- Spotify Web API integration (Spotipy)
- Play playlist by name
- Next and previous track control
- Volume adjustment
- Real-time playback detection
- Windows executable discovery and launch
- Custom animated interface built with Tkinter and Pillow
- Modular project structure

---

## Technical Highlights

- Modular architecture separated into `core/` and `util/`
- Environment variable handling using `python-dotenv`
- Threaded microphone listening system
- Windows Registry scanning for executable detection
- Structured command processing pipeline
- Secure credential handling via `.env`

---

## Technologies Used

- Python 3.11
- Spotipy (Spotify Web API)
- SpeechRecognition
- Tkinter
- Pillow
- python-dotenv
- PyWin32

---

## Installation

Clone the repository: https://github.com/CaioFratini/desktop-virtual-assistant.git <br>
cd desktop-virtual-assistant

Install dependencies:  pip install -r requirements.txt

---

## Environment Configuration

Create a `.env` file in the project root:

SPOTIFY_CLIENT_ID=your_client_id <br>
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback

You must create a Spotify application at:
https://developer.spotify.com/dashboard

---

## Running the Application
python main.py <br>

---

## Project Structure 
core/ <br>
├── ativador.py <br>
├── comandos.py <br>
├── escutador.py <br>
├── interface.py <br>
├── spotify.py <br>
util/ <br>
└── busca_executavel.py <br>
main.py <br>
requirements.txt

---

## Architectural Overview

The system is divided into logical layers:

- `escutador.py` handles microphone input and activation detection.
- `ativador.py` verifies activation keywords.
- `comandos.py` processes recognized commands.
- `spotify.py` manages Spotify API interactions.
- `interface.py` renders the graphical terminal interface.
- `busca_executavel.py` performs Windows executable discovery via registry and filesystem scanning.

This separation improves maintainability and scalability.

---

## Future Improvements

- Enhanced natural language processing
- Persistent memory system
- Cross-platform compatibility
- Configuration interface
- Expanded command system

---

## License

This project is intended for educational and portfolio purposes.
## Intellectual Property and Usage Restrictions

© 2025 Caio Fratini. All rights reserved.

This project is published for educational, personal, and recreational use.  
Individuals are free to study, test, and use this software for non-commercial purposes.

Commercial use, corporate use, redistribution, sublicensing, or modification for business or enterprise purposes is strictly prohibited without explicit prior written authorization from the author.

Any malicious use of this software is also strictly prohibited.
