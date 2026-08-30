# _scripts — 로컬 데이터 수집

클라우드에서는 **Yahoo Finance·네이버 금융·Stooq가 모두 차단**돼 있다. 종목 시세가 필요한
작업은 **로컬(맥북/맥미니)에서 이 스크립트로 받아 커밋**하고, 리포트 작성은 그 파일을
읽어서 클라우드가 한다. (`90_정기발간/수급리뷰_운영메모.md` 의 하이브리드 원칙과 동일)

## 준비 (최초 1회)

```bash
python3 -m venv ~/.venv/krx
~/.venv/krx/bin/pip install pykrx
```

## 종가_수집_로컬.py

KRX 공식 종가를 받아 `_manifest/데이터/<접두어>_<날짜>.{csv,json}` 로 떨어뜨린다.

```bash
# 저장소 문서에서 종목코드를 뽑아 수집 (가장 자주 쓰는 방식)
~/.venv/krx/bin/python _scripts/종가_수집_로컬.py --from-docs 10_국내주식/22_반도체 --out 반도체

# 코드 직접 지정
~/.venv/krx/bin/python _scripts/종가_수집_로컬.py --code 005930 000660 --start 20260101 --out 메모리

# 목록 파일로 (한 줄에 `005930` 또는 `005930,삼성전자`)
~/.venv/krx/bin/python _scripts/종가_수집_로컬.py --codes codes.txt --out 포트폴리오

# PER·PBR·배당까지 (KRX 계정 필요)
KRX_ID=xxx KRX_PW=yyy ~/.venv/krx/bin/python _scripts/종가_수집_로컬.py \
  --from-docs 10_국내주식 --fundamental --out 전체
```

