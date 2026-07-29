# Capability map — scanner component → Power Platform equivalent

Component-by-component mapping of the landscape-scanner engine onto Microsoft 365,
with the platform limit that governs each. Supports the options in
[`README.md`](README.md). Source references are to
`trgallagher-research/landscape-scanner` at 2026-07-29.

Status key: **direct** — a native equivalent exists; **workaround** — achievable with
a named compromise; **gap** — no equivalent inside Microsoft 365.

## Pipeline stages

| # | Scanner component | Source | Power Platform equivalent | Status |
|---|---|---|---|---|
| 1 | Frame: question → search queries + segments | `pipeline.py:136` | AI Builder *Run a prompt*, structured output | direct |
| 2 | Discovery: 30 queries × 2 indexes | `search/serper.py`, `search/brave.py` | HTTP (premium) or custom connector to Serper/Brave | **gap** — see below |
| 3 | Entity extraction from result batches | `pipeline.py:178` | *Run a prompt*, batched 25 hits per call | direct |
| 4 | Triage scoring, batched 40 | `pipeline.py:230` | *Run a prompt* + Select/Filter array | direct |
| 5 | Scrape: HTTP GET → visible text | `scrape.py:192` | HTTP (premium) GET; HTML→text has no native action | workaround |
| 6 | Scrape: PDF text extraction | `scrape.py:114` | No connector extracts text from fetched PDF bytes | **gap** |
| 7 | Scrape: reader fallback for JS/bot-walled pages | `scrape.py:230` | HTTP GET to `r.jina.ai` — same DLP question as #2 | workaround |
| 8 | Scrape cache, per URL | `scrape.py:262` | SharePoint list or Dataverse table keyed on URL hash | direct |
| 9 | Span inventory + verbatim filter | `pipeline.py:400` | Office Script substring filter, or nested `contains()` | workaround |
| 10 | Attribute population from spans | `pipeline.py:326` | *Run a prompt*, structured output | direct |
| 11 | Claim verification: exact + fuzzy restore | `verify.py:88` | No regex or fuzzy matching in flows — Office Script | **gap** in-flow |
| 12 | Value-only match rejection | `verify.py:74` | Requires number extraction by regex — Office Script | **gap** in-flow |
| 13 | Passage selection, top-6 lexical | `verify.py:118` | Office Script (token-set similarity) | workaround |
| 14 | Relation check + verbatim re-validation | `pipeline.py:408` | *Run a prompt* + deterministic re-check in Office Script | workaround |
| 15 | Existence test and quarantine | `pipeline.py:349` | Flow expressions and conditions | direct |
| 16 | Confidence banding with basis string | `pipeline.py:424` | Flow expressions, `concat` | direct |
| 17 | Budget meter on real tokens | `budget.py:107` | `promptTokens`/`completionTokens` accumulated in a variable | workaround |
| 18 | Hard resumable budget stop | `budget.py:126` | Terminate action + stage state in SharePoint | workaround |
| 19 | Per-stage resume from disk | `state.py` | SharePoint list or Dataverse rows per stage | direct |
| 20 | Provider manifest | `pipeline.py:519` | Composed object written with the report | direct |
| 21 | Single-file HTML report | `report_html.py` | Compose HTML → create file in a document library | direct |
| 22 | Multi-user auth and request intake | `app/api.py` | Forms / Power Apps / SharePoint — native identity | **better than current** |
| 23 | Progress display | `app/runner.py` | SharePoint list + Power App, or Teams adaptive card | direct |

## The four gaps, in detail

### Web search across two independent indexes (#2)

Bing Search APIs were retired on 11 August 2025. Microsoft's stated migration path is
Grounding with Bing Search inside Azure AI Foundry, which requires an Azure project and
model deployment rather than an API key, and which returns grounded generative answers
rather than a ranked result list.

The options are therefore to call Serper and Brave from the generic HTTP connector
(premium, DLP-sensitive), to wrap them in a custom connector (premium, same DLP
question, better governance and reuse), or to accept Copilot Studio's Bing-backed
generative answers and give up cross-index agreement along with the raw snippets that
triage scores from.

