from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.lead import Lead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhook/lead")
def receber_lead(payload: dict, db: Session = Depends(get_db)):
    lead = Lead(
        nome=payload.get("nome"),
        telefone=payload.get("telefone"),
        email=payload.get("email"),
        origem=payload.get("origem"),
        mensagem_inicial=payload.get("mensagem")
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return {"status": "ok", "lead_id": lead.id}