### 옵션

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--from-docs 경로` | — | 문서의 `종목명(123456)` 표기에서 코드 추출. 파일·디렉터리 모두 가능 |
| `--codes 파일` | — | 코드 목록 파일 |
| `--code 코드…` | — | 코드 직접 나열 |
| `--start` / `--end` | `20260101` / 오늘 | 수집 기간 |
| `--out` | `종가` | 출력 파일 접두어 |
| `--delay` | `0.35` | 종목 간 대기 초 |
| `--retries` | `3` | 종목별 재시도 |
| `--fundamental` | 끔 | PER·PBR·EPS·BPS·DIV·DPS. **KRX 로그인 필요** |

### 출력

- **CSV** (UTF-8 BOM, 엑셀에서 한글 안 깨짐): 종목명·코드·최종 종가·기간 고저·**월말 종가**·분할의심
- **JSON**: 위 내용 + 실패 목록 + 수집 시각

### 설계 원칙

- 수치는 KRX 공식 데이터, 계산은 **결정론적 파이썬**. LLM 산술 배제.
- **실패한 종목을 지우지 않는다** — 코드·사유를 그대로 기록한다.
- **액면분할·병합 의심 자동 표시** — 일간 −40% 이하 또는 +60% 이상 구간을 `분할의심` 열에 남긴다.
  수익률을 계산하기 전에 이 열을 반드시 확인할 것.

### 알려진 제약

| 항목 | 상태 |
|---|---|
| 종목별 OHLCV | ✅ 로그인 없이 작동 |
| **일괄 조회**(`get_market_ohlcv(date, market="ALL")`) | ❌ KRX 로그인 필요 |
| **PER·PBR·시가총액** | ❌ KRX 로그인 필요 (`KRX_ID`/`KRX_PW`) |
| 지수 OHLCV | ❌ KRX 로그인 필요 |
| 상장폐지·합병 종목 | 빈 응답 → 실패로 기록 (예: HD현대미포 010620) |

## KRX 자격증명 설정

PER·PBR·시가총액·지수·일괄조회는 KRX 로그인이 필요하다. **자격증명은 이 저장소에 절대 커밋하지 않는다**
(`.gitignore` 처리됨). 실행 호스트에만 둔다.

```bash
mkdir -p ~/.config/krx
printf 'KRX_ID=아이디\nKRX_PW=비밀번호\n' > ~/.config/krx/env
chmod 600 ~/.config/krx/env
```

> 💡 명령 앞에 **공백 한 칸**을 넣으면 셸 히스토리에 안 남는다(zsh `HIST_IGNORE_SPACE` 기준).

스크립트가 아래 순서로 자동 인식한다. **값은 로그에 출력하지 않는다.**

1. 이미 설정된 환경변수 `KRX_ID` / `KRX_PW`
2. `~/.config/krx/env` (권장 — 저장소 밖)
3. `_scripts/krx.env` (`.gitignore` 처리됨. 양식은 [`krx.env.example`](./krx.env.example))

설정 후:

```bash
~/.venv/krx/bin/python _scripts/종가_수집_로컬.py --from-docs 10_국내주식 --fundamental --out 전체
```

## 산출물 이력

- `_manifest/데이터/T1_종가_2026-08-11.{csv,json}` — 밸류에이션 재확인 T1 84종목
- `_manifest/데이터/T1_재계산_결과_2026-08-11.md` — 위 데이터의 분석 요약

## 코스피200_구성종목_수집.py

코스피200 편입 종목을 네이버 금융 '코스피200 편입종목' 목록에서 받는다. KRX 공식 API
(`data.krx.co.kr`)는 이 환경에서 **403** 이고 pykrx 도 같은 이유로 막혀 있다.

```bash
~/.venv/krx/bin/python _scripts/코스피200_구성종목_수집.py
# → _manifest/데이터/코스피200_구성종목_<날짜>.{csv,json}
```

종목코드가 **여섯 자리 숫자라는 가정을 버렸다.** 2026년 상장분에는 `0126Z0`(삼성에피스홀딩스),
`0220W0`(한화머시너리앤서비스홀딩스)처럼 영문이 섞인 단축코드가 있다. `\d{6}` 로 긁으면 조용히
두 종목이 빠진다 — 그중 하나가 기계 업종이었다.

## 네이버_시세컨센_수집.py

종가·시총·후행PER·PBR·컨센EPS(선행PER)·외국인비중·52주 고저를 네이버 종목 API 에서 받는다.

```bash
~/.venv/krx/bin/python _scripts/네이버_시세컨센_수집.py --codes-file /tmp/codes.txt --out 기계
# → _manifest/데이터/기계_시세컨센_<날짜>.{csv,json}
```

**시장(코스피/코스닥)도 같은 페이지에서 받는다.** 원장(`qw_universe`·`consensus`·`stocks`)에는
우선주·리츠·인프라펀드의 시장이 아예 없다 — 유니버스 326종목 중 13종목이 그랬다. 종목
페이지의 배지(`alt="코스피"`)를 같이 긁으면 결측이 0이 된다.

**`lastClosePrice` 는 전일 종가다.** 최종 거래일 종가는 일별 시세(`siseJson.naver`)에서 따로
받아 `trade_date` 와 함께 적는다. 시총·PER 은 최종 거래일 기준이라 그대로 쓰면 종가만 하루
어긋난 표가 나온다.

## 원장_컨센추출_미니.py

**맥미니에서만 돈다.** 원장(`~/research-site/demo/warehouse/research.duckdb`)이 거기 있다.
목표주가·투자의견·리포트 본문·리포트별 추정치(`reports`, `report_estimates`)와 QuantiWise
컨센 추이(`qw_fundamentals`)를 종목 목록에 맞춰 JSON 으로 뽑는다.

```bash
scp _scripts/원장_컨센추출_미니.py mini:/tmp/ && scp codes.txt mini:/tmp/k200_기계.txt
ssh mini 'cd ~/research-site/demo && python3 /tmp/원장_컨센추출_미니.py'
scp mini:/tmp/기계_컨센.json _manifest/데이터/기계_컨센추이_<날짜>.json
```

**증권사마다 리포트 표의 단위가 다르다(억/십억/백만원).** 값마다 따로 맞추면 한 리포트의
매출과 영업이익이 다른 단위로 갈린다. 그래서 리포트 한 건을 단위 하나로 보고, 매출액을
QuantiWise 컨센(억원) 자릿수에 맞춘 `10^k` 를 같은 리포트의 영업이익에 그대로 적용한다.
근거 문장 추출도 파이썬 규칙(업종 어휘 + 숫자 포함)뿐이다 — **모델을 쓰지 않는다.**

## 업종_WI26_배정.py

**업종 축은 WI26 하나다.** 미니 PG `research.sector_map`(QuantiWise WI26, 4,040종목)을
그대로 읽는다. 아카이브가 자체 규칙을 만들지 않는다 — 만들면 화면·원장과 문서가 다른
기준으로 묶인다. 이전 판이 그랬고, 그래서 방산이 기계에, 2차전지가 기계에 앉아 있었다.

```bash
ssh mini '~/.venv-ibbridge/bin/python /tmp/pgsec.py'   # sector_map 스냅샷 → JSON
scp mini:/tmp/sector_map.json _manifest/데이터/업종_WI26_sector_map_<날짜>.json
~/.venv/krx/bin/python _scripts/업종_WI26_배정.py
# → _manifest/데이터/업종_WI26_유니버스_<날짜>.csv
```

배정 순서는 셋이다. ① `sector_source='wi26'` 행은 그 값이 곧 WI26. ② 그 외는 종목의
WICS 산업을 ①행들에서 뽑은 **다수결 표**로 접는다(2,596행에서 유도, 78개 산업 전부
만장일치). ③ 그래도 안 되면 '미분류'.

②가 필요한 이유는 실제로 있다. `sector_map` 의 `naver_mapped` 행은 손으로 쓴 `TO_WICS`
표로 접힌 것이라 QuantiWise 실제 WI26 과 6개 산업에서 어긋난다(전기장비·포장재·가구·
전자제품·가정용기기와용품·양방향미디어와서비스). 그대로 두면 **LG전자는 IT가전,
LG전자우는 IT하드웨어**로 갈라진다.

## 국내주식_코스피200_문서생성.py

위 세 산출물을 읽어 `10_국내주식/` 26개 업종 폴더의 종목표·종목분석·기업분석·기초자료와
전체 색인 `_코스피200_유니버스.md` 를 다시 쓴다. 문서에 손으로 숫자를 적지 않는다.
다시 돌려도 같은 결과가 나온다(멱등 — 원래 손으로 쓴 표는 §2-1·§6-1 로 내려 보존한다).

```bash
~/.venv/krx/bin/python _scripts/국내주식_코스피200_문서생성.py
```

**업종 배정은 새로 만들지 않았다.** 네이버 종목 페이지의 '업종' 이 곧 WICS 산업이고, 이걸
이전 판 300종목의 `업종(WICS)` 과 전부 대조해 **불일치 0** 을 확인한 뒤 이전 판의
WICS→폴더 짝을 그대로 썼다. 코스피200 에만 있던 산업 5개(음료·포장재·가구·복합유틸리티·
핸드셋)만 스크립트 안 `EXTRA` 표에 근거와 함께 손으로 배정했다. 배정이 틀렸다고 보면
그 표만 고치면 된다.

## 순서

```bash
~/.venv/krx/bin/python _scripts/코스피200_구성종목_수집.py
# 유니버스 = 코스피200 ∪ 직전 시총300위. 코드 목록을 만들어
~/.venv/krx/bin/python _scripts/네이버_시세컨센_수집.py --codes-file /tmp/universe.txt --out 국내주식
# 원장 추출은 미니에서 (탭 구분 TSV: code<TAB>name<TAB>wics<TAB>market)
scp _scripts/원장_컨센추출_미니.py mini:/tmp/ && scp /tmp/universe.tsv mini:/tmp/
ssh mini 'cd ~/research-site/demo && UNIVERSE=/tmp/universe.tsv OUT=/tmp/consensus.json python3 /tmp/원장_컨센추출_미니.py'
scp mini:/tmp/consensus.json _manifest/데이터/국내주식_컨센추이_<날짜>.json
~/.venv/krx/bin/python _scripts/국내주식_코스피200_문서생성.py
```

**목록 파일은 탭으로 구분한다.** WICS 산업명에 쉼표가 들어간다(`섬유,의류,신발,호화품`).
쉼표로 나누면 조용히 어긋나 스크립트가 중간에 죽는다.
