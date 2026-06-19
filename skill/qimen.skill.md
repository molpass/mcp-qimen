---
name: qimen
description: Use when the user wants a Qi Men Dun Jia (기문둔갑/奇門遁甲) reading — "기문둔갑 봐줘", "기문으로 포국 세워줘", "지금 시각 기문국". Calls get_qimen with the divination time, returns the 9-palace plate PNG with a short reading.
---

# qimen

`mcp-qimen` 서버의 `get_qimen` 도구를 호출해 기문둔갑 9궁 포국(팔문·구성·팔신·천반/지반)과
9궁 PNG를 만든다. 도구는 "사실"(포국·렌더), 이 스킬은 "의미"(시각 확보 + 짧은 해석)를 담당한다.

## 트리거

- "기문둔갑 봐줘", "기문으로 봐줘"
- "지금 시각으로 포국 세워줘", "오늘 OO시 기문국"
- 특정 일시의 기문 9궁/팔문을 보려는 요청

## 동작

1. **점단 일시**를 확보한다.
   - "지금"이면 현재 일시를 `YYYY-MM-DD HH:MM`로 만들어 넣는다.
   - 특정 일시를 말하면 그 값을 쓴다. 분 단위가 모호하면 한 번 확인한다.
2. 필요 시 `method`를 정한다(기본 `chaibu` 拆補, 또는 `zhirun` 置閏).
3. `get_qimen` 을 호출한다.
4. 반환된 **9궁 PNG**를 보여주고, 핵심을 요약한다:
   - **排局(국)**, **値符·値使**(궁), 그리고 길문(開·休·生)이 어느 궁에 있는지 짚어준다.
   - 用神/방위 질문이면 해당 궁의 神·星·門·干 조합을 한두 줄로.

## 파라미터 요약

`datetime_str`("YYYY-MM-DD HH:MM", 필수), `method`(chaibu/zhirun, 기본 chaibu).

## 주의

- 시각이 핵심이다 — 時干支가 바뀌면 포국 전체가 달라진다. 모르면 사용자에게 확인한다.
- 절기·자시 경계 부근은 局이 민감하니 가능하면 정확한 분까지 받는다.
- 기문둔갑은 전통 술수 체계다. 해석은 재미/참고용으로 단정적이지 않게 전달한다.
