#!/usr/bin/env python3
"""Decoupe la planche ``assets/personnage a mettre dans le décor.png`` en 5 vues pour play.html."""

from pathlib import Path

import numpy as np
from PIL import Image

SOURCE = Path(__file__).resolve().parents[1] / "assets/personnage a mettre dans le décor.png"
OUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "play"


def main():
    im = Image.open(SOURCE).convert("RGBA")
    arr = np.array(im)
    w, _h = arr.shape[1], arr.shape[0]
    rgb = arr[:, :, :3]
    mask = ~((rgb[:, :, 0] < 35) & (rgb[:, :, 1] < 35) & (rgb[:, :, 2] < 35))

    bboxes = []
    for bi in range(5):
        x0 = int(w * bi / 5)
        x1 = int(w * (bi + 1) / 5)
        sub = mask[:, x0:x1]
        rows, cols = np.where(sub)
        xmin = int(cols.min() + x0)
        xmax = int(cols.max() + x0)
        ymin, ymax = int(rows.min()), int(rows.max())
        bboxes.append((xmin, ymin, xmax + 1, ymax + 1))

    max_w = max(b[2] - b[0] for b in bboxes)
    max_h = max(b[3] - b[1] for b in bboxes)
    cell_w = max_w + 8
    cell_h = max_h + 8

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, (xmin, ymin, xmax, ymax) in enumerate(bboxes):
        crop = arr[ymin:ymax, xmin:xmax].copy()
        cr, cg, cb = crop[..., 0], crop[..., 1], crop[..., 2]
        black = (cr < 38) & (cg < 38) & (cb < 38)
        crop[..., 3][black] = 0
        pil = Image.fromarray(crop)
        canvas = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
        ox = (cell_w - pil.width) // 2
        oy = (cell_h - pil.height) // 2
        canvas.paste(pil, (ox, oy), pil)
        out = OUT_DIR / f"plage_tournant_{i}.png"
        canvas.save(out)
        print(out)


if __name__ == "__main__":
    main()
