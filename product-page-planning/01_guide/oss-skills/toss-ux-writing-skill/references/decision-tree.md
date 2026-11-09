# Decision Tree

Use this decision tree before rewriting Korean product copy.

## 0. Is the text product UX copy?

If it is legal boilerplate, a contract quote, a regulatory phrase, or customer support policy that must be exact, do not rewrite the legally binding text. You may add a user-facing summary around it.

## 1. Register gate: 해요체

- If the copy uses `합니다/됩니다/가능합니다/하십시오`, convert to 해요체.
- If the copy uses 반말, convert to 해요체.
- If the copy is a brand slogan or legal term, preserve it and add nearby UX explanation if needed.

## 2. Passive gate

### Prefer active when

- The user completed an action.
- The product completed an action for the user.
- The copy is a success state, toast, or simple status.
- The passive verb hides the useful verb.

### Allow passive when

1. **Service end / period expiry**
   - The subject is the service, benefit, period, or deadline.
   - The product needs to emphasize `종료`, `만료`, or similar status.

2. **Consequences that affect the user**
   - The copy explains what happens because of the user's action or inaction.
   - Common verbs: `연체돼요`, `해지돼요`, `적용돼요`, `제한돼요`.

3. **User reassurance / sensitive data handling**
   - The copy explains recording, logging, data use, collection, or visibility.
   - Passive can shift attention from actor to safety outcome.

4. **Conciseness and accuracy**
   - Active wording would be longer or less precise.

Always use `돼요`, not `되어요`.

## 3. Negativity gate

### Prefer positive framing when

- The user can proceed after meeting a condition.
- A benefit is unavailable but the service itself is available.
- The goal is to guide recovery.

Pattern:

```text
[조건]하면 [가능한 행동/혜택]을 할 수 있어요.
```

### Allow negative wording when

1. **Hard policy/legal/product block**
   - The user cannot use a service because of age, law, region, role, eligibility, or product policy.
   - Include the reason.

2. **Only some functions are blocked**
   - Be precise about which function is unavailable.
   - Avoid making the user think the whole product is blocked.

3. **User choice has a consequence**
   - The user is about to change, give up, cancel, or switch something.
   - Negative wording can clarify irreversibility.

4. **Reassurance**
   - `볼 수 없어요`, `기록되지 않아요`, `공유되지 않아요` can calm privacy anxiety.

## 4. Honorific gate

### Prefer casual respect when

- It is a direct product action.
- The question is about a form field.
- The copy is a button, toast, error, or benefit 안내.

Transform:

```text
~하시겠어요? → ~할까요?
~하고 계시나요? → ~하고 있나요? / ~가 있나요?
~께 → ~에게
여쭤볼게요 → 확인할게요 / 물어볼게요
```

### Allow `시나요/셨나요` when

- The product uses a real user context such as location, recent activity, or purchase.
- The product is inferring a user's current situation.
- The product needs the user's goodwill, opinion, or reflection.

Even then, keep the sentence short and avoid stacking multiple honorifics.

## 5. Noun stack gate

If a sentence contains `{noun}+{noun}` or a Sino-Korean nominalization, ask:

- Can the noun become a verb?
- Can the cause become `~해서`?
- Can the user-facing object become the subject?
- Can a stiff financial term be replaced with a familiar noun?

Examples:

```text
잔액 부족으로 → 잔액이 부족해서
이자 환불 → 이자를 돌려받기
정보 입력 → 정보를 입력하기 / 필요한 정보를 알려주기
```

## 6. Button gate

- Prefer action-specific CTA labels: `동의하기`, `업데이트하기`, `계좌 만들기`.
- In dialogs, use left button `닫기` when the secondary action just exits the dialog.
- Use `취소` only when it truly cancels an in-progress operation.

## Final check

If a rewrite is warmer but less precise, reject it. Toss-style copy optimizes for friendly clarity, not cheerfulness alone.
