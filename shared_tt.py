"""Lock-free shared-memory transposition table for Lazy SMP.

Each slot is 16 bytes: two little-endian ``uint64`` words

    word0 = key XOR data
    word1 = data

Readers recover ``key' = word0 XOR word1`` and accept the entry only when it
equals the probe key. A torn write (the two words briefly out of sync across
processes) fails that check and is treated as a miss, so no lock is needed
(Hyatt's XOR trick). ``data`` packs the move, score, depth and bound flag.
"""
import struct
from multiprocessing import shared_memory

import chess

from transposition import TT_EXACT, TT_LOWER, TT_UPPER, MATE_GUARD

ENTRY_SIZE = 16
_ENTRY = struct.Struct("<QQ")
_U64 = (1 << 64) - 1


def _pack_move(move):
    if move is None:
        return 0
    return move.from_square | (move.to_square << 6) | ((move.promotion or 0) << 12)


def _unpack_move(value):
    value &= 0xFFFF
    if value == 0:
        return None
    promo = (value >> 12) & 7
    return chess.Move(value & 63, (value >> 6) & 63, promo or None)


def _pack_data(move, score, depth, flag):
    depth = 0 if depth < 0 else (255 if depth > 255 else int(depth))
    return ((_pack_move(move) & 0xFFFF)
            | ((score & 0xFFFF) << 16)
            | (depth << 32)
            | ((flag & 0xFF) << 40))


def _unpack_data(data):
    move = _unpack_move(data)
    raw = (data >> 16) & 0xFFFF
    score = raw - 0x10000 if raw >= 0x8000 else raw
    return move, score, (data >> 32) & 0xFF, (data >> 40) & 0xFF


class SharedTT:
    def __init__(self, slots=1 << 20, name=None, create=True):
        assert slots & (slots - 1) == 0, "slots must be a power of two"
        self.slots = slots
        self.mask = slots - 1
        if create:
            self.shm = shared_memory.SharedMemory(create=True, size=slots * ENTRY_SIZE)
        else:
            self.shm = shared_memory.SharedMemory(name=name)
        self.name = self.shm.name

    def probe(self, key, depth, alpha, beta):
        off = (key & self.mask) * ENTRY_SIZE
        word0, data = _ENTRY.unpack_from(self.shm.buf, off)
        if data == 0 or (word0 ^ data) != key:
            return False, 0, None
        move, score, e_depth, flag = _unpack_data(data)
        if e_depth >= depth and abs(score) < MATE_GUARD:
            if flag == TT_EXACT:
                return True, score, move
            if flag == TT_LOWER and score >= beta:
                return True, score, move
            if flag == TT_UPPER and score <= alpha:
                return True, score, move
        return False, 0, move

    def store(self, key, depth, score, flag, move):
        off = (key & self.mask) * ENTRY_SIZE
        word0, old = _ENTRY.unpack_from(self.shm.buf, off)
        if old and (word0 ^ old) == key and _unpack_data(old)[2] > depth:
            return  # keep the deeper entry for this position
        data = _pack_data(move, score, depth, flag)
        _ENTRY.pack_into(self.shm.buf, off, (key ^ data) & _U64, data)

    def close(self):
        try:
            self.shm.close()
        except Exception:
            pass

    def unlink(self):
        try:
            self.shm.unlink()
        except Exception:
            pass


class SharedFlag:
    """One shared byte used as a cross-process stop signal."""

    def __init__(self, name=None, create=True):
        if create:
            self.shm = shared_memory.SharedMemory(create=True, size=1)
            self.shm.buf[0] = 0
        else:
            self.shm = shared_memory.SharedMemory(name=name)
        self.name = self.shm.name

    def set(self):
        self.shm.buf[0] = 1

    def is_set(self):
        return self.shm.buf[0] != 0

    def close(self):
        try:
            self.shm.close()
        except Exception:
            pass

    def unlink(self):
        try:
            self.shm.unlink()
        except Exception:
            pass
