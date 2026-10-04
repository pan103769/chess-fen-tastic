import ollama
import webbrowser
import keyboard
import tkinter as tk
from PIL import ImageGrab

MODEL = "gemma4:cloud"
IMAGE = "chessposition2.png"

files = "abcdefgh"

piece_to_fen = {
    "white_king": "K",
    "white_queen": "Q",
    "white_rook": "R",
    "white_bishop": "B",
    "white_knight": "N",
    "white_pawn": "P",
    "black_king": "k",
    "black_queen": "q",
    "black_rook": "r",
    "black_bishop": "b",
    "black_knight": "n",
    "black_pawn": "p",
    "empty": ""
}

expected_squares = [
    f"{file}{rank}"
    for rank in range(8, 0, -1)
    for file in files
]


def wait_for_hotkey():
    print("\n================================")
    print("READY")
    print("================================")
    print("Press F8 to capture the chessboard.")
    print("")

    keyboard.wait("f8")


def take_screenshot():
    root = tk.Tk()

    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.25)
    root.configure(cursor="cross")

    canvas = tk.Canvas(root, cursor="cross")
    canvas.pack(fill="both", expand=True)

    start_x = 0
    start_y = 0
    rectangle = None

    def mouse_down(event):
        nonlocal start_x, start_y, rectangle

        start_x = event.x
        start_y = event.y

        rectangle = canvas.create_rectangle(
            start_x,
            start_y,
            start_x,
            start_y,
            outline="red",
            width=2
        )

    def mouse_move(event):
        if rectangle:
            canvas.coords(
                rectangle,
                start_x,
                start_y,
                event.x,
                event.y
            )

    def mouse_up(event):
        x1 = min(start_x, event.x)
        y1 = min(start_y, event.y)
        x2 = max(start_x, event.x)
        y2 = max(start_y, event.y)

        root.destroy()

        image = ImageGrab.grab(
            bbox=(x1, y1, x2, y2)
        )

        image.save(IMAGE)

        print("\nScreenshot saved.")

    canvas.bind("<ButtonPress-1>", mouse_down)
    canvas.bind("<B1-Motion>", mouse_move)
    canvas.bind("<ButtonRelease-1>", mouse_up)

    root.mainloop()


def recognize_board():

    prompt = """
Analyze the chessboard image and reconstruct the exact chess position.

Identify EVERY ONE of the 64 squares.

Use these exact chess coordinates:

a8 b8 c8 d8 e8 f8 g8 h8
a7 b7 c7 d7 e7 f7 g7 h7
a6 b6 c6 d6 e6 f6 g6 h6
a5 b5 c5 d5 e5 f5 g5 h5
a4 b4 c4 d4 e4 f4 g4 h4
a3 b3 c3 d3 e3 f3 g3 h3
a2 b2 c2 d2 e2 f2 g2 h2
a1 b1 c1 d1 e1 f1 g1 h1

For every square, output exactly one of:

empty
white_king
white_queen
white_rook
white_bishop
white_knight
white_pawn
black_king
black_queen
black_rook
black_bishop
black_knight
black_pawn

Also determine the side to move.

IMPORTANT:
- Output EVERY square.
- Do not skip squares.
- Do not output FEN.
- Do not explain anything.
- Do not use Markdown.
- Do not use code blocks.

Output exactly this format:

a8: piece
b8: piece
c8: piece
...
h1: piece
side_to_move: white

Replace "piece" with the correct value.
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [IMAGE]
            }
        ],
        options={"temperature": 0},
        think=False
    )

    return response["message"]["content"].strip()


def parse_board(content):

    board = {}
    turn = None

    for line in content.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("side_to_move:"):
            turn = line.split(":", 1)[1].strip()
            continue

        if ":" not in line:
            continue

        square, piece = line.split(":", 1)

        square = square.strip()
        piece = piece.strip()

        if square in expected_squares:
            board[square] = piece

    missing = [
        square
        for square in expected_squares
        if square not in board
    ]

    if missing:

        print("\nERROR: Missing squares:")
        print(missing)

        return None, None

    return board, turn


def generate_fen(board, turn):

    fen_ranks = []

    for rank in range(8, 0, -1):

        fen_rank = ""
        empty_count = 0

        for file in files:

            square = f"{file}{rank}"
            piece = board[square]

            if piece == "empty":

                empty_count += 1

            else:

                if empty_count:

                    fen_rank += str(empty_count)
                    empty_count = 0

                if piece not in piece_to_fen:

                    print(
                        f"\nERROR: Unknown piece "
                        f"'{piece}' on {square}"
                    )

                    return None

                fen_rank += piece_to_fen[piece]

        if empty_count:
            fen_rank += str(empty_count)

        fen_ranks.append(fen_rank)

    piece_placement = "/".join(fen_ranks)

    if turn == "white":
        side = "w"

    elif turn == "black":
        side = "b"

    else:

        print(
            "\nERROR: Invalid side_to_move:",
            turn
        )

        return None

    return f"{piece_placement} {side} - - 0 1"


def validate_fen(fen):

    parts = fen.split()

    if len(parts) != 6:
        return False

    ranks = parts[0].split("/")

    if len(ranks) != 8:
        return False

    for rank in ranks:

        count = 0

        for char in rank:

            if char.isdigit():

                count += int(char)

            elif char in "KQRBNPkqrbnp":

                count += 1

            else:

                return False

        if count != 8:
            return False

    if parts[1] not in ["w", "b"]:
        return False

    return True


def open_lichess(fen):

    lichess_fen = fen.replace(" ", "_")

    url = f"https://lichess.org/editor/{lichess_fen}"

    print("\n================================")
    print("OPENING LICHESS")
    print("================================")

    print(url)

    webbrowser.open(url)


def process_position():

    print("\nSelect the chessboard with your mouse.")

    take_screenshot()

    print("\nAnalyzing with Gemma 4...")

    content = recognize_board()

    print("\n========== GEMMA OUTPUT ==========\n")
    print(content)

    board, turn = parse_board(content)

    if board is None:
        return

    fen = generate_fen(board, turn)

    if fen is None:
        return

    print("\n================================")
    print("FEN")
    print("================================")

    print(fen)

    valid = validate_fen(fen)

    print("\n================================")
    print("VALID FEN")
    print("================================")

    print(valid)

    if valid:
        open_lichess(fen)


print("\n================================")
print("CHESS SCREENSHOT → FEN")
print("================================")

print("Press F8 to capture a chessboard.")
print("Press CTRL+C in the terminal to quit.")

while True:

    wait_for_hotkey()

    process_position()