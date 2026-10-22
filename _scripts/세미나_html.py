# -*- coding: utf-8 -*-
"""기초세미나 HTML 렌더러 — `_seminar/<slug>.json` 을 단독 실행 HTML 한 장으로 만든다.

사용: python _scripts/세미나_html.py _seminar/shipbuilding.json 10_국내주식/07_조선/조선업_기초세미나_2026-10.html
스키마는 `_seminar/SCHEMA.md`. 외부 의존성 없음(폰트·스크립트·차트 전부 인라인) — 오프라인 발표에서도 열린다.
차트는 SVG 를 파이썬에서 직접 그린다. 값은 스펙의 숫자를 그대로 쓰고, 렌더러는 축 눈금만 계산한다.
"""
import html, json, math, re, sys

SPEC, OUT = sys.argv[1], sys.argv[2]
S = json.load(open(SPEC, encoding="utf-8"))
E = html.escape

# ── 색: dataviz 기본 팔레트(검증된 순서 고정) ─────────────────────────────
SERIES_L = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
SERIES_D = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]

CSS = """
:root{--page:#f9f9f7;--surface:#fcfcfb;--raise:#ffffff;--ink:#0b0b0b;--ink2:#52514e;--muted:#6f6d68;--grid:#e1e0d9;--axis:#c3c2b7;
--line:rgba(11,11,11,.10);--accent:#2a78d6;--accent-soft:#e8f1fc;--pos:#2a78d6;--neg:#d03b3b;--good:#006300;--warn-bg:#fff6e5;--warn-ink:#7a4a00;
--good-bg:#eaf6ea;--info-bg:#eef4fb;--now:#eb6834;--chip:#f0efec;
""" + "".join(f"--s{i+1}:{c};" for i, c in enumerate(SERIES_L)) + """
color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--page:#0d0d0d;--surface:#1a1a19;--raise:#222220;--ink:#f0efec;--ink2:#c3c2b7;--muted:#9a988f;
--grid:#2c2c2a;--axis:#4a4a46;--line:rgba(255,255,255,.10);--accent:#3987e5;--accent-soft:#1b2a3d;--pos:#3987e5;--neg:#e66767;--good:#0ca30c;
--warn-bg:#33270f;--warn-ink:#f2c46b;--good-bg:#132a13;--info-bg:#17222f;--now:#d95926;--chip:#2c2c2a;""" + "".join(f"--s{i+1}:{c};" for i, c in enumerate(SERIES_D)) + """color-scheme:dark}}
:root[data-theme="dark"]{--page:#0d0d0d;--surface:#1a1a19;--raise:#222220;--ink:#f0efec;--ink2:#c3c2b7;--muted:#9a988f;
--grid:#2c2c2a;--axis:#4a4a46;--line:rgba(255,255,255,.10);--accent:#3987e5;--accent-soft:#1b2a3d;--pos:#3987e5;--neg:#e66767;--good:#0ca30c;
--warn-bg:#33270f;--warn-ink:#f2c46b;--good-bg:#132a13;--info-bg:#17222f;--now:#d95926;--chip:#2c2c2a;""" + "".join(f"--s{i+1}:{c};" for i, c in enumerate(SERIES_D)) + """color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--page);color:var(--ink);font:16px/1.65 system-ui,-apple-system,"Apple SD Gothic Neo","Malgun Gothic","Segoe UI",sans-serif;word-break:keep-all;overflow-wrap:anywhere}
a{color:var(--accent)}main{min-width:0}.fig{min-width:0}
.wrap{display:grid;grid-template-columns:240px minmax(0,1fr);gap:40px;max-width:1240px;margin:0 auto;padding:32px 24px 80px}
nav.toc{position:sticky;top:24px;align-self:start;font-size:14px}
nav.toc .brand{font-weight:700;font-size:13px;color:var(--muted);letter-spacing:.02em;margin-bottom:12px}
nav.toc ol{list-style:none;margin:0;padding:0;counter-reset:t}
nav.toc li{counter-increment:t}
nav.toc a{display:block;padding:6px 10px;border-radius:8px;color:var(--ink2);text-decoration:none}
nav.toc a::before{content:counter(t) ". ";color:var(--muted)}
nav.toc a.on{background:var(--accent-soft);color:var(--ink);font-weight:600}
nav.toc .tools{margin-top:16px;display:flex;gap:8px;flex-wrap:wrap}
button.tb{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--raise);color:var(--ink2);border-radius:8px;padding:6px 10px;cursor:pointer}
header.hero{padding:8px 0 28px;border-bottom:1px solid var(--line);margin-bottom:8px}
.eyebrow{font-size:13px;color:var(--muted);font-weight:600;letter-spacing:.02em}
h1{font-size:34px;line-height:1.25;margin:6px 0 8px;letter-spacing:-.01em}
.sub{font-size:18px;color:var(--ink2);margin:0 0 18px}
.one{font-size:19px;font-weight:600;border-left:4px solid var(--accent);padding:4px 0 4px 14px;margin:20px 0 22px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.kpi .l{font-size:13px;color:var(--ink2)}.kpi .v.sm{font-size:18px;line-height:1.35}.kpi .v{font-size:24px;font-weight:700;font-variant-numeric:tabular-nums;margin:2px 0}
.kpi .n{font-size:13px;color:var(--ink2)}.kpi .s{font-size:11.5px;color:var(--muted);margin-top:6px}
section.sec{padding:36px 0 8px;border-bottom:1px solid var(--line)}
section.sec>h2{font-size:24px;margin:0 0 6px;letter-spacing:-.01em}
section.sec>h2 .no{color:var(--accent);margin-right:8px}
.lead{color:var(--ink2);font-size:17px;margin:0 0 18px}
.blk{margin:18px 0}
.text p{margin:0 0 10px}.text ul{margin:0 0 10px;padding-left:20px}.text li{margin:3px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.card h4{margin:0 0 6px;font-size:16px}.card p{margin:0;color:var(--ink2);font-size:14.5px}
.tag{display:inline-block;font-size:11.5px;font-weight:600;background:var(--chip);color:var(--ink2);border-radius:999px;padding:1px 8px;margin-bottom:6px}
.flow{display:flex;flex-wrap:wrap;row-gap:10px;align-items:stretch}
.step{flex:1 1 150px;min-width:150px;max-width:260px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;position:relative}
.step .k{font-size:12px;color:var(--accent);font-weight:700}.step h4{margin:2px 0 4px;font-size:15.5px}.step p{margin:0;font-size:13.5px;color:var(--ink2)}
.step .who{margin-top:8px;font-size:12px;color:var(--muted)}
.arrow{flex:0 0 22px;display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:18px}
.cycle{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;counter-reset:c}
.ph{counter-increment:c;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;position:relative}
.ph::before{content:counter(c);position:absolute;top:10px;right:12px;font-size:12px;color:var(--muted);font-weight:700}
.ph h4{margin:0 0 4px;font-size:15.5px}.ph p{margin:0;font-size:13.5px;color:var(--ink2)}
.ph.now{border:2px solid var(--now);background:color-mix(in srgb,var(--now) 7%,var(--surface))}
.ph.now .here{display:inline-block;font-size:11.5px;font-weight:700;color:#fff;background:var(--now);border-radius:999px;padding:1px 8px;margin-bottom:6px}
.note{font-size:13px;color:var(--muted);margin-top:8px}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
table{border-collapse:collapse;width:max-content;min-width:100%;font-size:14px;font-variant-numeric:tabular-nums}
th,td{padding:8px 12px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left;max-width:24em;min-width:4.5em}
th{font-size:12.5px;color:var(--ink2);font-weight:600;background:var(--raise);position:sticky;top:0}
tr:last-child td{border-bottom:0}td.r,th.r{text-align:right;white-space:nowrap}
.callout{border-radius:12px;padding:12px 16px;font-size:15px}
.callout.info{background:var(--info-bg)}.callout.warn{background:var(--warn-bg);color:var(--warn-ink)}.callout.good{background:var(--good-bg)}
.callout .ic{font-weight:700;margin-right:6px}
.callout p{margin:0 0 6px}.callout p:last-child{margin:0}
.fig{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.fig h4{margin:0 0 2px;font-size:15.5px}.fig .u{font-size:12.5px;color:var(--muted)}
.fig .sc{overflow-x:auto;margin-top:8px}.fig svg{display:block;width:100%;min-width:620px;height:auto;overflow:visible}
.fig svg text{fill:var(--ink2);font-size:13px;font-family:inherit}
.fig svg .ax{stroke:var(--axis)}.fig svg .gr{stroke:var(--grid)}
.fig svg .hit{fill:transparent;cursor:default}
.fig svg .m:hover,.fig svg .hit:hover+.m{opacity:.8}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px;color:var(--ink2);margin-top:6px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;vertical-align:-1px}
details.tv{margin-top:8px;font-size:13px}details.tv summary{cursor:pointer;color:var(--muted)}
details.tv table{margin-top:6px;font-size:13px}
.tip{position:fixed;pointer-events:none;background:var(--raise);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:6px 10px;font-size:13px;box-shadow:0 4px 16px rgba(0,0,0,.12);display:none;z-index:9;white-space:nowrap}
.chk{display:grid;gap:10px}
.ck{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1.4fr) minmax(0,1.1fr) minmax(0,1fr);gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:14px}
.ck b{display:block;font-size:15px}.ck .lb{display:block;font-size:11.5px;color:var(--muted);font-weight:600;margin-bottom:2px}
.gl{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:8px 18px}
.gl div{padding:8px 0;border-bottom:1px solid var(--line)}.gl b{display:block}.gl span{font-size:14px;color:var(--ink2)}
footer.src{padding:28px 0;font-size:13px;color:var(--muted)}footer.src li{margin:2px 0}
@media (max-width:900px){.wrap{grid-template-columns:minmax(0,1fr);gap:0;padding:16px 16px 60px}nav.toc{position:static;margin-bottom:12px}
nav.toc ol{display:flex;gap:4px;overflow-x:auto;padding-bottom:6px}nav.toc a{white-space:nowrap}h1{font-size:27px}
.ck{grid-template-columns:1fr}.flow{flex-direction:column}.arrow{transform:rotate(90deg);height:22px}.step{min-width:0}}
@media print{nav.toc{display:none}.wrap{display:block;max-width:none;padding:0}section.sec{break-before:page;border:0}
details.tv{display:none}body{background:#fff}}
body.present section.sec{min-height:100vh;display:flex;flex-direction:column;justify-content:flex-start;padding-top:48px}
body.present{font-size:18px}
"""

