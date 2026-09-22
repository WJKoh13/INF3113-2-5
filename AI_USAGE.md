# AI Tool Usage

The assignment brief permits and expects AI coding tools: *"AI coding tools are
permitted and expected throughout. The build is a few hours' work with an agent,
and that is accepted."*

It also draws the line clearly: *"an agent will not label your test data, run
your load tests, or make your recommendation. The assessment targets
measurement, interpretation, and judgement."*

This file records what was done with AI assistance and what was not, so the
division is auditable. Add to it as the project goes.

**Tool used:** Claude Code (Claude Opus 5 / Claude Sonnet 5), Anthropic.

---

## Log

### 22 Sep 2026 — Baseline service scaffold

Commit `c6cedbf`.

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

### 22 Sep 2026 — Documentation and planning

Commits `d545d0c`, `4893d01`, `90019b5`.

- `README.md`: repo structure, endpoint table, baseline characteristics, run
  instructions, configuration, logging and evidence requirements.
- Team member table and responsibility split.
- `PREDICTIONS.md`: template for the Step 4 prediction record.
- Drafted the work breakdown and schedule for the team.

Decisions made by the team, not the tool: who owns which step, the schedule,
and the freeze date.

---

## Not done with AI

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

---

## For Slide 12

Acknowledge the tool alongside the other sources:

> Anthropic. *Claude Code* [AI coding assistant]. Used for scaffolding the
> baseline service implementation and project documentation. Accessed
> September 2026.

Check the citation style your module expects before submitting.
