import logging
import time

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import ollama_client
from app.categories import CATEGORIES
from app.db import Ticket, get_db, init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("triage")

app = FastAPI(title="Ticket Triage Service")


@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Startup complete. Model=%s Ollama=%s", ollama_client.OLLAMA_MODEL, ollama_client.OLLAMA_BASE_URL)


class TicketIn(BaseModel):
    narrative: str


class TicketOut(BaseModel):
    id: int
    narrative: str
    category: str
    model: str

    class Config:
        from_attributes = True


@app.post("/tickets", response_model=TicketOut)
def create_ticket(ticket: TicketIn, db: Session = Depends(get_db)):
    """Synchronous baseline: classifies via Ollama before returning, per
    Assignment 1 Step 2 (no caching, no queuing)."""
    start = time.perf_counter()
    request_id = f"{int(start * 1000)}"

    logger.info("request_id=%s POST /tickets narrative_len=%d", request_id, len(ticket.narrative))

    try:
        category = ollama_client.classify(ticket.narrative)
    except Exception:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.exception("request_id=%s classification failed elapsed_ms=%.1f", request_id, elapsed_ms)
        raise HTTPException(status_code=502, detail="Model backend error")

    row = Ticket(narrative=ticket.narrative, category=category, model=ollama_client.OLLAMA_MODEL)
    db.add(row)
    db.commit()
    db.refresh(row)

    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "request_id=%s POST /tickets ticket_id=%d category=%s elapsed_ms=%.1f",
        request_id, row.id, category, elapsed_ms,
    )
    return row


@app.get("/search", response_model=list[TicketOut])
def search_tickets(q: str = "", db: Session = Depends(get_db)):
    logger.info("GET /search q=%r", q)
    query = db.query(Ticket)
    if q:
        query = query.filter(Ticket.narrative.ilike(f"%{q}%"))
    return query.order_by(Ticket.id.desc()).limit(200).all()


@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    logger.info("GET /stats")
    rows = db.query(Ticket.category, func.count(Ticket.id)).group_by(Ticket.category).all()
    counts = {category: 0 for category in CATEGORIES}
    for category, count in rows:
        counts[category] = count
    return counts


@app.get("/health")
def health():
    return {"status": "ok"}
