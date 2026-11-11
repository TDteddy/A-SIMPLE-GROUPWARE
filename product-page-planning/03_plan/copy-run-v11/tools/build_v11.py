#!/usr/bin/env python3
"""v11 기획안을 조립한다.
사용: python3 tools/build_v10.py <런 폴더> <출력 md>
읽는 것: v11_틀.md, P_상업용.md(본안), 있으면 W1_선명.md·W2_강렬.md·W3_담백.md(바꿔 끼울 후보),
        C_공통칸.json, tools/studio_defaults.json, S_확인.md, S_부록.md
쓰는 것: 출력 md, N001_v11_스튜디오_문구.json(스튜디오 시안의 texts 값)
"""
import json, os, re, sys

RUN, OUT = sys.argv[1], sys.argv[2]
P = lambda n: os.path.join(RUN, n)
D = json.load(open(P("tools/studio_defaults.json"), encoding="utf-8"))
C = json.load(open(P("C_공통칸.json"), encoding="utf-8"))

UNITS = {
    "03": [("제목 (T1 / T2)", [1, 2], " / "), ("보조문 (T3 / T4)", [3, 4], " / "), ("칩 (T5 · T6 · T7)", [5, 6, 7], " · ")],
    "04": [("제목 (T0 / T1)", [0, 1], " / "), ("카드 1 (T2 — T3)", [2, 3], " — "), ("카드 2 (T4 — T5)", [4, 5], " — "),
           ("카드 3 (T6 — T7)", [6, 7], " — "), ("카드 4 (T8 — T9)", [8, 9], " — ")],
    "05": [("제목 (T0 / T1)", [0, 1], " / "), ("큰 사진 위 띠 문구 (T14 / T15)", [14, 15], " / "),
           ("사진 캡션 1 (T16)", [16], ""), ("사진 캡션 2 (T17)", [17], ""), ("사진 캡션 3 (T18)", [18], "")],
    "07": [("제목 (T0 / T1)", [0, 1], " / "), ("자석 헤드 설명 (T7)", [7], ""), ("관절 설명 (T9)", [9], ""),
           ("흡착 베이스 설명 (T11)", [11], ""), ("맺음 제목 (T12 / T13)", [12, 13], " / ")],
    "08": [("제목 (T1 / T2)", [1, 2], " / "), ("본문 (T3 / T4)", [3, 4], " / ")],
    "09": [("제목 (T1)", [1], ""), ("본문 (T2 / T3)", [2, 3], " / ")],
    "10": [("제목 (T1 / T2)", [1, 2], " / "), ("본문 (T3 / T4 / T5)", [3, 4, 5], " / ")],
    "11": [("제목 (T0 / T1)", [0, 1], " / ")],
    "12": [("제목 (T0 / T1)", [0, 1], " / ")],
}
REVIEWS = [(3, 4, 5, 6), (7, 8, 9, 10), (11, 12, 13, 14), (15, 16, 17, 18), (19, 20, 21, 22)]
# 바꿔 끼울 후보로 보여 줄 제목 칸
ALT_SLOTS = [("03", "메인 제목", [1, 2]), ("04", "타겟 제목", [0, 1]), ("05", "위험소구 제목", [0, 1]),
             ("07", "설계 제목", [0, 1]), ("07", "설계 맺음 제목", [12, 13]), ("08", "설치 제목", [1, 2]),
             ("09", "방향·기울기 제목", [1]), ("10", "접이 제목", [1, 2]), ("11", "비교 제목", [0, 1]),
             ("12", "라이프스타일 제목", [0, 1])]


# 광고주가 그만 쓰자고 한 표현(의성어 착, 보기 편한 자리)이 든 후보는 싣지 않는다
BANNED = re.compile(r"(?<![가-힣])착(?![가-힣])|보기 편한")


def parse(path):
    pages, extra, sec, cur = {}, {}, None, None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = re.match(r"^##\s+(\d{2})\b", line)
        if m:
            sec, cur = m.group(1), None
            pages.setdefault(sec, {})
            continue
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            sec, cur = None, m.group(1).strip()
            extra[cur] = []
            continue
        if sec:
            m = re.match(r"^\s*T(\d+)\s*:\s?(.*)$", line)
            if m:
                pages[sec][int(m.group(1))] = m.group(2).strip().replace('\\n', ' / ')
        elif cur and line.strip():
            extra[cur].append(line)
    return pages, extra


def esc(s):
    return s.replace("|", "\\|")


def join(t, slots, sep):
    return esc(sep.join((t.get(k) or "").strip() for k in slots))


page, extra = parse(P("P_상업용.md"))
alts = []
for f in ("W1_선명.md", "W2_강렬.md", "W3_담백.md"):
    if os.path.exists(P(f)):
        pg, ex = parse(P(f))
        if "12" in pg and pg["12"].get(1):  # 끝까지 쓴 파일만
            alts.append((pg, ex))


