#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mcp-qimen — 기문둔갑(奇門遁甲) MCP 서버 (stdio).

get_qimen: 점단 일시 → 9궁 포국(팔문·구성·팔신·천반/지반) 텍스트 + 9궁 PNG.
"""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from mcp.server.fastmcp import FastMCP, Image

from qimen_core import divine, format_text, render_png

mcp = FastMCP("qimen")


@mcp.tool()
def get_qimen(datetime_str: str, method: Literal["chaibu", "zhirun"] = "chaibu") -> list:
    """기문둔갑 포국을 세운다 (時家奇門).

    Args:
        datetime_str: 점단 일시 "YYYY-MM-DD HH:MM".
        method: 포국 방식 — chaibu(拆補, 기본) / zhirun(置閏).

    Returns:
        구조화 텍스트(9궁 포국: 神·星·門·天盤/地盤, 排局/節氣/値符値使/旬空)와 9궁 PNG.
    """
    try:
        dt = datetime.strptime(datetime_str.strip(), "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError(f"일시 형식 오류 (YYYY-MM-DD HH:MM): {datetime_str}")

    result = divine(dt.year, dt.month, dt.day, dt.hour, dt.minute, method)
    text = format_text(result)
    png = render_png(result)
    return [text, Image(data=png, format="png")]


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
