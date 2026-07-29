# Landscape Scanner on Power Automate / AI Builder — options assessment

Assessment of how the [landscape-scanner](https://github.com/trgallagher-research/landscape-scanner)
engine could be implemented inside the Microsoft 365 suite, using Power Automate,
AI Builder, Copilot Studio and the SharePoint/Excel connectors.

Written 2026-07-29 against the engine at `src/scanner/` and the platform limits
current at that date. The tenant evidence comes from
`../collective-innovation-http-mapping/`, which captured a working IB flow that
already uses Microsoft Forms, an AI Builder **Run a prompt** action with
structured output, and the SharePoint connector.

Companion document: [`capability-map.md`](capability-map.md) — the component-by-component
mapping with exact platform limits.

## The question this has to answer

The scanner is not valuable because it summarises search results. It is valuable
because of four guarantees, and any port has to be judged on whether it keeps them:

1. **Anchor-constrained extraction.** The model may only *select* text spans that
   appear verbatim in a scraped page. A span that is not a substring of the source
   is discarded on the spot (`pipeline.py:400`).
2. **Verbatim verification.** Every decision-bearing claim must trace to an exact
   quote, found by deterministic string matching first and only then by a model
   whose proposed span is re-validated as verbatim (`verify.py`).
3. **Quarantine, not deletion.** Entities that cannot be confirmed stay in the
   report, flagged.
4. **No silent fakery.** The run refuses to start without its keys, records which
   providers actually ran, and meters real token spend against a hard, resumable cap.

Guarantees 1, 2 and 4 are the load-bearing ones, and they are load-bearing precisely
because they are *mechanical*. They do not ask a model to behave; they check its
output with string comparison and arithmetic. That property is what a Power Platform
port most threatens, because Power Automate cloud flows have no regular-expression
functions and no fuzzy string matching, and AI Builder bills in credits rather than
in metered tokens against a dollar budget.

## What the platform gives, and what it takes away

Three things work in the platform's favour, and the tenant evidence already proves
two of them.

The **LLM layer transfers cleanly**. AI Builder's *Run a prompt* action runs GPT
models on Azure OpenAI, returns structured output, and exposes `promptTokens` and
`completionTokens` for cost accounting. The existing Collective Innovation flow
consumes exactly this shape — `outputs('Run_a_prompt')?['body/responsev2/predictionOutput/structuredOutput/topics']`
— so schema-validated JSON from a prompt action is proven in this tenant, not
assumed. All eight of the scanner's model tasks are ordinary structured-output
prompts and would port with only prompt-text changes.

The **front door gets better, not worse**. The scanner's weakest edge today is that
it runs on a home server behind a Cloudflare Tunnel with a hand-rolled bearer token,
reachable only through a separate Vercel app. In Microsoft 365 the request form,
per-user identity, run history, stored reports, approvals and Teams notification are
all native and free of bespoke auth code. If the goal is *distribution inside the IB*,
this is a genuine gain rather than a compromise.

Against that, the **search layer has no Microsoft answer that preserves the design**.
Bing Search APIs were retired on 11 August 2025, and the migration path Microsoft
offers is Grounding with Bing Search inside Azure AI Foundry, which is an Azure
platform commitment rather than a drop-in search API and costs materially more.
Copilot Studio can search the web, but it returns a *summarised, grounded answer with
citations* — Microsoft's grounding check, not ours. The scanner needs raw ranked
results with URLs and snippets from two independent indexes, because cross-index
agreement is what powers its high-confidence tier. Nothing in the Microsoft 365 suite
supplies that; it has to come from the generic HTTP connector calling Serper and
Brave, or from a custom connector wrapping them, both of which are premium and both
of which land squarely on the tenant's DLP posture.

And the **deterministic verification layer has to leave the flow**. Power Automate
expressions cannot do regular expressions or fuzzy matching, so sentence splitting,
normalisation of smart quotes and thousands separators, the fuzzy restore threshold
of 92, number extraction for the value-only trap, and the verbatim re-check of a
model-proposed span cannot be written as flow expressions. They can be written in an
Office Script, which is TypeScript and can do all of it — but Office Scripts cannot
make external calls when run from Power Automate (`fetch is not defined`), are capped
at 1,600 script runs per user per day, and share the 120-second synchronous timeout.
They would work as a pure text-processing function called with the page text and the
claims, which is exactly the shape `verify.py` already has.

## Load, measured against the limits

At default configuration — 30 search queries, a 25-entity shortlist, 3 pages scraped
per entity — one scan costs roughly 60 search API calls, 75 page fetches, and between
120 and 240 model calls, of which about 75 are span discovery over 15,000 characters
of page text each. Against the platform that means:

| Constraint | Limit | Assessment |
|---|---|---|
| Actions per flow definition | 500 | Requires splitting into a parent plus 3–4 child flows |
| Synchronous HTTP timeout | 120 s | Adequate; the scraper's own timeout is 20 s, 35 s on the reader rung |
| Apply-to-each items | 100,000 | Not a constraint |
| Maximum run duration | 30 days | Not a constraint |
| Office Script runs | 1,600 per user per day | Binding if called per claim; batch to one call per entity (~25 per scan) |
| AI Builder prompt runs | Throttled, credit-metered | The real cost and throughput question — see below |

The credit question is the one with a date on it. Seeded AI Builder credits are
removed for all customers on 1 November 2026, after which AI Builder consumption
requires Copilot Credits or an active add-on. A design that puts 120–240 prompt runs
through AI Builder per scan needs that licensing answered before it is built, not after.

## The options

### A. Full port — the whole pipeline in Power Automate and AI Builder

Every stage rebuilt as flows: HTTP calls to Serper and Brave for discovery, HTTP GETs
for scraping, AI Builder prompts for the eight model tasks, an Office Script for the
deterministic verification core, SharePoint lists for resumable stage state, and a
composed HTML report written to a document library.

This is achievable and it is the only option that is genuinely "in the O365 suite".
It is also the most expensive to build and the most fragile to own. The verification
core survives only by being exiled to an Office Script, which means the guarantee that
makes the scanner trustworthy now depends on a script attached to a workbook, subject
to a per-user daily quota, that no longer has a test suite around it. The scanner's
current offline test suite covers exactly this logic; none of it transfers.

Two further losses are worth naming plainly. The budget meter becomes approximate:
token counts are available, but AI Builder bills credits, so the honest "$0.55 for this
run" line in the report becomes a credit estimate. And PDF text extraction disappears —
institutional sources such as OECD and World Bank publications are PDF-first, and there
is no connector that extracts text from a fetched PDF, so a meaningful share of sources
would degrade to `unreachable`.

### B. Thin front end — Microsoft 365 drives the existing engine

Power Automate does no scanning. A Microsoft Form or Power App captures the question
and budget, a flow calls the existing token-authenticated `serve-api`, polls for
completion, stores the returned HTML report in SharePoint, and notifies the requester
in Teams. Every guarantee is preserved unchanged, because the engine is unchanged.

This is by far the cheapest to build — a handful of actions against an API that already
exists — and it is the only option where the verification logic keeps its test suite.
Its blocker is not technical but governance: it points an IB tenant flow at a personal
home server on a personal domain, using personal API keys. That is fine as a
demonstration and hard to defend as an IB service. Moving the engine to IB-controlled
infrastructure removes the objection and turns this into option E.

### C. Split by trust boundary — orchestration in the platform, verification in code

Power Automate owns the funnel, the UI, the storage and the model calls. Everything
mechanical — the verbatim span filter, exact and fuzzy restoration, the value-only
check, the re-validation of a model-proposed span — runs in one deterministic
component called once per entity.

The interesting question is what that component is. As an Office Script it is option A's
compromise. As a Dataverse low-code plug-in it gains Power Fx's `IsMatch`/`Match`
functions and proper regular expressions, at the cost of a Dataverse licence. As an
Azure Function it is the existing Python `verify.py` lifted verbatim, tests and all,
behind a custom connector.

That last variant deserves attention: it keeps the accuracy heart as reviewed, tested
Python, puts everything else on the platform, and confines the Azure footprint to one
small stateless function. It is the best available answer to "how much of this can be
Microsoft 365 without breaking the thing that makes it worth having".

### D. Copilot Studio agent

A conversational agent with web search enabled, plus a Power Automate tool to write
findings to SharePoint. Fastest to something demonstrable, and comfortably the best
user experience.

It also abandons the design. Copilot Studio's generative answers summarise Bing results
and apply Microsoft's own grounding and provenance checks; the agent never handles the
raw source text, so anchor-constrained extraction cannot be enforced, claims cannot be
matched against a scraped page, and no entity can be quarantined on evidence. What comes
out is a well-cited chatbot answer about a landscape. That is a legitimate product, but
it is the product the scanner was built to be distinguishable from, and it should not be
presented internally as a port of it.

### E. Azure AI Foundry, surfaced through Microsoft 365

The engine runs as-is in Azure — Container Apps or Functions — using Grounding with
Bing Search or the existing Serper and Brave keys held in Key Vault. Power Automate,
Teams and SharePoint provide the front end, exactly as in option B.

This is the honest answer to "keep the guarantees and put it on Microsoft
infrastructure the IB can own". It is not the Microsoft 365 suite, and it needs an Azure
subscription, a resource owner and a budget line. But no guarantee is lost, the Python
test suite still runs, and the governance objection to option B disappears.

## Assessment

| Option | Guarantees kept | Build cost | Runtime cost | Main risk |
|---|---|---|---|---|
| A. Full port | 1, 2 weakened; 3 kept; 4 approximate | High | AI Builder credits, premium licences | DLP block on outbound HTTP; PDF sources lost |
| B. Thin front end | All four | Low | Unchanged (~$0.50–2/run) | Governance: IB flow calling a personal server |
| C. Split by trust | All four if the component is code | Medium | Credits plus a small Azure or Dataverse line | Two platforms to own |
| D. Copilot Studio | None of 1, 2, 3 | Low | Copilot licences | Looks like the scanner, is not |
| E. Azure + M365 front end | All four | Medium | Azure hosting plus provider keys | Not "in the O365 suite"; needs a subscription owner |

Two questions decide between these before any build starts, and both are cheap to answer.

**Does the tenant's DLP policy permit the generic HTTP connector to reach non-Microsoft
endpoints?** The Collective Innovation permission matrix already flags this as untested
for `Send an HTTP request to SharePoint`, which is a far milder ask than arbitrary
outbound calls to Serper, Brave and the open web. If the answer is no, options A and C
are dead in their Power-Automate-native forms and the choice collapses to B or E.

**Who pays for AI Builder after 1 November 2026?** A design that puts 120–240 prompt
runs through AI Builder per scan needs a licensing owner. If the answer is nobody, A and
C lose their model layer.

If the goal is to give IB colleagues access to landscape scans, option B or E delivers
that in a fraction of the effort with none of the guarantees weakened, and the Microsoft
365 layer does what it is genuinely good at — identity, request capture, storage,
notification and approval. If the goal is specifically that the *engine* must live in
Power Automate, option C with the verification core kept as tested code is the version
worth building, and option A is the version to expect if that constraint hardens further.

Option D should be built only if it is named as what it is: a Copilot agent that answers
landscape questions, not the landscape scanner.

## Before building anything

Three tests, in this order, each cheap:

1. **DLP probe.** In a copied flow, add an HTTP action with a GET to a public
   non-Microsoft endpoint. A policy block shows at save or run start. This is the
   single most decisive result in the assessment.
2. **AI Builder structured-output probe.** Point a *Run a prompt* action at the
   scanner's `EXTRACT_SYSTEM` prompt with one batch of search results, and confirm the
   structured output validates against `ExtractOutput`. The Collective Innovation flow
   makes this near-certain; confirming it costs ten minutes.
3. **Office Script verification probe.** Port `verify.py`'s `normalise`, `split_sentences`
   and `restore` to TypeScript, call it from a flow with one page of text and five claims,
   and check the verdicts match the Python engine on the same input. This measures how
   much of the accuracy heart really survives the platform, which is the question the
   whole assessment turns on.

## A note on lanes

The scanner sits in the personal-research lane: the `trgallagher-research` org, personal
provider keys, MIT-licensed and public. Implementing it in the IB tenant moves it into the
IB lane, with IB ownership, IB data handling and IB licensing. That is a decision about
whose tool this is rather than a technical detail, and it is worth taking deliberately
rather than as a by-product of choosing a platform.
