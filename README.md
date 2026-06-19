# mcp-qimen

점단 일시를 받아 **기문둔갑(奇門遁甲)** 9궁 포국(팔문·구성·팔신·천반/지반)을 세워
구조화 텍스트와 **9궁 PNG**를 반환하는 MCP 서버. (Python 런타임)

> 구조·네이밍·PNG·설치 규약은 [`STANDARD.md`](STANDARD.md)를 따른다(§6 Python 블록).
> mcp-liuren과 동일한 Python 패턴.

---

## 구성 / 계산

- **포국 엔진**: [`kinqimen`](https://pypi.org/project/kinqimen/) — 時家奇門, 일시를 직접 받아 포국(달력 변환 레이어 불필요).
- **천체력 의존**: `sxtwl`, `ephem` (절기/간지 계산용 — kinqimen 내부 사용).
- **렌더**: [`Pillow`](https://pypi.org/project/pillow/) — 洛書 3×3 9궁, 한자/한글 폰트.
- 결정론적: 같은 입력 → 같은 포국.

> **局(국) 신뢰성**: 예제(`2024-02-10 14:30`, 立春)의 排局 = **陽遁二局下元**.
> 立春 三元局數(陽 8·5·2, 上·中·下元) 표준표에서 下元 = 陽2局과 일치한다.

---

## 도구

### `get_qimen`

| 파라미터 | 타입 | 필수 | 기본 | 설명 |
|---|---|---|---|---|
| `datetime_str` | string `YYYY-MM-DD HH:MM` | ✅ | — | 점단 일시 |
| `method` | `chaibu` \| `zhirun` | | `chaibu` | 拆補(1) / 置閏(2) |

**출력 (둘 다 반환)**:
1. 구조화 텍스트 — 9궁(神·星·門·天盤/地盤), 排局·節氣·値符値使·旬空·馬星
2. 9궁 PNG (1080×1176, 洛書 배치 · 値符/値使 궁 강조)

예제 출력: [`examples/qimen_example.png`](examples/qimen_example.png) (`2024-02-10 14:30`, 拆補).

---

## 설치 (Python 3.10/3.11)

> ⚠️ `sxtwl`/`ephem`은 바이너리 휠이 필요하다. **Windows에서는 Python 3.10 또는 3.11**을 쓴다
> (3.12+는 sxtwl 휠 부재 → 빌드 실패). Linux는 3.12도 manylinux 휠로 가능.

```bash
git clone https://github.com/molpass/mcp-qimen.git
cd mcp-qimen
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install --no-deps kinqimen==0.0.6.6
```

> 두 번째 줄(`--no-deps`)이 필요한 이유: kinqimen이 `sxtwl==2.0.6`/`ephem==4.1.3`(휠 없음)을
> 핀하므로, 휠이 있는 상위 버전(requirements.txt)을 먼저 깔고 kinqimen은 의존성 없이 설치한다.

예제 9궁을 직접 생성해 보려면:

```bash
python examples/generate-example.py   # examples/qimen_example.png 재생성
```

> **폰트**: 한자·한글 라벨을 위해 한글 가능 폰트가 필요하다.
> Windows는 Malgun Gothic 기본 탑재. Linux는 Noto CJK / Nanum 권장.

---

## MCP 등록 (서버명 `qimen`, STANDARD §6 Python)

```json
{
  "mcpServers": {
    "qimen": {
      "command": "/abs/path/mcp-qimen/.venv/bin/python",
      "args": ["/abs/path/mcp-qimen/server.py"]
    }
  }
}
```

> Windows 예: `"command": "C:/Users/<you>/mcp-qimen/.venv/Scripts/python.exe"`,
> `"args": ["C:/Users/<you>/mcp-qimen/server.py"]`

---

## 스킬

페어링 스킬: [`skill/qimen.skill.md`](skill/qimen.skill.md).

## License

MIT
