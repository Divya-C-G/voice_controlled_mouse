# Voice-Controlled Mouse 🎙️🖱️

This project implements a voice-controlled virtual mouse using Python and a web-based interface. It enables hands-free control of the mouse cursor using voice commands, making computer interaction more accessible and innovative.

## 🚀 Features

-  Voice command recognition
-  Cursor movement and clicks via voice
-  Web-based UI with conversational interface
-  Intelligent response using integrated AI logic (Proton.py)

## 🛠️ Tech Stack

- Frontend: HTML, CSS, JavaScript (jQuery)
- Backend: Python (Flask)
- Voice Recognition: SpeechRecognition, PyAudio
- Automation: PyAutoGUI

## 📂 Project Structure

voice_controlled_mouse/
├── app.py                  # Flask backend application
├── Proton.py              # Custom AI response logic
├── web/
│   ├── index.html         # Main chat interface
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript logic
│   └── images/            # Icons and background
└── README.md              # Project documentation
```

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/voice-controlled-mouse.git
   cd voice-controlled-mouse
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not available, install manually:
   ```bash
   pip install Flask SpeechRecognition PyAudio PyAutoGUI
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and go to:
   ```
   http://localhost:5000
   ```

##  Usage

- Use the chat interface to type or speak commands like:
  - "Move mouse left"
  - "Click right"
  - "Scroll down"

##  Future Enhancements

-  Add gesture control
-  Multilingual voice support
-  User authentication
-  Command analytics