def table_T(sec):
    dflt = {i: t for i, t in enumerate(D[sec]["texts"])}
    t = page.get(sec, {})
    rows = ["| 자리 | 기본안 | 이번 문구 |", "|---|---|---|"]
    if sec == "06":
        rows.append("| 제목 (T1 / T2) | " + join(dflt, [1, 2], " / ") + " | **" + join(t, [1, 2], " / ") + "** |")
        for n, (who, a, b, c) in enumerate(REVIEWS, 1):
            def rv(x):
                return esc(f"`{(x.get(who) or '').strip()}`<br>{(x.get(a) or '').strip()} **{(x.get(b) or '').strip()}** {(x.get(c) or '').strip()}")
            rows.append(f"| 후기 {n} (T{who}~T{c}) | {rv(dflt)} | {rv(t)} |")
        return "\n".join(rows)
    for name, slots, sep in UNITS[sec]:
        cur = join(t, slots, sep)
        if name.startswith("제목") or name.startswith("맺음"):
            cur = f"**{cur}**"
        rows.append(f"| {name} | {join(dflt, slots, sep)} | {cur} |")
    return "\n".join(rows)


def table_C(sec):
    dflt = D[sec]["texts"]
    cur = C.get(sec, {})
    rows = ["| 칸 | 기본안 | 이번 문구 |", "|---|---|---|"]
    for k in sorted(cur, key=int):
        base = dflt[int(k)]
        if base.strip() == cur[k].strip():
            continue
        rows.append(f"| T{k} | {esc(base)} | {esc(cur[k])} |")
    out = "\n".join(rows) if len(rows) > 2 else "기본안 그대로."
    for group, items in C.get(sec + "_추가행", {}).items():
        out += f"\n\n스튜디오에서 행을 늘려 넣는 것 — {group}\n\n"
        if items and isinstance(items[0], list):
            out += "| 항목 | 내용 |\n|---|---|\n" + "\n".join(f"| {esc(a)} | {esc(b)} |" for a, b in items)
        else:
            out += "\n".join(f"- {x}" for x in items)
    return out


def alt_table():
    if not alts and not extra.get("메인 다른 안"):
        return ""
    L = ["## 2. 바꿔 끼울 수 있는 제목 후보", "",
         "모두 템플릿 한 줄 용량 안에 들어가는 것만 실었다. 스튜디오에서 그 칸만 바꿔 넣으면 된다.", ""]
    head = "| 자리 | 본안 |" + "".join(f" 후보 {i} |" for i in range(1, len(alts) + 1))
    L += [head, "|---|---|" + "---|" * len(alts)]
    for sec, name, slots in ALT_SLOTS:
        row = f"| {sec} {name} | {join(page.get(sec, {}), slots, ' / ')} |"
        for pg, _ in alts:
            cand = join(pg.get(sec, {}), slots, ' / ')
            row += f" {cand if not BANNED.search(cand) else '—'} |"
        L.append(row)
    more = [x.lstrip("- ").strip() for x in extra.get("메인 다른 안", [])]
    for _, ex in alts:
        more += [x.lstrip("- ").strip() for x in ex.get("메인 다른 안", [])]
    more = [m for m in more if not BANNED.search(m)]
    if more:
        L += ["", "메인 제목으로 더 써 본 것: " + " · ".join(f"`{m}`" for m in more)]
    return "\n".join(L)


doc = open(P("v11_틀.md"), encoding="utf-8").read()
doc = re.sub(r"<<T:(\d{2})>>", lambda m: table_T(m.group(1)), doc)
doc = re.sub(r"<<C:(\d{2})>>", lambda m: table_C(m.group(1)), doc)
doc = doc.replace("<<ALTS>>", "")
F = {}
for name in ("F1_교정자.json", "F2_소비자.json"):
    if os.path.exists(P(name)):
        F[name[:2]] = json.load(open(P(name), encoding="utf-8"))["줄"]


def second(m):
    nums = m.group(1).split(",")
    out = []
    for n in nums:
        a = F.get("F1", {}).get(n, {}).get("자연")
        b = F.get("F2", {}).get(n, {}).get("자연")
        c = F.get("F2", {}).get(n, {}).get("끌림")
        if a is None and b is None:
            return "2차 읽기 대기"
        out.append(f"자연 {a}·{b}, 끌림 {c}")
    return "2차 " + " / ".join(out)


doc = re.sub(r"\{\{F:([0-9,]+)\}\}", second, doc)
for tok, f in [("<<VERIFY>>", "S_검증.md"), ("<<CONFIRM>>", "S_확인.md"), ("<<APPENDIX>>", "S_부록.md")]:
    doc = doc.replace(tok, open(P(f), encoding="utf-8").read().strip() if os.path.exists(P(f)) else "")
doc = re.sub(r"\n{3,}", "\n\n", doc).rstrip() + "\n"
open(OUT, "w", encoding="utf-8").write(doc)

# 스튜디오 시안의 texts 값
texts = {s: dict(v) for s, v in C.items() if s.isdigit()}
for sec, d in page.items():
    texts.setdefault(sec, {})
    for k, v in d.items():
        texts[sec][str(k)] = v.replace(' / ', '\n') if (sec, k) == ('09', 1) else v
for _, a, _b, c in REVIEWS:
    r = texts["06"]
    r[str(a)] = r[str(a)].rstrip() + " "
    r[str(c)] = " " + r[str(c)].lstrip()
json.dump({"_설명": "영역 번호(01~14) → 칸 번호 → 문구. 스튜디오 시안에서 그 영역 후보의 texts 에 들어가는 값. 적혀 있지 않은 칸은 템플릿 기본 문구.",
           "texts": texts}, open(P("N001_v11_스튜디오_문구.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(OUT, len(doc), "| 후보 파일", len(alts))
