# 🎮 Noughts and Crosses (CGV Project)

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/MishraSudarshan/CGVProject)](https://github.com/MishraSudarshan/CGVProject/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/MishraSudarshan/CGVProject)](https://github.com/MishraSudarshan/CGVProject/network)
[![GitHub issues](https://img.shields.io/github/issues/MishraSudarshan/CGVProject)](https://github.com/MishraSudarshan/CGVProject/issues)

A simple **Noughts and Crosses (Tic-Tac-Toe)** game built for a **Computer Graphics & Visualization (CGV)** project, focused on web-based gameplay.

</div>

---

## 📖 Overview

This project implements the classic **Noughts and Crosses (Tic-Tac-Toe)** game using Python.  
It includes a simple game system with a **persistent leaderboard** stored in a text file.

The project is intended for **academic use**, learning purposes, and basic gameplay demonstration.

---

## ✨ Features

* Classic Noughts and Crosses gameplay  
* Persistent leaderboard using a text file  
* Web-focused structure (no executable files)  
* Python-based game logic  

---

## 🛠️ Tech Stack

* **Backend / Logic:** Python  
* **Frontend:** Web interface (extendable)  
* **Data Storage:** Text file (`leaderboard.txt`)  

---

## 🚀 Getting Started

### Prerequisites

* Python 3.x  
* Web browser  

---

## 🔧 Installation & Run

1. Clone the repository
   ```bash
   git clone https://github.com/MishraSudarshan/CGVProject.git
   cd CGVProject
   ```

2. Start the web server (from the **CGVProject** folder):
   ```bash
   python web/server.py
   ```

3. Open in your browser the URL shown in the terminal (e.g. **http://127.0.0.1:8000/**). If the terminal says a different port (e.g. 8765), use that.

### Running from a zip on another device

1. Extract the **entire** zip so you have the project folder (e.g. `CGVProject`) with a **web** folder inside it.
2. On the other device you need **Python 3** installed. Open a terminal in the project folder and run:
   ```bash
   python web/server.py
   ```
   (Or run `python` with the full path to `server.py`; it will find the files automatically.)
3. Use the **exact URL** printed in the terminal (e.g. `http://127.0.0.1:8000/`). If you see "Port 8000 was in use. Using port 8765", open `http://127.0.0.1:8765/` instead.
4. If the game does not load, check the terminal for errors or warnings (e.g. missing `app.js` or `styles.css` — then re-zip including the whole **web** folder).

---

## ⚙️ Configuration

leaderboard.txt stores player scores

File can be cleared manually if required

👨‍💻 Development

Edit noughtsandcrosses.py for game logic

Use play_game.py to test changes

Extend the web/ folder for UI improvements

🤝 Contributing

Fork the repository

Create a new branch

Make your changes

Submit a pull request