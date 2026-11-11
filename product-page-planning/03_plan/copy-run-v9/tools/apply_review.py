#!/usr/bin/env python3
"""검수 결과와 되돌림 재작성을 문구에 반영한다.
사용: python3 apply_review.py <런 폴더>
읽는 것: W_pages.json, N_검수.json(손봄만 반영), W1_되돌림.md … (있으면 그 칸을 덮어쓴다), N_재검수.json(있으면 손봄 반영)
쓰는 것: W_pages_최종.json, C_공통칸.json(공통 칸 손봄), 반영 내역을 표준 출력으로
"""
import json, os, re, sys

RUN = sys.argv[1]
P = lambda n: os.path.join(RUN, n)
W = json.load(open(P("W_pages.json"), encoding="utf-8"))
C = json.load(open(P("C_공통칸.json"), encoding="utf-8"))
log = {"손봄": 0, "아니오": 0, "되돌림 반영": 0, "공통 손봄": 0}
no_items = []


def slot_of(s):
    return str(int(re.sub(r"\D", "", str(s))))


def apply_items(items, label):
    for it in items:
        who, sec, key, verdict = it["대상"], it["영역"], it["칸"], it["판정"]
        if verdict == "아니오":
            log["아니오"] += 1
            no_items.append(it)
            continue
        if verdict != "손봄" or not it.get("수정"):
            continue
        if who == "공통":
            if sec in C and str(key) in C[sec]:
                C[sec][str(key)] = it["수정"]
                log["공통 손봄"] += 1
            else:
                print("공통 칸을 찾지 못함:", sec, key, "→ 직접 확인")
            continue
        k = slot_of(key)
        W[who]["칸"].setdefault(sec, {})[k] = it["수정"]
        log["손봄"] += 1


for name in ("N_검수.json", "N_재검수.json"):
    if os.path.exists(P(name)):
        apply_items(json.load(open(P(name), encoding="utf-8")).get("items", []), name)
        if name == "N_검수.json":
            # 되돌림 재작성은 1차 검수 뒤, 재검수 앞에 반영한다
            for code, w in W.items():
                f = P(f"{code}_되돌림.md")
                if not os.path.exists(f):
                    continue
                sec = None
                for line in open(f, encoding="utf-8"):
                    m = re.match(r"^##\s+(\d{2})\b", line)
                    if m:
                        sec = m.group(1)
                        continue
                    if re.match(r"^##\s", line):
                        sec = None
                        continue
                    m = re.match(r"^\s*T(\d+)\s*:\s?(.*)$", line)
                    if sec and m and m.group(2).strip():
                        w["칸"].setdefault(sec, {})[str(int(m.group(1)))] = m.group(2).strip()
                        log["되돌림 반영"] += 1

json.dump(W, open(P("W_pages_최종.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(C, open(P("C_공통칸.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(log)
for it in no_items:
    print(f"아니오 {it['대상']} {it['영역']}.{it['칸']}: {it['원문']} — {it['사유']}")
