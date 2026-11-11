#!/usr/bin/env python3
"""v9 기획안 문서를 조립한다.
사용: python3 build_doc.py <런 폴더> <출력 md>
읽는 것: v9_틀.md, W_pages_최종.json(없으면 W_pages.json), C_공통칸.json, tools/studio_defaults.json,
        끝부분 조각 파일 S_검수.md / S_대조.md / S_기본안.md / S_확인.md / S_부록.md (있으면 넣는다)
"""
import json, os, re, sys

RUN, OUT = sys.argv[1], sys.argv[2]
J = lambda n: json.load(open(os.path.join(RUN, n), encoding="utf-8"))
D = J("tools/studio_defaults.json")
C = J("C_공통칸.json")
W = J("W_pages_최종.json") if os.path.exists(os.path.join(RUN, "W_pages_최종.json")) else J("W_pages.json")
ORDER = [("W1", "선명"), ("W2", "강렬"), ("W3", "담백")]

# 영역 → [(행 이름, [칸...], 이어 붙이는 방식)]
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


def esc(s):
    return s.replace("|", "\\|")


def join(texts, slots, sep):
    return esc(sep.join((texts.get(str(k)) or texts.get(k) or "").strip() for k in slots))


def wtexts(code, sec):
    return {int(k): v for k, v in W.get(code, {}).get("칸", {}).get(sec, {}).items()}


def table_T(sec):
    dflt = {i: t for i, t in enumerate(D[sec]["texts"])}
    rows = ["| 자리 | 기본 | 선명 | 강렬 | 담백 |", "|---|---|---|---|---|"]
    if sec == "06":
        rows.append("| 제목 (T1 / T2) | " + join(dflt, [1, 2], " / ") + " | " +
                    " | ".join(join(wtexts(c, sec), [1, 2], " / ") for c, _ in ORDER) + " |")
        for n, (who, a, b, c_) in enumerate(REVIEWS, 1):
            def rv(t):
                body = f"{(t.get(a) or '').strip()} **{(t.get(b) or '').strip()}** {(t.get(c_) or '').strip()}"
                return esc(f"`{(t.get(who) or '').strip()}`<br>{body}")
            rows.append(f"| 후기 {n} (T{who}~T{c_}) | " + rv(dflt) + " | " + " | ".join(rv(wtexts(c, sec)) for c, _ in ORDER) + " |")
        return "\n".join(rows)
    for name, slots, sep in UNITS[sec]:
        rows.append(f"| {name} | " + join(dflt, slots, sep) + " | " +
                    " | ".join(join(wtexts(c, sec), slots, sep) for c, _ in ORDER) + " |")
    return "\n".join(rows)


def table_C(sec):
    dflt = D[sec]["texts"]
    cur = C.get(sec, {})
    rows = ["| 칸 | 기본 | 이번 문구 |", "|---|---|---|"]
    for k in sorted(cur, key=int):
        base = dflt[int(k)]
        mark = "(그대로)" if base.strip() == cur[k].strip() else esc(cur[k])
        rows.append(f"| T{k} | {esc(base)} | {mark} |")
    extra = C.get(sec + "_추가행", {})
    out = "\n".join(rows)
    for group, items in extra.items():
        out += f"\n\n스튜디오에서 행을 늘려 넣는 것 — {group}\n\n"
        if items and isinstance(items[0], list):
            out += "| 항목 | 내용 |\n|---|---|\n" + "\n".join(f"| {esc(a)} | {esc(b)} |" for a, b in items)
        else:
            out += "\n".join(f"- {x}" for x in items)
    return out


def piece(name):
    p = os.path.join(RUN, name)
    return open(p, encoding="utf-8").read().strip() if os.path.exists(p) else ""


doc = open(os.path.join(RUN, "v9_틀.md"), encoding="utf-8").read()
doc = re.sub(r"<<T:(\d{2})>>", lambda m: table_T(m.group(1)), doc)
doc = re.sub(r"<<C:(\d{2})>>", lambda m: table_C(m.group(1)), doc)
for tok, f in [("<<REVIEW>>", "S_검수.md"), ("<<CHECK12>>", "S_대조.md"), ("<<DEFAULTS>>", "S_기본안.md"),
               ("<<CONFIRM>>", "S_확인.md"), ("<<APPENDIX>>", "S_부록.md")]:
    doc = doc.replace(tok, piece(f))
doc = re.sub(r"\n{3,}", "\n\n", doc).rstrip() + "\n"
open(OUT, "w", encoding="utf-8").write(doc)
print(OUT, len(doc))
