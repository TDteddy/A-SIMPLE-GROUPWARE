#!/usr/bin/env python3
"""작성자 파일 하나를 스튜디오 템플릿에 실제로 넣어 보고, 한 줄에 안 들어가 꺾이는 칸을 알려 준다.
사용: python3 tools/fit_check.py <런 폴더> <W1|W2|W3>
- 실제 글꼴(Noto Sans KR)로 그려서 기본 문구보다 줄이 늘어난 칸을 찾는다.
- 흐름 글(06 후기 본문, 13·14)은 줄이 늘어도 되므로 빼고 본다.
- 빠진 칸과 흐름 글의 글자 수 한도도 같이 본다.
"""
import json, os, re, subprocess, sys, tempfile

RUN, CODE = sys.argv[1], sys.argv[2]
SP = "/tmp/claude-0/-home-user-A-SIMPLE-GROUPWARE/cb02de4c-2427-5da5-97fd-829e8871780e/scratchpad"
NAMES = {"W1": "선명", "W2": "강렬", "W3": "담백"}

# 써야 하는 칸
SLOTS = {
    "03": [1, 2, 3, 4, 5, 6, 7],
    "04": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "05": [0, 1, 14, 15, 16, 17, 18],
    "06": [1, 2] + list(range(3, 23)),
    "07": [0, 1, 7, 9, 11, 12, 13],
    "08": [1, 2, 3, 4],
    "09": [1, 2, 3],
    "10": [1, 2, 3, 4, 5],
    "11": [0, 1],
    "12": [0, 1],
}
REVIEW_BODY = [(4, 5, 6), (8, 9, 10), (12, 13, 14), (16, 17, 18), (20, 21, 22)]
FLOW = {("06", k) for g in REVIEW_BODY for k in g}
# 흐름 글·낱말 단위 줄바꿈 칸의 글자 수 한도(공백 포함)
CHAR_MAX = {("04", 3): 16, ("04", 5): 16, ("04", 7): 16, ("04", 9): 16,
            ("07", 7): 18, ("07", 9): 18, ("07", 11): 18,
            ("06", 3): 20, ("06", 7): 20, ("06", 11): 20, ("06", 15): 20, ("06", 19): 20,
            ("06", 5): 27, ("06", 9): 27, ("06", 13): 27, ("06", 17): 27, ("06", 21): 27}


def parse(path):
    pages, sec = {}, None
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^##\s+(\d{2})\b", line)
        if m:
            sec = m.group(1)
            pages.setdefault(sec, {})
            continue
        if re.match(r"^##\s", line):
            sec = None
            continue
        m = re.match(r"^\s*T(\d+)\s*:\s?(.*)$", line)
        if sec and m:
            pages[sec][int(m.group(1))] = m.group(2).strip()
    return pages


path = os.path.join(RUN, f"{CODE}_{NAMES[CODE]}.md")
pages = parse(path)
problems = []
for sec, slots in SLOTS.items():
    for k in slots:
        v = pages.get(sec, {}).get(k, "")
        if not v:
            problems.append(f"{sec}.T{k}: 비어 있음")
        elif (sec, k) in CHAR_MAX and len(v) > CHAR_MAX[(sec, k)]:
            problems.append(f"{sec}.T{k}: {len(v)}자 > {CHAR_MAX[(sec, k)]}자 — {v}")
    if sec == "06":
        for a, b, c in REVIEW_BODY:
            tot = sum(len(pages.get(sec, {}).get(x, "")) for x in (a, b, c))
            if not 50 <= tot <= 78:
                problems.append(f"06 후기 본문(T{a}~T{c}) 합계 {tot}자 — 55~75자로")

common = json.load(open(os.path.join(RUN, "C_공통칸.json"), encoding="utf-8"))
texts = {s: dict(v) for s, v in common.items() if s.isdigit()}
for sec, d in pages.items():
    texts.setdefault(sec, {})
    for k, v in d.items():
        texts[sec][str(k)] = v
for a, b, c in REVIEW_BODY:
    r = texts.get("06", {})
    if str(a) in r:
        r[str(a)] = r[str(a)].rstrip() + " "
    if str(c) in r:
        r[str(c)] = " " + r[str(c)].lstrip()

tmp = tempfile.mkdtemp(prefix="fit_", dir=os.path.join(SP, "v9"))
tj = os.path.join(tmp, "texts.json")
json.dump(texts, open(tj, "w", encoding="utf-8"), ensure_ascii=False)
r = subprocess.run(["node", os.path.join(SP, "v9", "render2.js"),
                    os.path.join(SP, "live", "detail-studio-v2", "template.js"), tmp, tj],
                   capture_output=True, text=True, timeout=300)
fit = json.load(open(os.path.join(tmp, "fit.json"), encoding="utf-8"))
for w in fit["wraps"]:
    sec, k = w["sec"], int(w["key"])
    if sec in ("13", "14") or (sec, k) in FLOW:
        continue
    if sec in SLOTS and k in SLOTS[sec]:
        problems.append(f"{sec}.T{k}: 한 줄에 안 들어가 {w['baseLines']}줄 → {w['lines']}줄로 꺾임 — {w['text']}")
print("\n".join(problems) if problems else "모든 칸이 템플릿에 들어갑니다.")
print(f"(그린 화면: {tmp}/s03.png … s12.png)")
