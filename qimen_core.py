# -*- coding: utf-8 -*-
"""기문둔갑(奇門遁甲) 핵심 로직: kinqimen 포국 + 텍스트/PNG(9궁) 렌더.

kinqimen은 일시를 직접 받으므로 별도 달력 변환 레이어가 필요 없다(時家奇門).
kinqimen 내부가 'import config'(절대 임포트)를 쓰는 패키징 버그가 있어,
패키지 디렉터리를 sys.path에 추가해 해결한다.
"""
from __future__ import annotations

import io
import os
import sys

import kinqimen as _pkg

# kinqimen.kinqimen 의 'import config' 해결: 패키지 디렉터리를 sys.path에 추가
sys.path.insert(0, os.path.dirname(_pkg.__file__))
from kinqimen import kinqimen  # noqa: E402

from PIL import Image as PILImage, ImageDraw, ImageFont  # noqa: E402

_METHOD = {"chaibu": 1, "zhirun": 2}  # 拆補 / 置閏

# 洛書 9궁 배치 (離=남쪽 위). (row, col)
_PALACE_CELL = {
    "巽": (0, 0), "離": (0, 1), "坤": (0, 2),
    "震": (1, 0), "中": (1, 1), "兌": (1, 2),
    "艮": (2, 0), "坎": (2, 1), "乾": (2, 2),
}
_PALACE_DIR = {
    "巽": "東南", "離": "南", "坤": "西南",
    "震": "東", "中": "中", "兌": "西",
    "艮": "東北", "坎": "北", "乾": "西北",
}


def _fmt_horse(ma) -> str:
    """馬星(dict 또는 문자열)을 보기 좋게."""
    if isinstance(ma, dict):
        return " ".join(f"{k}{v}" for k, v in ma.items())
    return str(ma) if ma else "-"


def divine(year: int, month: int, day: int, hour: int, minute: int, method: str = "chaibu") -> dict:
    mode = _METHOD.get(method)
    if mode is None:
        raise ValueError(f"method는 chaibu/zhirun 중 하나 (받음: {method})")
    r = kinqimen.Qimen(year, month, day, hour, minute).pan(mode)
    r["_input"] = {"datetime": f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}", "method": method}
    return r


def _palace_lines(r: dict, p: str) -> list[str]:
    """한 궁의 神/星/門/天盤/地盤."""
    sky = r.get("天盤", {}).get(p)
    earth = r.get("地盤", {}).get(p)
    door = r.get("門", {}).get(p)
    star = r.get("星", {}).get(p)
    god = r.get("神", {}).get(p)
    return [god, star, door, sky, earth]


def format_text(r: dict) -> str:
    inp = r.get("_input", {})
    zf = r.get("值符值使", {})
    xk = r.get("旬空", {})
    lines = [
        "기문둔갑(奇門遁甲) 포국",
        f"일시: {inp.get('datetime')}  |  排盤 {r.get('排盤方式')}",
        f"干支: {r.get('干支')}",
        f"排局: {r.get('排局')}   節氣: {r.get('節氣')}   局日: {r.get('局日')}",
        f"旬首: {r.get('旬首')}   旬空: 日空 {xk.get('日空','-')} / 時空 {xk.get('時空','-')}   馬星: {_fmt_horse(r.get('馬星'))}",
        f"值符: {'/'.join(map(str, zf.get('值符星宮', [])))}   值使: {'/'.join(map(str, zf.get('值使門宮', [])))}",
        "",
        "[9궁 포국]  (神 · 星 · 門 · 天盤/地盤)",
    ]
    order = ["巽", "離", "坤", "震", "中", "兌", "艮", "坎", "乾"]
    for p in order:
        god, star, door, sky, earth = _palace_lines(r, p)
        if p == "中":
            lines.append(f"  {p}({_PALACE_DIR[p]}): 地盤 {earth}")
        else:
            lines.append(
                f"  {p}({_PALACE_DIR[p]}): 神 {god or '-'} · 星 {star or '-'} · 門 {door or '-'} · 天 {sky or '-'}/地 {earth or '-'}"
            )
    return "\n".join(lines)


