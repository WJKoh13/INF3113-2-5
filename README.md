# INF3113-2-5 — Ticket Triage Service

Assignment 1: Performance Requirements & Testing.

A ticket triage service that classifies financial services complaint narratives
into one of seven categories using a locally hosted LLM. Built as the "system
under test" for performance and accuracy measurement.

**Client constraint:** no public model API. All inference runs on CPU-only
hardware the client controls, so the model backend is Ollama running locally.

Due **Fri 9 Oct 2026, 2359**. See [SCHEDULE.md](SCHEDULE.md) for per-person
deadlines and [AI_USAGE.md](AI_USAGE.md) for what was AI-assisted.

## Team

Team number: **5** — so our dataset slice is rows **5000–5999** of the course
extract (team `n` uses rows `n × 1000` to `n × 1000 + 999`). All labelling and
all test traffic must come from these rows.

| Name | Student ID | Primary responsibility | Then (Step 5) |
| --- | --- | --- | --- |
| Koh Wen Jun | 2401646 | Golden set — labeller (`labelling_sheet_A.csv`) (Step 1) | Backend service maintenance, instrumentation |
| Lau Peng Jie | 2402164 | Workload model, requirements (Steps 3, 4) | JMeter open-loop runs |
| Muhammad Haidar Bin Abdul Hamid | 2401912 | Test rig — machine setup (Step 5 prep) | JMeter open-loop runs, stress test |
| Raffael Davin Harjanto | 2402294 | Golden set — labeller (`labelling_sheet_B.csv`) (Step 1) | Accuracy tests, confusion matrices |
| Teo Min Megan Lynette | 2401824 | Candidate models, prediction record draft (Step 4) | Accuracy tests, confusion matrices |

Step 1 (golden set) and Steps 3–4 (workload model, requirements, predictions)
run in parallel from Week 1. Step 5 cannot begin until Steps 1–4 are complete
and committed. Step 6 (the recommendation) and the slide deck are the whole
team.

Note: `labelling_sheet_A.csv` and `labelling_sheet_B.csv` contain the
identical 200 tickets — the filename maps to a labeller, not to a different
sample. See [Golden test set](#golden-test-set) below for why.

## Repository structure

```
.
├── docker-compose.yml          # triage-service + postgres + ollama
├── triage-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py             # endpoints, per-request logging
│       ├── db.py               # SQLAlchemy models, Postgres connection
│       ├── ollama_client.py    # synchronous classification call
│       └── categories.py       # the seven fixed categories
├── data/
│   └── team5_rows.csv          # our 1000 rows — JMeter draws from this
├── golden-set/
│   ├── labelling_sheet_A.csv   # 200 tickets, blind, labeller A
│   └── labelling_sheet_B.csv   # same 200 tickets, labeller B
├── scripts/
│   └── make_golden_sample.py   # regenerates the above, fixed seed
├── PREDICTIONS.md              # Step 4 prediction record
├── AI_USAGE.md                 # what was AI-assisted, what was not
└── README.md
```

Not tracked in git (see `.gitignore`): the assignment brief, the raw 50,000-row
dataset CSV (45 MB), and `logs/`.

## Golden test set

Our 200 tickets are sampled from rows 5000–5999 with a fixed seed
(`scripts/make_golden_sample.py`, seed `20260922`), so the sample is
reproducible and demonstrably not cherry-picked.

The labelling sheets **omit `source_label` deliberately.** Those labels were
selected by consumers at submission time and are noisy; seeing them while
labelling would anchor our labels to them. For the same reason, no labelling
happens after seeing model output.

Two team members label the same 200 tickets independently, without conferring,
following the written protocol. Both sheets are kept — we submit them along
with the agreement statistic and the record of how each disagreement was
resolved.

To regenerate (needs `ict3113_tickets.csv` in the repo root):

```bash
python3 scripts/make_golden_sample.py
```

Do not rerun with a different seed or sample size after the golden set is
frozen.

## Categories

Credit reporting · Debt collection · Mortgage · Credit card ·
Bank account or service · Consumer loan · Money transfer or service

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/tickets` | Accepts one ticket narrative, classifies it via the model backend, stores the result, returns the assigned category |
| `GET` | `/search?q=` | Returns stored tickets whose narrative matches the text query |
| `GET` | `/stats` | Returns counts of stored tickets by category |
| `GET` | `/health` | Liveness check |

The service starts empty. Tickets enter only through `POST /tickets` — the
dataset CSV is never loaded into the service directly.

## Baseline characteristics

Per Step 2, this is the deliberately unoptimised baseline:

- Classification is **synchronous** — `POST /tickets` does not return until the
  model has classified the ticket.
- **No caching.** Identical narratives are re-classified from scratch.
- **No queuing.** Requests are handled as they arrive.

Optimisation is Assignment 2. Do not pre-optimise this.

## Running it

Requires Docker Desktop (or Docker engine) running.

```bash
docker compose up --build -d
docker compose exec ollama ollama pull <model:tag>   # e.g. llama3.2:1b
```

The service listens on `localhost:8000`, Ollama on `localhost:11434`.

Smoke test:

```bash
curl -s localhost:8000/health

curl -s -X POST localhost:8000/tickets \
  -H 'Content-Type: application/json' \
  -d '{"narrative": "I have been trying to dispute an incorrect late payment on my credit report for three months."}'

curl -s localhost:8000/stats
curl -s "localhost:8000/search?q=credit"
```

Inspect stored rows directly:

```bash
docker compose exec db psql -U triage -d triage -c 'select id, category, model, created_at from tickets;'
```

Tear down (`-v` also drops the database and pulled models):

```bash
docker compose down
docker compose down -v
```

## Configuration

Set in `docker-compose.yml` under `triage-service.environment`:

| Variable | Default | Notes |
| --- | --- | --- |
| `OLLAMA_MODEL` | `llama3.2:1b` | Change per candidate model under test. Pin by exact tag, and record the digest for the report. |
| `OLLAMA_BASE_URL` | `http://ollama:11434` | Point elsewhere if Ollama runs on a separate machine |
| `DATABASE_URL` | `postgresql://triage:triage@db:5432/triage` | |

To capture a model's digest for the submission:

```bash
docker compose exec ollama ollama show <model:tag>
```

## Logging and evidence

Every request is logged with a request id, ticket id, assigned category, and
elapsed milliseconds. Logs go to stdout:

```bash
docker compose logs triage-service
docker compose logs triage-service > logs/run-N.log    # keep per run
```

Every number reported in the final document must reconcile with these logs and
with the raw JMeter `.jtl` files. Keep both in the repository for every run
reported — a number that cannot be traced to a log entry is treated as
unsupported.

## Commit order matters

The golden test set and the prediction record must be committed **before the
first benchmark run**. The commit history is the evidence that the labels and
predictions predate the measurements, so do not run benchmarks until both are
in.

## Testing notes

The load generator and the system under test must run on **separate machines** —
a co-hosted load generator steals CPU from the service and produces unusable
latency numbers.

JMeter traffic must be generated **open-loop** at controlled arrival rates (Open
Model Thread Group or Precise Throughput Timer). Closed-loop results will not be
accepted as evidence.

Three runs per configuration, reporting means and spread.

## Data source

Course extract from the Consumer Complaint Database published by the US Consumer
Financial Protection Bureau:
<https://www.consumerfinance.gov/data-research/consumer-complaints/>

Raw category labels were selected by consumers at submission time and are noisy —
hence the hand-labelled golden test set.