JS = r"""
(()=>{const r=document.documentElement;const k='seminar-theme';
try{const t=localStorage.getItem(k);if(t)r.dataset.theme=t}catch(e){}
document.getElementById('theme').onclick=()=>{const d=r.dataset.theme||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
r.dataset.theme=d==='dark'?'light':'dark';try{localStorage.setItem(k,r.dataset.theme)}catch(e){}};
document.getElementById('present').onclick=()=>document.body.classList.toggle('present');
const secs=[...document.querySelectorAll('section.sec')],links=[...document.querySelectorAll('nav.toc a')];
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){links.forEach(a=>a.classList.toggle('on',a.hash==='#'+e.target.id))}})},{rootMargin:'-30% 0px -60% 0px'});
secs.forEach(s=>io.observe(s));
const cur=()=>{let i=0;secs.forEach((s,j)=>{if(s.getBoundingClientRect().top<120)i=j});return i};
addEventListener('keydown',e=>{if(e.target.closest('input,textarea'))return;
if(e.key==='ArrowRight'||e.key==='PageDown'||e.key==='j'){e.preventDefault();(secs[cur()+1]||secs[cur()]).scrollIntoView()}
if(e.key==='ArrowLeft'||e.key==='PageUp'||e.key==='k'){e.preventDefault();(secs[Math.max(cur()-1,0)]).scrollIntoView()}});
const tip=document.querySelector('.tip');
document.querySelectorAll('[data-tip]').forEach(n=>{n.addEventListener('mousemove',e=>{tip.textContent=n.dataset.tip;tip.style.display='block';
const x=Math.min(e.clientX+14,innerWidth-tip.offsetWidth-8);tip.style.left=x+'px';tip.style.top=(e.clientY+14)+'px'});
n.addEventListener('mouseleave',()=>tip.style.display='none')});
})();
"""


