# Project Notes

Working notes for the team: schedule, prediction record, and AI usage log.
See [README.md](README.md) for the service itself and repo structure.

- [Schedule](#schedule)
- [Prediction Record](#prediction-record)
- [AI Tool Usage](#ai-tool-usage)

---

## Schedule

Due **Fri 9 Oct 2026, 2359**. Working backwards from that date, two deadlines
carry the whole schedule and are non-negotiable — everything else depends on
them:

- **Mon 29 Sep — freeze.** Golden set + prediction record committed. Nothing
  after this date can be edited; the commit history is our evidence they
  predate any measurement.
- **Fri 2 Oct — measurement done.** Week 6 is writing only. No room for reruns
  after this.

### Deadlines

| Who | Deliverable | Deadline |
| --- | --- | --- |
| Haidar | Confirm SUT machine + RAM, tell Megan (caps her model choices) | Wed 24 Sep |
| Wen Jun + Raffael | Labelling protocol written | Wed 24 Sep |
| Wen Jun + Raffael | Both sheets labelled independently | Fri 25 Sep |
| Megan | Candidate models picked, pinned (tag + digest), justified | Fri 25 Sep |
| Peng Jie | Workload model draft | Fri 25 Sep |
| Wen Jun + Raffael | Disagreements resolved, agreement stat computed, protocol updated | Sun 28 Sep |
| Megan | Prediction record drafted, others' sections filled in | Sun 28 Sep |
| **Everyone** | **Golden set + prediction record committed — freeze, no edits after** | **Mon 29 Sep** |
| Haidar + Peng Jie | JMeter load tests done — 3 runs/config, open-loop | Fri 2 Oct |
| Haidar | Stress test done | Fri 2 Oct |
| Raffael + Megan | Accuracy tests + confusion matrices done | Fri 2 Oct |
| Everyone | Recommendation drafted, 12 slides built | Wed 7 Oct |
| Everyone | Deck reviewed, gaps checked against requirements | Thu 8 Oct |
| **Everyone** | **Submit `Group05.pptx` + supporting files on xSiTe** | **Fri 9 Oct, 2359** |

Role owners: see the team table in [README.md](README.md#team).

### If something slips

Flag it in the group chat as soon as it's clear, not at the deadline. A
slipped labelling deadline pushes the freeze; a slipped freeze eats into
measurement time, which cannot be recovered once Week 6 starts. Raise it
early — there's no slack built into this schedule to absorb a late catch.

---

## Prediction Record

**Status: DRAFT — not yet frozen**

This section must be committed before our first benchmark run, together with
the golden test set. Once committed as final it cannot be revised. The commit
history is our evidence that these predictions predate the measurements.

Target freeze: **Mon 29 Sep 2026**

Marks are awarded for specificity, and for the quality of our later account of
where we were wrong — not for being right. A prediction that cannot fail earns
nothing. Commit to numbers, not to directions.

Rule of thumb for each claim below: could someone read our results table and
say "that was wrong"? If not, it needs a number.

### Test machines

We all have different machines, so every latency and throughput figure in this
section and in the final deck refers to **one designated machine** — the
system under test. Numbers measured on anyone else's machine are not
comparable and must not be mixed into the results.

| Role | Owner | Hardware | OS |
| --- | --- | --- | --- |
| **System under test** (service + Ollama + Postgres) | Haidar (desktop) | AMD Ryzen 5 7500F (6C/12T), 32 GB RAM | Windows 11 Pro |
| **Load generator** (JMeter) | Haidar (laptop) | AMD Ryzen 5 7535HS (6C/12T), 32 GB RAM | Windows 11 Pro |

The two must be different machines — a co-hosted load generator steals CPU from
the service and produces latency numbers that will not be accepted as evidence.

Everyone else's machines are for development only. Dev anywhere; measure only
on the SUT.

What this does and does not constrain:

- **Latency, throughput, stress** — SUT only. Hardware-bound.
- **Accuracy** — much less hardware-sensitive (same model, same prompt,
  `temperature: 0`), so this work can be split across the team. Still record
  which machine produced each accuracy run.

#### Anchor measurement

One measured data point from the baseline smoke test, for scaling the latency
estimates. Re-measure on the SUT once it is chosen and replace this row.

| Model | Machine | Narrative length | Latency |
| --- | --- | --- | --- |
| `llama3.2:1b` | Apple M3, 8 cores, 16 GB, macOS 26.5.2 (Wen Jun) | ~120 chars | ~2.6 s |

Everything else below is a guess made before measuring.

### 1. Bottleneck under load

Where do we expect the system to saturate first, and why?

Name the component, the load at which it gives way, and what the other
components are doing at that moment. Say what we expect to observe, not just
what we expect to be true.

> _Replace this. Example of the required specificity:_
> _"Ollama's CPU inference saturates first. At an arrival rate of 2 tickets/sec,_
> _all 8 cores sit near 100% and p95 latency for POST /tickets exceeds 10 s,_
> _while the FastAPI process stays under 15% CPU and Postgres under 5%. Reason:_
> _each classification is a full forward pass over roughly 200 tokens, and_
> _Ollama serialises requests per loaded model, so concurrent requests queue_
> _rather than overlap."_

**Our prediction:**

TBD

**Reasoning:**

TBD

### 2. Per-model predictions

One row per candidate model. Fill in before any model runs against the golden
set.

Accuracy is overall accuracy on our golden set. Latency is single-request
`POST /tickets`, unloaded, **on the designated SUT** — not on whichever machine
happens to be handy.

| Model (tag) | Size class | Expected accuracy | Expected p50 latency | Basis for the estimate |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD % | TBD s | TBD |
| TBD | TBD | TBD % | TBD s | TBD |
| TBD | TBD | TBD % | TBD s | TBD |
| TBD | TBD | TBD % | TBD s | TBD |
| TBD | TBD | TBD % | TBD s | TBD |

Pin each model by exact tag and digest here once chosen (`ollama show <tag>`):

```
TBD
```

### 3. Hardest categories

Which of the seven categories do we expect the models to get wrong most often,
and which categories will they be confused with?

Predict the direction of the confusion, not just that confusion exists — name
the true category and the predicted category, and give a rough rate.

The seven categories: Credit reporting · Debt collection · Mortgage ·
Credit card · Bank account or service · Consumer loan · Money transfer or service

> _Replace this. Example of the required specificity:_
> _"Debt collection is the hardest. We expect over 20% of true Debt collection_
> _tickets to be predicted as Credit reporting, because those narratives_
> _typically mention the debt appearing on the complainant's credit report, so_
> _the surface vocabulary overlaps heavily. Second hardest: Consumer loan_
> _predicted as Credit card, since both describe instalment and revolving_
> _credit in similar terms."_

**Hardest category:**

TBD

**Second hardest:**

TBD

**Categories we expect to be easy, and why:**

TBD

### After the measurements

Do not edit anything above this line once frozen. Record the comparison here,
and carry it onto Slide 11.

| Prediction | Actual | Off by | Why we think we were wrong |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

---

## AI Tool Usage

The assignment brief permits and expects AI coding tools: *"AI coding tools are
permitted and expected throughout. The build is a few hours' work with an agent,
and that is accepted."*

It also draws the line clearly: *"an agent will not label your test data, run
your load tests, or make your recommendation. The assessment targets
measurement, interpretation, and judgement."*

This section records what was done with AI assistance and what was not, so the
division is auditable. Add to it as the project goes.

**Tool used:** Claude Code (Claude Opus 5 / Claude Sonnet 5), Anthropic.

### Log

**22 Sep 2026 — Baseline service scaffold.** Commit `c6cedbf`.

- Read the assignment brief and extracted the System Under Test requirements.
- Scaffolded the triage service: FastAPI app with `POST /tickets`,
  `GET /search`, `GET /stats`, `GET /health`; SQLAlchemy models against
  Postgres; synchronous Ollama client; per-request logging.
- Wrote `Dockerfile` and `docker-compose.yml` wiring service + Postgres +
  Ollama.
- Verified end to end: `docker compose up --build`, pulled `llama3.2:1b`,
  posted a test narrative, confirmed correct classification (~2.6 s), storage
  in Postgres, and that `/stats` and `/search` reflected the result.

Decisions made by the team, not the tool: Python/FastAPI as the stack, Postgres
over SQLite.

**22 Sep 2026 — Documentation and planning.** Commits `d545d0c`, `4893d01`,
`90019b5`.

- `README.md`: repo structure, endpoint table, baseline characteristics, run
  instructions, configuration, logging and evidence requirements.
- Team member table and responsibility split.
- Prediction record template.
- Drafted the work breakdown and schedule for the team.

Decisions made by the team, not the tool: who owns which step, the schedule,
and the freeze date.

**22 Sep 2026 — Dataset slice and golden set sampling.** Commit `62aa6ce`.

- Confirmed team number (5) resolves to rows 5000–5999 of the 50,000-row
  course extract.
- Wrote `scripts/make_golden_sample.py`: extracts the team's 1,000 rows for
  JMeter, and samples 200 of them (fixed seed, reproducible) into two
  identical blind labelling sheets with `source_label` stripped.
- Checked the resulting sample for category balance and confirmed both
  sheets contain the same 200 tickets.

Decisions made by the team, not the tool: team number (confirmed by the
team), sample size (200, within the brief's 150–200 range), and to withhold
the noisy source label from labellers.

**22 Sep 2026 — Role assignment revisions.** No code changes. Assisted with
drafting and revising the team task-split message as roles were reassigned
(golden set, candidate models, test rig, Week 5 ownership), and kept
`README.md`'s responsibility table consistent with each revision.

Decisions made by the team, not the tool: who does what.

**22 Sep 2026 — Merged SCHEDULE.md, PREDICTIONS.md and AI_USAGE.md into this
file** for a single working-notes document alongside README.md.

### Not done with AI

These are the parts the assignment is actually assessing, and they are the
team's own work:

- **Golden test set labelling.** Labelled by hand, independently, by two team
  members following a written protocol. No model output was consulted during
  labelling — doing so would drag the labels toward the model and corrupt the
  accuracy measurement, which is the specific failure the brief warns about.
- **The inter-annotator agreement statistic and the disagreement resolutions.**
- **The workload model** and the figures cited in it.
- **The requirements** and their justification.
- **The predictions**, which are the team's own expectations recorded before
  measuring.
- **All measurements.** Every latency, throughput, error rate and accuracy
  figure comes from an actual run on our hardware, recorded in the JMeter
  `.jtl` files and service logs kept in this repository.
- **The recommendation** and its defence against our stated requirements.

No number reported in the final deck is generated, estimated or inferred by an
AI tool. Every one traces to a log entry or a result file in this repository.

### For Slide 12

Acknowledge the tool alongside the other sources:

> Anthropic. *Claude Code* [AI coding assistant]. Used for scaffolding the
> baseline service implementation and project documentation. Accessed
> September 2026.

Check the citation style your module expects before submitting.
