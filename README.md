This is the project structure
lyra-assistant/
│
├── app.py                    # Flask server
├── lyra_core.py              # Whisper + command logic + responses
├── requirements.txt
├── templates/
│   └── index.html            # Your Tailwind UI (modified)
│
├── static/
│   ├── js/
│   │   └── main.js           # mic recording + send to backend
│   └── css/
│       └── style.css         # optional
│
└── README.md
## Requirements
- Python 3.8+
- ffmpeg installed & on PATH
- Optional: CUDA + torch+cuda for faster whisper (install matching torch)

 Install:
   pip install -r requirements.txt

 Run:
   python app.py

 Open browser at:
   http://127.0.0.1:5000
