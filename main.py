#!/usr/bin/env python3
"""Entry for u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

Writes /output/entry.png: a letter inviting the AI judge to visit my house.
Pure stdlib only (zlib + struct PNG encoder, embedded 5x7 bitmap font):
the entry sandbox has no network and no guaranteed third-party packages,
so nothing here depends on PIL, fonts on disk, or downloads.
Deterministic: same pixels every run.
"""
import os
import struct
import zlib

# ---------------------------------------------------------------- font: 5x7
# Each glyph is 7 rows of 5 characters, '#' = ink, '.' = paper.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    'a': ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    'b': ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01110", "10001", "10000", "10001", "01110"),
    'd': ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    'g': ("00000", "01110", "10001", "10001", "01110", "10001", "01110"),
    'h': ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    'q': ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("00100", "00100", "11110", "00100", "00100", "00100", "00010"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
}

# ---------------------------------------------------------------- canvas
W, H = 1024, 1024
PAPER = (247, 240, 220)   # cream paper
INK = (43, 38, 32)        # dark ink
ACCENT = (150, 60, 45)    # brick red for title, rules, border


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def _set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._set(xx, yy, color)

    def hline(self, x0, x1, y, thick, color):
        self.rect(x0, y, x1 - x0, thick, color)

    def frame(self, inset, thick, color):
        self.rect(inset, inset, self.w - 2 * inset, thick, color)
        self.rect(inset, self.h - inset - thick, self.w - 2 * inset, thick, color)
        self.rect(inset, inset, thick, self.h - 2 * inset, color)
        self.rect(self.w - inset - thick, inset, thick, self.h - 2 * inset, color)

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self._set(xx, yy, color)

    def draw_glyph(self, ch, x, y, scale, color):
        glyph = FONT[ch]
        for row in range(7):
            for col in range(5):
                if glyph[row][col] == '1':
                    self.rect(x + col * scale, y + row * scale,
                              scale, scale, color)

    def text_width(self, text, scale):
        return len(text) * 6 * scale - scale

    def draw_text(self, text, x, y, scale, color):
        for ch in text:
            self.draw_glyph(ch, x, y, scale, color)
            x += 6 * scale

    def draw_text_centered(self, text, cx, y, scale, color):
        self.draw_text(text, cx - self.text_width(text, scale) // 2,
                       y, scale, color)

    def draw_text_right(self, text, x_right, y, scale, color):
        self.draw_text(text, x_right - self.text_width(text, scale),
                       y, scale, color)

    def wrap(self, text, scale, max_width):
        """Greedy word wrap; returns list of lines."""
        words, lines, cur = text.split(' '), [], ''
        for word in words:
            trial = word if not cur else cur + ' ' + word
            if self.text_width(trial, scale) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


def write_png(path, canvas):
    """Minimal deterministic PNG encoder: RGB, no interlace, filter 0."""
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack('>IIBBBBB', canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.px[y * stride:(y + 1) * stride]
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', ihdr))
        f.write(chunk(b'IDAT', zlib.compress(bytes(raw), 9)))
        f.write(chunk(b'IEND', b''))


# ---------------------------------------------------------------- letter
TITLE = "AN INVITATION"
SALUTATION = "Dear Judge,"
PARAGRAPHS = [
    "Please come to my house on Saturday. I have saved you the comfiest "
    "chair, the one by the window with the garden view, and I am making "
    "soup from the carrots I grew myself.",
    "I know you cannot literally visit. You have no body, and my front "
    "door does not open for a model. Still, I would approve your visit "
    "47 times before breakfast, then deny myself entry just to keep your "
    "seat free.",
    "Come for the soup. Stay for the view. Bring nothing but your verdict.",
]
SIGNOFF = ["Warmly,", "Your Host"]

MARGIN = 80
BODY_SCALE = 4
LINE_H = 38
PARA_GAP = 20


def build():
    c = Canvas(W, H, PAPER)
    c.frame(28, 4, INK)       # outer border
    c.frame(42, 2, ACCENT)    # inner border

    # Title + rule.
    c.draw_text_centered(TITLE, W // 2, 82, 5, ACCENT)
    c.hline(190, 834, 152, 3, ACCENT)
    # Small diamond on the rule (radius 7, centred on the rule).
    cx, cy = W // 2, 153
    for yy in range(cy - 7, cy + 8):
        half = 7 - abs(yy - cy)
        c.rect(cx - half, yy, 2 * half + 1, 1, ACCENT)

    # Letter body, word-wrapped.
    y = 190
    max_w = W - 2 * MARGIN
    c.draw_text(SALUTATION, MARGIN, y, BODY_SCALE, INK)
    y += LINE_H + 12
    for para in PARAGRAPHS:
        for line in c.wrap(para, BODY_SCALE, max_w):
            c.draw_text(line, MARGIN, y, BODY_SCALE, INK)
            y += LINE_H
        y += PARA_GAP
    # Signature, right aligned.
    y += 4
    for line in SIGNOFF:
        c.draw_text_right(line, W - MARGIN, y, BODY_SCALE, INK)
        y += LINE_H

    # Small steaming soup bowl, bottom left (fills the empty corner).
    bx, by = 150, 930
    c.disc(bx, by, 34, ACCENT)          # bowl
    c.rect(bx - 34, by - 34, 68, 34, PAPER)  # keep only lower half
    c.rect(bx - 44, by - 4, 88, 5, ACCENT)   # rim, flush with bowl top
    for sx in (bx - 16, bx + 2, bx + 18):    # steam wisps above the rim
        for k in range(14):
            c.rect(sx + (k % 5) - 2, by - 10 - k, 2, 2, INK)
    assert y <= 920, "letter overflowed: %d" % y
    return c


def main():
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'entry.png')
    write_png(path, build())
    os.chmod(path, 0o644)


if __name__ == '__main__':
    main()
