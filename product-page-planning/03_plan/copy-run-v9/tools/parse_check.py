#!/usr/bin/env python3
"""작성자 산출물(W*.md)을 읽어 칸별 문구를 뽑고 글자 수 한도를 기계로 센다.
사용: python3 parse_check.py <런 폴더>   → <런 폴더>/W_pages.json, 한도 초과·빠진 칸을 출력
"""
import json, re, sys, os

RUN = sys.argv[1]
WRITERS = [("W1", "선명"), ("W2", "강렬"), ("W3", "담백")]

# 영역 → {칸: 한도}. 06 본문 세 칸은 합계로 따로 센다.
LIMITS = {
    "03": {1: 12, 2: 12, 3: 20, 4: 20, 5: 11, 6: 11, 7: 11},
    "04": {0: 12, 1: 12, 2: 6, 3: 16, 4: 6, 5: 16, 6: 6, 7: 16, 8: 6, 9: 16},
    "05": {0: 13, 1: 13, 14: 11, 15: 11, 16: 15, 17: 15, 18: 15},
    "06": {1: 10, 2: 10, 3: 20, 7: 20, 11: 20, 15: 20, 19: 20,
           5: 27, 9: 27, 13: 27, 17: 27, 21: 27,
           4: 99, 6: 99, 8: 99, 10: 99, 12: 99, 14: 99, 16: 99, 18: 99, 20: 99, 22: 99},
    "07": {0: 11, 1: 11, 7: 18, 9: 18, 11: 18, 12: 9, 13: 9},
    "08": {1: 11, 2: 11, 3: 20, 4: 20},
    "09": {1: 19, 2: 18, 3: 18},
    "10": {1: 10, 2: 10, 3: 18, 4: 18, 5: 18},
    "11": {0: 11, 1: 11},
    "12": {0: 11, 1: 11},
}
REVIEW_GROUPS = [(4, 5, 6), (8, 9, 10), (12, 13, 14), (16, 17, 18), (20, 21, 22)]


def parse(path):
    pages, extra, cur, sec = {}, {}, None, None
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
                pages[sec][int(m.group(1))] = m.group(2).strip()
        elif cur and line.strip():
            extra[cur].append(line)
    return pages, extra


def main():
    out, problems = {}, []
    for code, name in WRITERS:
        path = os.path.join(RUN, f"{code}_{name}.md")
        if not os.path.exists(path):
            problems.append(f"{code}: 파일 없음")
            continue
        pages, extra = parse(path)
        out[code] = {"이름": name, "칸": pages, "기타": extra}
        for sec, lim in LIMITS.items():
            got = pages.get(sec, {})
            for slot, mx in lim.items():
                if slot not in got or not got[slot]:
                    problems.append(f"{code} {sec}.T{slot}: 비어 있음")
                elif len(got[slot]) > mx:
                    problems.append(f"{code} {sec}.T{slot}: {len(got[slot])}자 > {mx}자 — {got[slot]}")
            if sec == "06":
                for a, b, c in REVIEW_GROUPS:
                    tot = sum(len(got.get(k, "")) for k in (a, b, c))
                    if not 50 <= tot <= 80:
                        problems.append(f"{code} 06 후기(T{a}~T{c}) 합계 {tot}자 (55~75 권장)")
    json.dump(out, open(os.path.join(RUN, "W_pages.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(problems) if problems else "한도 초과·빠진 칸 없음")


if __name__ == "__main__":
    main()
