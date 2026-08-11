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
