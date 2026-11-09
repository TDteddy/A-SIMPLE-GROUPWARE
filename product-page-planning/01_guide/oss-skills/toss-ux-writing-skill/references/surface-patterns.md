# Surface Patterns

## Buttons and CTAs

Goal: make the action obvious in 1–3 words.

Default recipe:

```text
[verb stem] + 기
```

Examples:

- `동의하기`
- `업데이트하기`
- `시작하기`
- `계좌 만들기`
- `받지 않고 만들기`

Rules:

- Use `닫기` for a secondary dialog button that simply closes the dialog.
- Avoid `취소` unless it cancels an actual operation.
- Avoid generic `확인` when the action can be named.

## Dialogs and confirmations

Goal: state the decision and consequence clearly.

Structure:

1. Title as a question or consequence.
2. Body explains the condition, risk, or benefit.
3. Primary CTA names the desired action.
4. Secondary CTA uses `닫기` or a precise alternative.

For irreversible or benefit-losing decisions, negative wording is allowed:

```text
한 번 바꾸면 [기존 혜택]은 다시 받을 수 없어요.
```

## Error messages

Goal: explain what happened and what to do next without exposing internals.

Structure:

```text
[사용자 목표]을/를 하려면 [필요 조건]이 필요해요.
[다음 행동]해주세요.
```

Prefer:

- condition + recovery
- plain language
- one primary action

Avoid:

- raw error codes as the headline
- `지금 버전에서는 쓸 수 없어요` without recovery
- blaming the user

## Benefit eligibility

Goal: avoid making the user think the whole service is unavailable when only a specific benefit is unavailable.

If the service is usable but a benefit is not:

- Lead with the benefit the user can still get.
- Specify which benefit is limited and why.
- Avoid headline-only `혜택을 받을 수 없어요`.

Template:

```text
[가능한 혜택]은 받을 수 있어요.
[제한되는 혜택]은 [대상 조건]에게 제공돼요.
```

## Forms and input questions

Goal: ask for the information, not for the user's deference.

Prefer subject-led prompts:

- `대출 목적이 무엇인가요?`
- `신고 이유를 선택해주세요`
- `매달 보험료는 얼마인가요?`

Avoid over-honorific prompts:

- `대출받으시나요?`
- `신고하시나요?`
- `내고 계시나요?`

## Notifications and push

Goal: make the state and timing immediately scannable.

Patterns:

- `곧 만료돼요` for expiry.
- `곧 끝나요` for recurring events or casual time-limited content.
- `오늘까지 내지 않으면 연체돼요` when consequence clarity matters.

Use passive when the status itself is the point.

## Privacy, consent, recording, and data use

Goal: reassure users about control and visibility.

Allowed passive/negative patterns:

- `기록돼요`
- `녹음돼요`
- `볼 수 없어요`
- `기록되지 않아요`

Make the safety boundary concrete:

```text
상담이 끝나면 [대상]도 [정보]를 볼 수 없어요.
```

## Policy and legal restrictions

Goal: be clear, not cheerful.

Use negative wording when a service or feature is unavailable by policy or law.

Template:

```text
[대상/상황]은 [행동]할 수 없어요.
[법/정책/제품 이유] 때문에 제한돼요.
```

Do not rewrite into a positive sentence if it suggests the user might be able to bypass the rule.

## Empty states

Goal: explain absence and suggest a next action.

Template:

```text
아직 [대상]이 없어요.
[행동]하면 여기에서 확인할 수 있어요.
```

Empty states are allowed to use `없어요` because absence is the state, but add a next step if possible.
