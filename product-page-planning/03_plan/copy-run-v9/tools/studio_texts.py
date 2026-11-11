#!/usr/bin/env python3
"""작성자 문구 + 공통 칸을 스튜디오 시안의 texts 꼴로 만든다.
사용: python3 studio_texts.py <런 폴더> <출력 폴더>
출력: <출력 폴더>/texts_W1.json … (영역 번호 → {칸 번호: 문구}),
      <런 폴더>/N001_v9_스튜디오_문구.json (세 안을 한 파일에. 스튜디오 시안의 candidates[].texts 에 그대로 들어가는 값)
"""
import json, os, sys

RUN, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
J = lambda n: json.load(open(os.path.join(RUN, n), encoding="utf-8"))
C = J("C_공통칸.json")
W = J("W_pages_최종.json") if os.path.exists(os.path.join(RUN, "W_pages_최종.json")) else J("W_pages.json")
REVIEW_BODY = [(4, 5, 6), (8, 9, 10), (12, 13, 14), (16, 17, 18), (20, 21, 22)]

bundle = {"_설명": "영역 번호(01~14) → 칸 번호 → 문구. 스튜디오 시안 파일에서 그 영역 후보의 texts 에 들어가는 값이다. "
                  "적혀 있지 않은 칸은 템플릿 기본 문구를 쓴다. 06 후기는 칸 사이 띄어쓰기를 문구 안에 넣어 두었다."}
for code, w in W.items():
    texts = {sec: dict(v) for sec, v in C.items() if sec.isdigit()}
    for sec, slots in w["칸"].items():
        texts.setdefault(sec, {})
        for k, v in slots.items():
            texts[sec][str(k)] = v
    r = texts.get("06", {})
    for a, b, c in REVIEW_BODY:
        if str(a) in r:
            r[str(a)] = r[str(a)].rstrip() + " "
        if str(c) in r:
            r[str(c)] = " " + r[str(c)].lstrip()
    json.dump(texts, open(os.path.join(OUT, f"texts_{code}.json"), "w", encoding="utf-8"), ensure_ascii=False)
    bundle[f"{code}_{w['이름']}"] = texts
json.dump(bundle, open(os.path.join(RUN, "N001_v9_스튜디오_문구.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", list(W))
