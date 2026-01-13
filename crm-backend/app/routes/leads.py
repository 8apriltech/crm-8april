from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal
from app.models.lead import Lead
from app.deps import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/leads")
def listar_leads(db: Session = Depends(get_db), user=Depends(get_current_user)):
    leads = (
        db.query(Lead)
        .order_by(Lead.created_at.desc())
        .all()
    )

    return [
        {
            "id": lead.id,
            "nome": lead.nome,
            "telefone": lead.telefone,
            "email": lead.email,
            "origem": lead.origem,
            "status": lead.status,
            "mensagem": lead.mensagem_inicial,
            "created_at": lead.created_at
        }
        for lead in leads
    ]

class LeadStatusUpdate(BaseModel):
    status: str

@router.patch("/leads/{lead_id}")
def atualizar_status(
    lead_id: int,
    payload: LeadStatusUpdate,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")

    lead.status = payload.status
    db.commit()
    db.refresh(lead)

    return {"status": "ok"}
