# -*- coding: utf-8 -*-
"""예제 9궁 포국 생성 (고정 일시 → 결정론적 재현).
실행(repo 루트): ./.venv/Scripts/python.exe examples/generate-example.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from qimen_core import divine, format_text, render_png

# 샘플: 2024-02-10 14:30 (立春, 甲辰日辛未時) — 拆補
result = divine(2024, 2, 10, 14, 30, "chaibu")
print(format_text(result))

png = render_png(result)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qimen_example.png")
with open(out, "wb") as f:
    f.write(png)
print(f"\nwrote {out} ({len(png)} bytes)")
