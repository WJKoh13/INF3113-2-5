# Prediction Record

**Status: DRAFT — not yet frozen**

This file must be committed before our first benchmark run, together with the
golden test set. Once committed as final it cannot be revised. The commit
history is our evidence that these predictions predate the measurements.

Target freeze: **Mon 29 Sep 2026**

Marks are awarded for specificity, and for the quality of our later account of
where we were wrong — not for being right. A prediction that cannot fail earns
nothing. Commit to numbers, not to directions.

Rule of thumb for each claim below: could someone read our results table and
say "that was wrong"? If not, it needs a number.

---

## Test machines

We all have different machines, so every latency and throughput figure in this
file and in the final deck refers to **one designated machine** — the system
under test. Numbers measured on anyone else's machine are not comparable and
must not be mixed into the results.

| Role | Owner | Hardware | OS |
| --- | --- | --- | --- |
| **System under test** (service + Ollama + Postgres) | TBD | TBD | TBD |
| **Load generator** (JMeter) | TBD | TBD | TBD |

The two must be different machines — a co-hosted load generator steals CPU from
the service and produces latency numbers that will not be accepted as evidence.

Everyone else's machines are for development only. Dev anywhere; measure only
on the SUT.

What this does and does not constrain:

- **Latency, throughput, stress** — SUT only. Hardware-bound.
- **Accuracy** — much less hardware-sensitive (same model, same prompt,
  `temperature: 0`), so this work can be split across the team. Still record
  which machine produced each accuracy run.

### Anchor measurement

One measured data point from the baseline smoke test, for scaling the latency
estimates. Re-measure on the SUT once it is chosen and replace this row.

| Model | Machine | Narrative length | Latency |
| --- | --- | --- | --- |
| `llama3.2:1b` | Apple M3, 8 cores, 16 GB, macOS 26.5.2 (Wen Jun) | ~120 chars | ~2.6 s |

Everything else below is a guess made before measuring.

---

## 1. Bottleneck under load

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

---

## 2. Per-model predictions

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

---

## 3. Hardest categories

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

---

## After the measurements

Do not edit anything above this line once frozen. Record the comparison here,
and carry it onto Slide 11.

| Prediction | Actual | Off by | Why we think we were wrong |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |
