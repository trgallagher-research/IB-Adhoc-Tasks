# AI layer — where the generated columns come from

Reference for the nine AI-populated columns. **This layer is unchanged by this
project** — every expression is preserved verbatim from the original flow's
`Create item` (see `04-existing-flow/sanitized/create-item.json`). Documented
here because "preserved verbatim" is not enough for whoever next needs to
change it.

## The chain

```
Compose labelled submission          full labelled text of every raw answer
        ↓  SubmissionText
Run a prompt  (AI Builder)           custom prompt, recordId
        ↓  predictionOutput            b3662383-a782-4915-af95-970e4c2b1cca
        ├── text                     → FullAIOutput  (raw JSON, audit trail)
        └── structuredOutput
             ├── summary             → AISummary
             ├── humanReviewRequired → HumanReviewRequired  (Boolean column)
             ├── humanReviewReason   → HumanReviewReason
             └── 7 arrays            → one Select action each → join with \n
```

## Where the prompt itself lives

**Not in the flow.** The flow passes only the input text; the prompt's
instructions and its output schema are stored in AI Builder
(Power Platform → AI hub → Prompts), referenced by the `recordId` above.

The flow *does* contribute prompt context: the labelled text includes the
rating-scale explainer ("1 = Strongly disagree … A score of 3 means neither
agree nor disagree… If a rating conflicts with its accompanying comments,
identify the inconsistency and recommend human review"). That text is part of
`compose-labelled-submission.txt` and therefore versioned in this repo — but
the surrounding instructions are not.

To change what the AI produces, edit the AI Builder prompt. To change what it
is told about the submission, edit the labelled-submission template.

## The seven array columns

Each array holds objects with a **different** property name, so each Select
picks a different key. Property names evidenced from `FullAIOutput` on live
items:

| Column | structuredOutput array | Select expression | Joined with |
|--------|------------------------|-------------------|-------------|
| `Topics` | `topics` | `item()?['topic']` | newline |
| `KeyFindings` | `keyFindings` | `item()?['finding']` | newline |
| `Examples` | `examples` | `item()?['example']` | newline |
| `OpenQuestions` | `openQuestions` | `item()?['question']` | newline |
| `DifferentPerspectives` | `differentPerspectives` | `item()?['perspective']` | newline |
| `ClaimsToVerify` | `claimsToVerify` | `item()?['claim']` | newline |
| `RelatedKnowledge` | `relatedKnowledge` | `item()?['relationship']` | newline |

The join is `join(body('Select_<name>'), decodeUriComponent('%0A'))` —
`decodeUriComponent('%0A')` is how a literal newline is expressed in a Power
Automate expression.

Three of the eight Select actions were captured by Peek code
(`Select_Topics`, `Select_Key_Findings`, `Select_Examples`); the other five are
evidenced by the `join(body('Select_…'))` references in `Create item` and
follow the identical pattern. Non-blocking, because the layer is preserved
rather than rebuilt — capture them only if the AI layer is ever reworked.

## The three direct columns

| Column | Source | Notes |
|--------|--------|-------|
| `AISummary` | `structuredOutput/summary` | plain string |
| `HumanReviewRequired` | `structuredOutput/humanReviewRequired` | Boolean column; the AI returns a real JSON boolean. Column default is No |
| `HumanReviewReason` | `structuredOutput/humanReviewReason` | plain string |
| `FullAIOutput` | `predictionOutput/text` | the complete raw JSON — the audit trail, and the place to look when a Select returns unexpected results |

## Boundary rules that still apply

- AI output **never** writes to a raw-answer column. The two layers share no
  destinations.
- The AI never sees SharePoint — only the labelled text.
- `PromptVersion` is a hand-maintained constant (`Knowledge Submission
  Analyser v1`, trailing newline included). **If the AI Builder prompt is
  edited, bump this string** — nothing does it automatically, and it is the
  only record of which prompt produced a given item.

## If an AI column comes back empty

Look at `FullAIOutput` on that item first:

- raw JSON present but a column empty → the array property name changed in the
  prompt's schema, so the matching Select found nothing. Fix the Select.
- raw JSON absent or malformed → the AI Builder prompt failed or returned
  non-JSON. Nothing downstream can recover it; re-run the submission.
