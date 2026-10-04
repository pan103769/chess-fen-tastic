# ♟️ Chess FEN-tastic

> **Bring any two-dimensional chess position to a digital, playable board in one click.**

### Ever seen a chess position and thought...

> "I want to analyze this on a board."

Then realized you have to manually place every single piece?

Yeah. No.

**Chess FEN-tastic** is a supercalifragilisticexpialidocious tool that turns a chess position from an image into a playable digital board in seconds.

---

## 🎥 See it in action

[Recording.2026-10-demo.also.solved.a.puzzle.mp4](https://github.com/user-attachments/assets/295e3b56-27d2-4324-8043-491a88122031)

**Select → Recognize → Play.**

That's basically it.

---

## 🧠 What's happening underneath?

```text
       2D CHESS POSITION
              │
              ▼
         📸 Screenshot
              │
              ▼
       🧠 GEMMA 4 CLOUD
              │
              ▼
     64 SQUARES RECOGNIZED
              │
              ▼
      🐍 PYTHON → FEN
              │
              ▼
       ♟️ LICHESS BOARD
```

Gemma looks at the position and identifies what's on each square.
Python takes that structured output and converts it into FEN.
Then the position gets opened on Lichess.
Gemma sees the board.
Python handles the notation (FEN).
Lichess makes it playable.

## ⚙️ Tech Stack

| Technology | Why |
|---|---|
| 🧠 **Gemma 4 Cloud** | Visual chess-position recognition |
| 🔗 **Ollama** | Connects Python to Gemma 4 Cloud |
| 🐍 **Python** | Core logic + FEN generation |
| ⌨️ **keyboard** | F8 hotkey detection |
| 🎨 **Tkinter** | Screenshot selection interface |
| 🖼️ **Pillow** | Captures and handles screenshots |
| 📦 **PyInstaller** | Packages the app into a Windows executable |


🚀 Run it
1. Clone
git clone https://github.com/pan103769/chess-fen-tastic.git
cd chess-fen-tastic

2. Install dependencies
pip install ollama pillow keyboard

3. Run
python main.py

Press F8, select the chess position, and let it do its thing.
🖥️ Windows
Don't want to run Python?
**[Download Chess FEN-tastic for Windows](https://github.com/pan103769/chess-fen-tastic/releases/tag/v1.0.0)**

Download → run → select position.



The full pipeline currently works✅:
Screenshot
   ↓
Gemma 4 Cloud
   ↓
64-square recognition
   ↓
FEN
   ↓
Validation
   ↓
Lichess board

And yes — you can do it again without restarting the program.
Because apparently one chess position wasn't enough.

- 📷 Photos of physical boards
- 📖 Chess books
- 🧩 Puzzle diagrams
- 🎥 Videos
- 🎨 Different board themes

♟️ Built for Hacktoberfest 2026
Built with open-source AI at its core.
Built because manually recreating a chess position is boring.
And built to make the gap between seeing a position and playing it basically disappear.
