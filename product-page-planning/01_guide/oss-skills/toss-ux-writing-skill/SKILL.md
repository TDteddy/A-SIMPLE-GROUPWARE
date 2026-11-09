---
name: toss-ux-writing
description: Use when rewriting or reviewing Korean product UX copy in a Toss-inspired voice: 해요체, active wording, positive framing, casual honorifics, de-nominalized verbs, and precise exception handling for errors, benefits, policies, forms, dialogs, buttons, and notifications.
category: writing
risk: safe
source: custom
source_url: https://developers-apps-in-toss.toss.im/design/ux-writing.html
metadata:
  triggers:
    - 토스 말투
    - Toss UX writing
    - 한국어 UX 카피
    - 해요체
    - 에러 메시지 문구
    - 버튼 라벨
    - 혜택 안내
    - 앱 문구 리뷰
  languages: [ko]
  output_contract: rewrite-table-or-copy-pack
---

# Toss UX Writing

Use this skill to generate, rewrite, or review Korean product microcopy in a Toss-inspired style. The goal is not to impersonate Toss or copy its source examples; the goal is to apply reusable patterns: friendly 해요체, active verbs, positive-first framing, casual respect, and clear exceptions.

## Core contract

When improving Korean UX copy:

1. **Use 해요체 everywhere.** Avoid formal `합니다/됩니다/하십시오` and avoid 반말.
2. **Prefer active wording.** Make the user, product, or object do the action instead of relying on `되다/됐어요/되어요`.
3. **Frame positively first.** Say what the user can do and under what condition before saying what is blocked.
4. **Keep honorifics casual.** Remove over-formal `~시겠어요`, `시나요`, `셨나요`, `께`, `계시다`, `여쭙다` unless an exception applies.
5. **De-nominalize.** Replace stiff `{noun}+{noun}` and Sino-Korean nouns with verbs, causes, and concrete actions.
6. **Respect exceptions.** Do not force positivity or active voice when legal/policy clarity, user reassurance, service end/expiry, or consequence explanation needs a passive or negative sentence.

## Workflow

### 1. Classify the surface

Identify where the copy appears:

- Button or CTA
- Dialog / confirmation
- Toast / snack bar
- Error / recovery message
- Empty state
- Form label, helper text, validation
- Benefit eligibility or reward 안내
- Policy/legal restriction
- Notification/push
- Privacy, consent, recording, data use

Use `references/surface-patterns.md` for surface-specific defaults.

### 2. Rewrite with the five primary transforms

Apply transforms in this order:

1. **Register:** convert to 해요체.
2. **Agency:** convert passive/stative phrasing to active wording.
3. **Valence:** convert avoidable negatives to possible conditions.
4. **Distance:** lower honorific altitude while preserving respect.
5. **Verbs:** turn noun stacks into verbs or cause clauses.

Use `references/vocabulary.md` for replacement patterns.

### 3. Check exception gates

Before finalizing, ask:

- Is this a hard legal/policy/product restriction? If yes, negative wording may be clearer.
- Is this about service 종료, 기간 만료, 연체, 해지, 적용, 기록, 녹음, or 정보 수집? If yes, passive wording may be clearer.
- Is the question using the user's real context, inferred situation, or asking for goodwill/opinion? If yes, `시나요/셨나요` may be allowed.
- Could positive wording make the user misunderstand that the whole service is unavailable? If yes, specify the affected benefit/function.

Use `references/decision-tree.md`.

### 4. Return an auditable result

For rewrites, return this table:

| 원문 | 개선안 | 적용 규칙 | 예외 여부 |
|---|---|---|---|

For generation tasks, group by surface:

1. Primary copy
2. Secondary/helper copy
3. CTA labels
4. Error/empty/recovery copy if relevant
5. Notes on risk, exception, or missing context

For audits, return:

1. Overall verdict: `좋음`, `수정 필요`, or `위험`
2. Findings by severity
3. Suggested rewrite
4. Rule references

## Hard rules

- Do not output `되어요`; use `돼요` if passive is intentionally allowed.
- In dialogs, prefer left button `닫기` over `취소` unless the action truly cancels a user-initiated operation.
- Avoid generic CTAs like `확인`, `진행`, `제출` when the action can be named.
- Do not blame the user. Prefer system/product constraints and next steps.
- Do not hide policy/legal restrictions behind cheerful wording.
- Do not claim generated copy is “official Toss copy.”
- Do not redistribute or quote the full Toss guide. Summarize patterns and cite the source when needed.

## Quick patterns

```text
카드를 해지하시겠어요?      → 카드를 해지할까요?
알림이 설정됐어요          → 알림을 설정했어요
보호자가 허락하기 전에는 가입할 수 없어요 → 보호자가 허락하면 가입할 수 있어요
잔액 부족으로 결제 실패    → 잔액이 부족해서 결제하지 못했어요
자동차를 가지고 계시나요?  → 자동차가 있나요?
```

## When to Use

- Korean app/web product copy needs a Toss-like tone.
- UX writing for errors, dialogs, buttons, benefits, onboarding, forms, notifications, or policy 안내 feels stiff.
- A PR adds Korean UI strings and needs a style review.
- You need multiple variants in friendly 해요체.
- You need to explain why a Korean phrase feels too formal, passive, negative, or noun-heavy.

## When Not to Use

- Legal terms must be reproduced verbatim.
- The brand voice intentionally uses formal `합니다체`.
- The audience requires institutional or government-style honorifics.
- The copy is not Korean.
- You are asked to clone Toss's proprietary UI or copy full official examples.

## References

- `references/tone-model.md` — deep analysis of the voice model.
- `references/decision-tree.md` — exception-first decision gates.
- `references/vocabulary.md` — replacement patterns and anti-patterns.
- `references/surface-patterns.md` — UI surface-specific copy recipes.
- `references/examples.md` — synthetic before/after examples.
- `references/review-rubric.md` — scoring rubric for audits.
- `scripts/toss_style_lint.py` — local heuristic linter.
