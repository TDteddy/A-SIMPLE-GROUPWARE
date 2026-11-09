# Tone Model: Toss-Inspired Korean UX Writing

This file distills the public Toss UX writing guide into a reusable model for product copy. It is an analysis, not a reproduction of Toss's source assets.

## North star

Toss-style UX writing sounds like a competent product teammate talking to the user:

- polite, but not ceremonial
- direct, but not cold
- optimistic, but not evasive
- short, but not cryptic
- user-facing, not organization-facing

The voice reduces friction by removing three kinds of distance:

1. **Grammatical distance** — passive voice and nominalizations make events feel abstract.
2. **Social distance** — excessive honorifics make the product feel like an institution.
3. **Cognitive distance** — negative or policy-heavy wording makes users scan less accurately.

## The five pillars

### 1. 해요체 as the baseline

Use `해요체` as the product-wide register. It keeps copy warm and consistent without becoming 반말.

Prefer:

- `확인했어요`
- `보낼게요`
- `필요해요`
- `할 수 있어요`

Avoid as default:

- `확인했습니다`
- `전송됩니다`
- `필요합니다`
- `가능합니다`

`주세요` is still 해요체 and can be useful for direct recovery instructions, but do not overuse it when the copy can name the user's next action more clearly.

### 2. Active agency

Make the sentence show who or what acts.

- Passive/stative: `알림이 설정됐어요`
- Active: `알림을 설정했어요`

The active version is usually shorter and gives the user a clearer sense of completion.

Common replacements:

- `됐어요` → `했어요`, `바꿨어요`, `설정했어요`, `보냈어요`
- `높아졌어요` → `올랐어요`
- `변경됐어요` → `바꿨어요`
- `결제될 예정이에요` → `결제일이에요`, `나가는 날이에요` when appropriate

### 3. Positive-first framing

When a user can proceed after a condition, lead with the condition and the possible action.

- Negative-first: `허락하기 전에는 가입할 수 없어요`
- Positive-first: `허락하면 가입할 수 있어요`

This does not mean hiding restrictions. Use positive framing when it helps the user understand the next path. Use negative framing when the user must understand a hard block.

### 4. Casual honorifics

The product should respect the user without sounding like a bank counter or government form.

Reduce:

- `~시겠어요?` → `~할까요?`
- `시나요?` → `나요?`, `있나요?`, or a subject-led question
- `계시다` → `있다`
- `여쭙다` → `확인하다`, `묻다`
- `께` → `에게`

If removing `시` makes a personal question awkward, rewrite the sentence so the information becomes the subject:

- `어떤 목적으로 대출받으시나요?`
- `대출 목적이 무엇인가요?`

### 5. De-nominalized verbs

Korean product copy often becomes stiff when it stacks nouns or Sino-Korean terms.

Prefer verbs and concrete cause clauses:

- `이자 환불` → `이자를 돌려받기`
- `잔액 부족으로` → `잔액이 부족해서`
- `카드값 결제 예정` → `카드값 나가는 날`

If a noun cannot be naturally converted to a verb, use `{명사}가 {상태/행동}해서` to soften it.

## Exception philosophy

Toss-style writing is not a blind positivity filter. It is a clarity filter.

Allow exceptions when they make the user's decision safer:

- service end and expiry: passive can emphasize the service/period
- consequences: passive can show “if you do X, Y happens”
- privacy/reassurance: passive can reduce perceived blame or agency
- legal/policy blocks: negative wording can prevent false hope
- contextual questions: honorific question endings can feel more natural when using a user's real-world activity or asking for goodwill

## Practical voice checklist

Before shipping copy, ask:

1. Does it sound like a real product teammate would say it?
2. Is the next action obvious within one scan?
3. Did we remove passive voice unless it is a deliberate exception?
4. Did we avoid making the user feel blamed?
5. Did we avoid hiding hard restrictions?
6. Is the shortest version still clear?
7. Are button labels action-specific?