# ---- PNG 렌더 ----
# repo 동봉 폰트를 명시적으로 로드(시스템 폰트 비의존, 기본 폰트 금지).
_FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "NotoSansCJK-Regular.otf")


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(_FONT_PATH, size)


_W = 1080
_HEADER = 132
_CELL = 316
_GRID = _CELL * 3            # 948
_PADX = (_W - _GRID) // 2    # 66
_FOOTER = 96
_H = _HEADER + _GRID + _FOOTER


def render_png(r: dict) -> bytes:
    img = PILImage.new("RGB", (_W, _H), "white")
    d = ImageDraw.Draw(img)
    f_title = _font(34)
    f_meta = _font(20)
    f_dir = _font(20)
    f_god = _font(26)
    f_star = _font(26)
    f_door = _font(30)
    f_gan = _font(40)

    # 헤더
    inp = r.get("_input", {})
    d.text((_PADX, 18), "奇門遁甲 기문둔갑", font=f_title, fill="#222222")
    d.text((_PADX, 64), f"{inp.get('datetime')}  ·  {r.get('干支')}", font=f_meta, fill="#555555")
    d.text((_PADX, 94), f"{r.get('排局')}  ·  節氣 {r.get('節氣')}  ·  排盤 {r.get('排盤方式')}", font=f_meta, fill="#b8460e")

    zf = r.get("值符值使", {})
    zhifu_p = (zf.get("值符星宮") or ["", ""])[1]
    zhishi_p = (zf.get("值使門宮") or ["", ""])[1]

    # 9궁
    for p, (row, col) in _PALACE_CELL.items():
        x = _PADX + col * _CELL
        y = _HEADER + row * _CELL
        # 값부/값사 궁 강조
        if p == zhishi_p:
            d.rectangle([x + 1, y + 1, x + _CELL - 1, y + _CELL - 1], fill="#fdf2e9")
        elif p == zhifu_p:
            d.rectangle([x + 1, y + 1, x + _CELL - 1, y + _CELL - 1], fill="#eaf3fb")
        d.rectangle([x, y, x + _CELL, y + _CELL], outline="#b0b0b0", width=2)

        # 방위 + 궁이름 (좌하단)
        d.text((x + 10, y + _CELL - 28), f"{p} {_PALACE_DIR[p]}", font=f_dir, fill="#999999")

        if p == "中":
            d.text((x + _CELL / 2, y + _CELL / 2 - 30), "中宮", font=f_door, fill="#888888", anchor="mm")
            d.text((x + _CELL / 2, y + _CELL / 2 + 24), f"地 {r.get('地盤',{}).get('中','')}", font=f_gan, fill="#2c3e50", anchor="mm")
            continue

        god, star, door, sky, earth = _palace_lines(r, p)
        # 神(좌상,청) · 星(우상,녹)
        d.text((x + 12, y + 10), god or "", font=f_god, fill="#2471a3")
        d.text((x + _CELL - 12, y + 10), star or "", font=f_star, fill="#1e8449", anchor="ra")
        # 門(중앙,적)
        d.text((x + _CELL / 2, y + _CELL / 2 - 6), door or "", font=f_door, fill="#c0392b", anchor="mm")
        # 天盤干 / 地盤干 (하단: 天 좌, 地 우)
        d.text((x + 16, y + _CELL - 74), sky or "", font=f_gan, fill="#7d3c98")
        d.text((x + _CELL - 16, y + _CELL - 74), earth or "", font=f_gan, fill="#34495e", anchor="ra")

    # 푸터: 값부/값사/순공/마성
    xk = r.get("旬空", {})
    fy = _HEADER + _GRID + 14
    d.text((_PADX, fy), f"値符 {'/'.join(map(str, zf.get('值符星宮', [])))}   値使 {'/'.join(map(str, zf.get('值使門宮', [])))}", font=f_meta, fill="#444444")
    d.text((_PADX, fy + 32), f"旬首 {r.get('旬首')}   旬空 日{xk.get('日空','-')}/時{xk.get('時空','-')}   馬星 {_fmt_horse(r.get('馬星'))}", font=f_meta, fill="#444444")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
