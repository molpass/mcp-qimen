# MCP 표준 아키텍처 v1

> 모든 개별 MCP repo가 따르는 공통 계약. 각 발주서는 이 문서를 "사전 인지 자료"로 참조한다.
> 목표: **심플 · 빠름 · 복제 가능**. 1개를 잘 만들고 나머지는 복사해서 채운다.

---

## 0. 사전 인지

- 본 문서 (`STANDARD.md`)
- 설치된 스킬 컨벤션 2종:
  - https://github.com/multica-ai/andrej-karpathy-skills
  - https://github.com/obra/superpowers
- 스킬 MD 작성 시 위 두 repo의 작성 규칙·구조를 상속한다.

---

## 1. 핵심 원칙

```
1 MCP = 1 GitHub 퍼블릭 repo = 1 발주서 = 1 스킬 MD
```

- **각 repo는 완전 독립**. 모노레포·공유 패키지 없음. 누구나 필요한 것만 골라 설치.
- "템플릿"은 공유 의존성이 아니라 **복사용 레퍼런스 repo**(= `mcp-qr`).
- 라이선스: 전부 **MIT**.

---

## 2. 런타임 표준

| 구분 | 런타임 | 대상 MCP |
|---|---|---|
| 기본 | **Node 20+ / TypeScript** | qr, biorhythm, astrology, ziwei, numerology, newsfeed |
| 예외 | **Python 3.10+** | liuren, qimen, taiyi (삼식 — kentang2017 계열) |

- SDK: 공식 MCP SDK (`@modelcontextprotocol/sdk` / Python `mcp`).
- 전송: stdio.

---

## 3. repo 네이밍 & 구조

네이밍: `mcp-<name>`

표준 구조 (Node 기준):
```
mcp-<name>/
├─ src/
│  └─ index.ts          # MCP 서버 엔트리
├─ skill/
│  └─ <name>.skill.md   # 페어링 스킬 (도구 호출·해석)
├─ examples/            # 예제 입력/출력(PNG 포함)
├─ package.json
├─ tsconfig.json
├─ README.md            # 설치 블록 + 사용법
└─ LICENSE              # MIT
```
Python(삼식)은 `src/` 대신 `server.py`, `pyproject.toml`, `requirements.txt`로 대체.

---

## 4. 도구(tool) 규약

- input schema를 명확히 정의(JSON Schema). 필수/선택 구분.
- 순수 계산형 MCP는 **결정론적**(같은 입력 → 같은 출력, 외부 의존 없음).
- 출력은 항상 두 가지를 함께:
  1. **구조화 텍스트** (해석·후속 처리에 쓸 수 있는 데이터)
  2. **PNG image 콘텐츠** (시각화가 있는 경우)

---

## 5. 차트 출력 규약 (PNG 통일)

- 모든 시각화는 **PNG(base64 image content)** 로 반환. (텔레그램/Hermes 호환)
- SVG 기반 라이브러리는 **서버에서 SVG→PNG 변환**(`sharp` 등).
- 표준 캔버스: 가로 **1080px** 기준, 여백 **48px**, 배경 흰색(투명 옵션 가능).
  폰트는 한글 포함(예: Noto Sans KR / Malgun Gothic 계열).

---

## 6. Hermes 설치 규약

README 하단에 **복붙용 설치 블록**을 반드시 포함.

Node MCP:
```bash
git clone https://github.com/<org>/mcp-<name>.git
cd mcp-<name>
npm install && npm run build
```
```json
{
  "mcpServers": {
    "<name>": { "command": "node", "args": ["/abs/path/mcp-<name>/dist/index.js"] }
  }
}
```

---

## 7. 스킬 페어링 규약

- 각 repo의 `skill/<name>.skill.md` 는 해당 MCP 도구를 **호출하고 결과를 해석**하는 스킬.
- karpathy/superpowers 스킬 작성 규칙 상속.
- 도구(계산·시각화)와 스킬(해석)을 분리: 도구는 "사실", 스킬은 "의미".

---

## 8. 라이브 데이터 / 시크릿 (newsfeed 전용)

- 순수 계산 MCP는 시크릿 없음.
- newsfeed만 `.env` + Hermes secret으로 API 키 관리.
- **저작권**: 기사 본문 전체 금지. 헤드라인 + 짧은 요약 + 원문 링크만.

---

## 9. 공통 완료조건 (Definition of Done)

- [ ] 빌드 통과 (`npm run build` / Python import)
- [ ] 예제 입력으로 도구 1회 정상 응답 (PNG 있으면 PNG 포함)
- [ ] README 설치 블록으로 **클린 환경에서 설치 재현** 확인
- [ ] `skill/<name>.skill.md` 1개 포함
- [ ] GitHub 퍼블릭 공개 + repo URL 보고
