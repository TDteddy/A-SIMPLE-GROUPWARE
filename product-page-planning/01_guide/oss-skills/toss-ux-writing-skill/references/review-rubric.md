# Review Rubric

Score each item from 0 to 2.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Register | formal/반말 mixed | mostly 해요체 | consistent 해요체 |
| Agency | passive hides action | mixed | active by default, exceptions justified |
| Valence | avoidable negative | mixed | positive-first without hiding restrictions |
| Honorifics | too ceremonial | mildly formal | casual respect |
| Verb clarity | noun-heavy | some noun stacks | verbs and concrete causes |
| Surface fit | generic | usable | tailored to surface and button roles |
| Exception handling | unsafe/unclear | partially justified | clear, explicit, safer than default |

## Verdict

- `12–14`: 좋음 — minor polish only
- `8–11`: 수정 필요 — rewrite before shipping
- `0–7`: 위험 — user may misunderstand, feel blamed, or hit a policy/safety issue

## Severity levels

### Critical

- Hides a legal/policy restriction.
- Positive rewrite makes an unavailable feature sound available.
- Button label causes a destructive action ambiguity.
- Privacy/data-use copy is misleading.

### Major

- Formal register in product UX copy.
- Avoidable passive status in success or CTA copy.
- Negative-first recovery message without next step.
- Over-honorific form question.

### Minor

- Slight noun heaviness.
- CTA can be more action-specific.
- Sentence can be shorter without losing meaning.

## Audit output template

```markdown
## Verdict: 수정 필요

| Severity | Finding | Rule | Suggested rewrite |
|---|---|---|---|
| Major | `설정됐어요` is passive in a success state | Active agency | `설정했어요` |

### Final copy

...
```