def md(s):
    """**굵게**, '- ' 목록, 빈 줄 문단만."""
    out = []
    for para in re.split(r"\n\s*\n", (s or "").strip()):
        lines = para.split("\n")
        if all(l.strip().startswith("- ") for l in lines if l.strip()):
            out.append("<ul>" + "".join(f"<li>{inline(l.strip()[2:])}</li>" for l in lines if l.strip()) + "</ul>")
        else:
            out.append(f"<p>{inline(' '.join(l.strip() for l in lines))}</p>")
    return "".join(out)


def inline(s):
    s = E(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


DEC = [0]  # 현재 차트의 소수 자릿수(차트마다 dec_for 로 정한다)


def dec_for(vals):
    vals = [v for v in vals if v is not None]
    return 1 if any(abs(v) < 100 and not float(v).is_integer() for v in vals) else 0


def fmt(v, d=None):
    if v is None:
        return "—"
    d = DEC[0] if d is None else d
    return f"{v:,.{d}f}".replace("-", "−")


def nice_ticks(lo, hi, n=5):
    if lo == hi:
        hi = lo + 1
    span = hi - lo
    step = 10 ** math.floor(math.log10(span / n))
    for m in (1, 2, 2.5, 5, 10):
        if span / (step * m) <= n:
            step *= m
            break
    a = math.floor(lo / step) * step
    b = math.ceil(hi / step) * step
    t, x = [], a
    while x <= b + step / 2:
        t.append(round(x, 10))
        x += step
    return t


def merge_labels(series):
    """계열마다 빠진 라벨(리포트 없는 달)이 달라도 각 계열 안의 순서를 지키며 합친다."""
    labels = []
    for s in series:
        prev = -1
        for l, _ in s["data"]:
            if l in labels:
                prev = labels.index(l)
            else:
                labels.insert(prev + 1, l)
                prev += 1
    return labels


def table_view(series, unit):
    labels = merge_labels(series)
    head = "<tr><th></th>" + "".join(f"<th class='r'>{E(s['name'])}</th>" for s in series) + "</tr>"
    rows = ""
    for l in labels:
        rows += f"<tr><td>{E(str(l))}</td>" + "".join(
            f"<td class='r'>{fmt(dict(s['data']).get(l))}</td>" for s in series) + "</tr>"
    return f"<details class='tv'><summary>표로 보기 ({E(unit)})</summary><div class='tw'><table>{head}{rows}</table></div></details>"


def chart_hbar(b):
    s = b["series"][0]
    data = s["data"]
    W, rowh, lw = 720, 30, 170
    vals = [v for _, v in data]
    lo, hi = min(0, min(vals)), max(0, max(vals))
    ticks = nice_ticks(lo, hi)
    lo, hi = ticks[0], ticks[-1]
    pad = 64 if lo < 0 else 0  # 음수 막대 끝 값 라벨 자리
    pw = W - lw - 64 - pad
    X = lambda v: lw + pad + (v - lo) / (hi - lo) * pw
    H = rowh * len(data) + 30
    g = [f"<svg viewBox='0 0 {W} {H}' role='img' aria-label='{E(b['title'])}'>"]
    for t in ticks:
        g.append(f"<line class='gr' x1='{X(t):.1f}' x2='{X(t):.1f}' y1='0' y2='{H-24}'/>"
                 f"<text x='{X(t):.1f}' y='{H-8}' text-anchor='middle'>{fmt(t, 0 if float(t).is_integer() else 1)}</text>")
    g.append(f"<line class='ax' x1='{X(0):.1f}' x2='{X(0):.1f}' y1='0' y2='{H-24}' stroke-width='1.5'/>")
    for i, (l, v) in enumerate(data):
        y = i * rowh + 6
        x0, x1 = sorted((X(0), X(v)))
        col = "var(--pos)" if v >= 0 else "var(--neg)"
        r = min(4, (x1 - x0) / 2)
        g.append(f"<text x='{lw-10}' y='{y+13}' text-anchor='end'>{E(str(l))}</text>")
        g.append(f"<rect class='m' x='{x0:.1f}' y='{y}' width='{max(x1-x0,1):.1f}' height='18' rx='{r:.1f}' fill='{col}'"
                 f" data-tip='{E(str(l))}: {fmt(v)}{E(b.get('unit_suffix',''))}'/>")
        tx = X(v) + (6 if v >= 0 else -6)
        g.append(f"<text x='{tx:.1f}' y='{y+13}' text-anchor='{'start' if v >= 0 else 'end'}' style='fill:var(--ink)'>{fmt(v)}{E(b.get('unit_suffix',''))}</text>")
    g.append("</svg>")
    return "".join(g)


def chart_bar(b):
    series = b["series"]
    labels = merge_labels(series)
    vals = [v for s in series for _, v in s["data"] if v is not None]
    lo, hi = min(0, min(vals)), max(0, max(vals))
    ticks = nice_ticks(lo, hi)
    lo, hi = ticks[0], ticks[-1]
    W, H, lm, bm, tm = 720, 300, 56, 46, 14
    pw, ph = W - lm - 10, H - bm - tm
    Y = lambda v: tm + (hi - v) / (hi - lo) * ph
    gw = pw / len(labels)
    n = len(series)
    bw = min(34, (gw - 14) / n - 2)
    g = [f"<svg viewBox='0 0 {W} {H}' role='img' aria-label='{E(b['title'])}'>"]
    for t in ticks:
        g.append(f"<line class='gr' x1='{lm}' x2='{W-10}' y1='{Y(t):.1f}' y2='{Y(t):.1f}'/>"
                 f"<text x='{lm-8}' y='{Y(t)+4:.1f}' text-anchor='end'>{fmt(t, 0 if float(t).is_integer() else 1)}</text>")
    g.append(f"<line class='ax' x1='{lm}' x2='{W-10}' y1='{Y(0):.1f}' y2='{Y(0):.1f}' stroke-width='1.5'/>")
    for i, l in enumerate(labels):
        cx = lm + gw * i + gw / 2
        g.append(f"<text x='{cx:.1f}' y='{H-bm+18}' text-anchor='middle'>{E(str(l))}</text>")
        for j, s in enumerate(series):
            v = dict(s["data"]).get(l)
            if v is None:
                continue
            x = cx - (n * (bw + 2)) / 2 + j * (bw + 2)
            y0, y1 = sorted((Y(0), Y(v)))
            col = f"var(--s{j+1})" if n > 1 else ("var(--pos)" if v >= 0 else "var(--neg)") if b.get("diverging") else "var(--s1)"
            g.append(f"<rect class='m' x='{x:.1f}' y='{y0:.1f}' width='{bw:.1f}' height='{max(y1-y0,1):.1f}' rx='3' fill='{col}'"
                     f" data-tip='{E(s['name'])} · {E(str(l))}: {fmt(v)}{E(b.get('unit_suffix',''))}'/>")
            if n <= 2 and len(labels) <= 12:
                ty = Y(v) - 6 if v >= 0 else Y(v) + 14
                g.append(f"<text x='{x+bw/2:.1f}' y='{ty:.1f}' text-anchor='middle' style='fill:var(--ink);font-size:11px'>{fmt(v)}</text>")
    g.append("</svg>")
    return "".join(g)


def chart_line(b):
    series = b["series"]
    labels = merge_labels(series)
    vals = [v for s in series for _, v in s["data"] if v is not None]
    lo, hi = min(vals), max(vals)
    if b.get("zero", False) or lo > 0 and lo / hi < 0.35:
        lo = min(0, lo)
    ticks = nice_ticks(lo, hi)
    lo, hi = ticks[0], ticks[-1]
    W, H, lm, bm, tm, rm = 720, 300, 60, 40, 14, 110
    pw, ph = W - lm - rm, H - bm - tm
    X = lambda i: lm + (i / max(len(labels) - 1, 1)) * pw
    Y = lambda v: tm + (hi - v) / (hi - lo) * ph
    g = [f"<svg viewBox='0 0 {W} {H}' role='img' aria-label='{E(b['title'])}'>"]
    for t in ticks:
        g.append(f"<line class='gr' x1='{lm}' x2='{lm+pw}' y1='{Y(t):.1f}' y2='{Y(t):.1f}'/>"
                 f"<text x='{lm-8}' y='{Y(t)+4:.1f}' text-anchor='end'>{fmt(t, 0 if float(t).is_integer() else 1)}</text>")
    if lo < 0 < hi:
        g.append(f"<line class='ax' x1='{lm}' x2='{lm+pw}' y1='{Y(0):.1f}' y2='{Y(0):.1f}' stroke-width='1.5'/>")
    step = max(1, math.ceil(len(labels) / 8))
    for i, l in enumerate(labels):
        if i % step == 0 or i == len(labels) - 1:
            g.append(f"<text x='{X(i):.1f}' y='{H-bm+20}' text-anchor='middle'>{E(str(l))}</text>")
    ends = []
    for j, s in enumerate(series):
        d = dict(s["data"])
        pts = [(X(i), Y(d[l]), l, d[l]) for i, l in enumerate(labels) if d.get(l) is not None]
        col = f"var(--s{j+1})"
        path = " ".join(f"{'M' if k == 0 else 'L'}{x:.1f},{y:.1f}" for k, (x, y, _, _) in enumerate(pts))
        g.append(f"<path d='{path}' fill='none' stroke='{col}' stroke-width='2' stroke-linejoin='round'/>")
        for x, y, l, v in pts:
            g.append(f"<circle class='hit' cx='{x:.1f}' cy='{y:.1f}' r='9' data-tip='{E(s['name'])} · {E(str(l))}: {fmt(v)}{E(b.get('unit_suffix',''))}'/>"
                     f"<circle class='m' cx='{x:.1f}' cy='{y:.1f}' r='3.5' fill='{col}' stroke='var(--surface)' stroke-width='2' pointer-events='none'/>")
        if pts and len(series) <= 4:
            ends.append([pts[-1][1], s["name"], col])
    ends.sort()
    for k in range(1, len(ends)):
        if ends[k][0] - ends[k - 1][0] < 14:
            ends[k][0] = ends[k - 1][0] + 14
    for y, name, col in ends:
        g.append(f"<text x='{lm+pw+8}' y='{y+4:.1f}' style='fill:var(--ink)'>{E(name)}</text>")
    g.append("</svg>")
    return "".join(g)


def legend(series):
    if len(series) < 2:
        return ""
    return "<div class='legend'>" + "".join(f"<span><i style='background:var(--s{j+1})'></i>{E(s['name'])}</span>" for j, s in enumerate(series)) + "</div>"


def tag(c):
    return f"<span class='tag'>{E(c['tag'])}</span>" if c.get("tag") else ""


def block(b):
    t = b["type"]
    if t == "text":
        return f"<div class='blk text'>{md(b['md'])}</div>"
    if t == "cards":
        return "<div class='blk cards'>" + "".join(
            f"<div class='card'>{tag(c)}<h4>{inline(c['title'])}</h4><p>{inline(c['body'])}</p></div>"
            for c in b["items"]) + "</div>"
    if t == "flow":
        parts = []
        for i, s in enumerate(b["steps"]):
            if i:
                parts.append("<div class='arrow' aria-hidden='true'>→</div>")
            who = f"<div class='who'>{inline(s['who'])}</div>" if s.get("who") else ""
            parts.append(f"<div class='step'><div class='k'>{i+1:02d}</div><h4>{inline(s['title'])}</h4><p>{inline(s['body'])}</p>{who}</div>")
        return "<div class='blk flow'>" + "".join(parts) + "</div>"
    if t == "cycle":
        ph = "".join(f"<div class='ph{' now' if p.get('now') else ''}'>{'<span class=here>지금</span>' if p.get('now') else ''}<h4>{inline(p['name'])}</h4><p>{inline(p['signal'])}</p></div>"
                     for p in b["phases"])
        note = f"<div class='note'>{inline(b['note'])}</div>" if b.get("note") else ""
        return f"<div class='blk'><div class='cycle'>{ph}</div>{note}</div>"
    if t == "table":
        al = b.get("align") or []
        cls = lambda i: " class='r'" if i < len(al) and al[i] == "r" else ""
        head = "".join(f"<th{cls(i)}>{inline(str(c))}</th>" for i, c in enumerate(b["columns"]))
        rows = "".join("<tr>" + "".join(f"<td{cls(i)}>{inline(str(c))}</td>" for i, c in enumerate(r)) + "</tr>" for r in b["rows"])
        note = f"<div class='note'>{inline(b['note'])}</div>" if b.get("note") else ""
        return f"<div class='blk'><div class='tw'><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>{note}</div>"
    if t == "chart":
        k = b["kind"]
        DEC[0] = dec_for([v for s_ in b["series"] for _, v in s_["data"]])
        svg = chart_hbar(b) if k == "hbar" else chart_bar(b) if k == "bar" else chart_line(b)
        lg = legend(b["series"]) if k != "hbar" else ""
        note = f"<div class='note'>{inline(b['note'])}</div>" if b.get("note") else ""
        src = f"<div class='note'>출처: {inline(b['src'])}</div>" if b.get("src") else ""
        return (f"<figure class='blk fig' style='margin:18px 0'><h4>{inline(b['title'])}</h4><div class='u'>{E(b.get('unit',''))}</div>"
                f"<div class='sc'>{svg}</div>{lg}{note}{src}{table_view(b['series'], b.get('unit',''))}</figure>")
    if t == "callout":
        ic = {"info": "판단", "warn": "주의", "good": "포인트"}[b.get("tone", "info")]
        lab = "" if re.match(r"^\W*(판단|주의|포인트)", b["md"]) else f"<span class='ic'>{ic}</span>"
        return f"<div class='blk callout {b.get('tone','info')}'>{lab}{md(b['md'])}</div>"
    if t == "checklist":
        return "<div class='blk chk'>" + "".join(
            f"<div class='ck'><div><span class='lb'>데이터</span><b>{inline(i['what'])}</b></div><div><span class='lb'>왜 보나</span>{inline(i['why'])}</div>"
            f"<div><span class='lb'>지금</span>{inline(i.get('now','—'))}</div><div><span class='lb'>어디서 · 언제</span>{inline(i.get('where','—'))}</div></div>"
            for i in b["items"]) + "</div>"
    if t == "glossary":
        return "<div class='blk gl'>" + "".join(f"<div><b>{inline(i['term'])}</b><span>{inline(i['def'])}</span></div>" for i in b["items"]) + "</div>"
    raise ValueError(f"모르는 블록: {t}")


h = S["hero"]
kpis = "".join(f"<div class='kpi'><div class='l'>{inline(k['label'])}</div><div class='v{' sm' if len(k['value']) > 7 else ''}'>{inline(k['value'])}</div>"
               f"<div class='n'>{inline(k.get('note',''))}</div><div class='s'>{inline(k.get('src',''))}</div></div>" for k in h.get("kpis", []))
toc = "".join(f"<li><a href='#{E(s['id'])}'>{E(s['title'])}</a></li>" for s in S["sections"])
secs = ""
for i, s in enumerate(S["sections"], 1):
    lead = f"<p class='lead'>{inline(s['lead'])}</p>" if s.get("lead") else ""
    secs += f"<section class='sec' id='{E(s['id'])}'><h2><span class='no'>{i:02d}</span>{inline(s['title'])}</h2>{lead}" + "".join(block(b) for b in s["blocks"]) + "</section>"
src = "".join(f"<li>{inline(x)}</li>" for x in S.get("sources", []))

doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(S['title'])}</title><meta name="description" content="{E(S.get('subtitle',''))}"><style>{CSS}</style></head>
<body><div class="wrap"><nav class="toc" aria-label="목차"><div class="brand">{E(S['title'])}</div><ol>{toc}</ol>
<div class="tools"><button class="tb" id="theme" type="button">밝게/어둡게</button><button class="tb" id="present" type="button">발표 모드</button></div>
<div class="note">← → 키로 섹션 이동</div></nav>
<main><header class="hero"><div class="eyebrow">기초세미나 · 기준일 {E(S['asof'])}{' · ' + E(S['audience']) if S.get('audience') else ''}</div>
<h1>{E(S['title'])}</h1><p class="sub">{inline(S.get('subtitle',''))}</p><div class="one">{inline(h['one_liner'])}</div><div class="kpis">{kpis}</div></header>
{secs}<footer class="src"><b>출처</b><ul>{src}</ul><div>숫자는 저장소 문서·맥미니 원장 추출본(`_manifest/데이터`)에서 그대로 옮겼다. 렌더러 `_scripts/세미나_html.py`.</div></footer></main></div>
<div class="tip" role="tooltip"></div><script>{JS}</script></body></html>"""
open(OUT, "w", encoding="utf-8").write(doc)
print("ok", OUT, f"{len(doc)/1024:.0f}KB", f"섹션 {len(S['sections'])}")