Cross-index agreement is not decorative: `pipeline.py:354` sets
`cross_index = len(candidate.indexes) >= 2`, and `_confidence` only awards the high band
to an entity that is both twice-grounded and twice-indexed. A single-index port silently
caps every entity at medium confidence.

### PDF text extraction (#6)

The scraper extracts text from PDF bytes with PyMuPDF. No Microsoft 365 connector does
this — the available conversions go *to* PDF, not from it. Institutional sources are
PDF-first, so in a native port those URLs fail the fetch ladder and are recorded as
`unreachable`, which is honest but materially reduces coverage on exactly the sources
a landscape scan most wants.

### Deterministic text matching (#11, #12)

Power Automate cloud flows have no regular-expression functions. Power Fx has
`IsMatch`, `Match` and `MatchAll`, but these are reachable from Power Apps and Dataverse
low-code plug-ins, not from cloud-flow expressions. The verification core needs sentence
splitting on punctuation, normalisation of smart quotes, en-dashes and thousands
separators, fuzzy token-sort ratio against a threshold of 92, and numeric extraction —
none of which is expressible in flow functions.

Three homes for this logic, in ascending order of fidelity: an **Office Script**
(TypeScript, full regex, no licence beyond Microsoft 365, but subject to 1,600 script
runs per user per day and no test harness); a **Dataverse low-code plug-in** (Power Fx
regex, needs Dataverse); or an **Azure Function** running the existing `verify.py`
unchanged, with its test suite intact, called through a custom connector.

Dropping fuzzy restoration entirely is worth considering as a deliberate simplification
rather than a loss. Exact matching alone is a *stricter* gate, not a weaker one — it
lowers the yield of verified claims but never admits a claim the fuzzy rung would have
rejected. The value-only check, however, cannot be dropped: it is what stops "the figure
is on the page but the page never says it about this entity", which the engine documents
as the dominant real-world failure mode.

### Cost metering in dollars (#17)

AI Builder exposes `promptTokens` and `completionTokens` per prompt run, so a flow can
accumulate real token counts. It bills in AI Builder credits — and after 1 November 2026,
in Copilot Credits — so the report's measured dollar cost becomes a credit estimate
against a per-tenant capacity rather than a metered spend against a user's budget. The
hard resumable stop is still implementable; the honest cost line is not.

## Platform limits that shape the design

| Limit | Value | Consequence |
|---|---|---|
| Actions per flow definition | 500 | Parent flow plus 3–4 child flows |
| Outbound synchronous HTTP timeout | 120 s | Adequate for the 20 s / 35 s scrape ladder |
| Apply-to-each array items | 100,000 (5,000 on Low) | Not binding |
| Apply-to-each concurrency | 1–50 | Parallel scraping is available and worth using |
| Maximum run duration | 30 days | Not binding |
| Daily action limit | 10k / 200k / 500k by performance profile | Not binding at ~2,000 actions per scan |
| Characters per expression | 8,192 | Binding — page text cannot be manipulated inline |
| Expression evaluation limit | 131,072 characters | Below the 15,000-char page text × several spans in one expression |
| Office Script runs | 1,600 per user per day | Batch to one call per entity, not per claim |
| Office Script parameter size | 28.6 MB | Not binding |
| Office Scripts external calls | Blocked from Power Automate | Verification component cannot fetch; text must be passed in |

## Tenant evidence already in hand

From `../collective-innovation-http-mapping/04-existing-flow/sanitized/`:

- **AI Builder *Run a prompt* with structured output works in this tenant.** The
  captured flow reads `body/responsev2/predictionOutput/structuredOutput/topics`,
  `.../keyFindings` and `.../examples` and maps them with Select actions. Structured
  output is proven, not assumed.
- **Microsoft Forms and SharePoint connectors work**, including a webhook trigger and
  `Create item`.
- **The DLP posture on generic HTTP actions is untested.** The permission matrix records
  test P1 — whether `Send an HTTP request to SharePoint` is DLP-blocked — as unresolved.
  Arbitrary outbound HTTP to Serper, Brave and the open web is a considerably larger ask
  and should be probed before any native design is committed to.
