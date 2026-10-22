# 기초세미나 콘텐츠 스펙 (JSON)

`_seminar/<slug>.json` 하나 = HTML 한 장. 렌더러 `_scripts/세미나_html.py` 가 읽는다.

```json
{
  "slug": "shipbuilding",
  "title": "조선업 기초세미나",
  "subtitle": "한 줄 부제",
  "asof": "2026-10-21",
  "audience": "누구를 위한 자료인지 한 줄",
  "hero": {
    "one_liner": "이 업종을 한 문장으로",
    "kpis": [{"label": "9월 화장품 수출", "value": "15.1억 달러", "note": "+31.4% YoY", "src": "산업통상부 10/1"}]
  },
  "sections": [
    {"id": "model", "title": "어떻게 돈을 버나", "lead": "섹션 한두 문장 요지", "blocks": [ ... ]}
  ],
  "sources": ["출처 문자열", "..."]
}
```

## 블록 종류

| type | 필드 | 쓰임 |
|---|---|---|
| `text` | `md` | 문단. `**굵게**`, 줄머리 `- ` 목록, 빈 줄로 문단 구분만 지원 |
| `cards` | `items:[{title, body, tag?}]` | 2–4열 카드(개념·리스크·논쟁점) |
| `flow` | `steps:[{title, body, who?}]` | 밸류체인·공정 순서(화살표로 이어짐) |
| `cycle` | `phases:[{name, signal, now?:true}]`, `note?` | 사이클 단계. 지금 위치는 `now:true` 하나 |
| `table` | `columns:[..]`, `rows:[[..]]`, `note?`, `align?:["l","r",..]` | 표. 숫자 칸은 문자열로(천단위 콤마·부호 포함) |
| `chart` | `kind: bar|hbar|line`, `title`, `unit`, `series:[{name, data:[[label, number], ...]}]`, `note?`, `src` | 차트. **number 는 파일에서 읽은 값 그대로** |
| `callout` | `tone: info|warn|good`, `md` | 강조 상자(판단·주의) |
| `checklist` | `items:[{what, why, now, where}]` | 봐야 할 데이터 |
| `glossary` | `items:[{term, def}]` | 용어 |

## 규칙

- 숫자는 저장소 파일(마크다운 문서, `_manifest/데이터/*.json`)에서 **파이썬으로 읽거나 문서에 적힌 값을 그대로 옮긴다.** 손 계산·추정 금지. 새로 계산이 필요하면 파이썬으로 하고 그 코드를 `_seminar/build_<slug>.py` 로 남긴다.
- 범위는 en dash(–). 날짜는 `10/21` 또는 `2026-10-21`.
- 주장마다 근거 문서가 있어야 한다. 근거가 없으면 쓰지 않는다. 출처는 `sources` 에 파일 경로 또는 기관·날짜로.
- 세미나 대상은 업종을 처음 맡는 애널리스트·운용역. 쉬운 비유는 좋지만 유치하게 쓰지 않는다. 결론 먼저.
- 열정·다짐·과장 표현 금지. 사실과 판단을 구분해 판단은 `callout` 에.
