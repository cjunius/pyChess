"""Regenerate ``docs/self-play.gif``: the engine playing itself, one frame per
move, over an ASCII board.

    python tools/self_play_gif.py [--seconds 5] [--moves 30] [--out docs/self-play.gif]

Every move is a real Lazy SMP search - no opening book. At the default 5 s/move
and 30-move cap this takes ~5 minutes.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import chess
from PIL import Image, ImageDraw, ImageFont

from pychess.constants import MATE, MATE_IN_MAX
from pychess.engine import Engine

WIDTH, HEIGHT = 566, 514
BG = (22, 22, 22)
FG = (230, 230, 230)
DIM = (138, 138, 138)
MARGIN_X = 29
TOP_Y = 32
LINE_H = 40
BOARD_TOP = 121
FRAME_MS = 1100

_FONT_CANDIDATES = (
    "/System/Library/Fonts/SFNSMono.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/Library/Fonts/DejaVuSansMono.ttf",
)


def _font(size: int) -> ImageFont.FreeTypeFont:
    for path in _FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


FONT = _font(25)

_PIECE_CP = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}


def _board_lines(board: chess.Board) -> list[str]:
    lines = []
    for rank in range(7, -1, -1):
        cells = []
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank))
            cells.append(piece.symbol() if piece else ".")
        lines.append(f"{rank + 1}  " + " ".join(cells))
    lines.append("   " + " ".join("abcdefgh"))
    return lines


def _score_text(white_cp: int) -> str:
    """A White-relative score for the info line: ``#N`` near mate, else ``cp``."""
    if abs(white_cp) >= MATE_IN_MAX:
        moves = (MATE - abs(white_cp) + 1) // 2
        return f"#{moves}" if white_cp > 0 else f"#-{moves}"
    return f"{white_cp:+d} cp"


def _material_note(board: chess.Board) -> str:
    diff = sum(
        _PIECE_CP[pt] * (len(board.pieces(pt, chess.WHITE)) - len(board.pieces(pt, chess.BLACK)))
        for pt in _PIECE_CP
    )
    mag = abs(diff)
    if mag < 2:
        return ""
    if mag == 2:
        return ", up two pawns"
    if mag < 5:
        return ", up a piece"
    if mag < 8:
        return ", up a rook"
    return ", up a queen"


def _render(title: str, subtitle: str, board: chess.Board) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.text((MARGIN_X, TOP_Y), title, font=FONT, fill=FG)
    draw.text((MARGIN_X, TOP_Y + LINE_H), subtitle, font=FONT, fill=DIM)
    for i, line in enumerate(_board_lines(board)):
        draw.text((MARGIN_X, BOARD_TOP + i * LINE_H), line, font=FONT, fill=FG)
    return img


def _summary(board: chess.Board, white_cp: int, moves_cap: int, capped: bool) -> tuple[str, str]:
    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        return f"{winner} wins by checkmate", "game over"
    if board.is_game_over() or board.is_repetition(3) or board.halfmove_clock >= 100:
        return "Draw", "game over"

    note = _material_note(board)
    if white_cp > 150:
        verdict = f"White is winning ({white_cp / 100:+.1f}{note})"
    elif white_cp < -150:
        verdict = f"Black is winning ({white_cp / 100:+.1f}{note})"
    else:
        verdict = f"Roughly balanced ({white_cp / 100:+.1f})"
    tail = f"game stopped at the {moves_cap}-move cap" if capped else "game over"
    return verdict, tail


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=5.0)
    parser.add_argument("--moves", type=int, default=30, help="full-move cap")
    parser.add_argument("--out", type=Path, default=Path("docs/self-play.gif"))
    args = parser.parse_args()

    engine = Engine()
    board = chess.Board()
    frames = [_render("pychess self-play", f"{args.seconds:g} second time limit per move", board)]

    white_cp = 0
    plies = args.moves * 2
    for _ply in range(plies):
        result = engine.search(board, {"movetime": int(args.seconds * 1000)})
        if not result.pv:
            break
        move = result.pv[0]
        move_no = board.fullmove_number
        san = board.san(move)
        moved_white = board.turn == chess.WHITE
        prefix = f"{move_no}." if moved_white else f"{move_no}..."
        board.push(move)
        white_cp = result.score if moved_white else -result.score
        info = (
            f"depth {result.depth}   {_score_text(white_cp)}   "
            f"{result.nodes:,} nodes   {result.elapsed:.1f}s"
        )
        frames.append(_render(f"{prefix} {san}", info, board))
        print(f"{prefix} {san}  ({info})", flush=True)
        if board.is_game_over() or board.is_repetition(3) or board.halfmove_clock >= 100:
            break

    capped = len(frames) - 1 >= plies
    title, subtitle = _summary(board, white_cp, args.moves, capped)
    frames.append(_render(title, subtitle, board))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        args.out,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
    )
    print(f"\nwrote {args.out} ({args.out.stat().st_size // 1024} KB, {len(frames)} frames)")


if __name__ == "__main__":
    main()
