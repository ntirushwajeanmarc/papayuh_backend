from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import AIChatLog

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # Placeholder AI response
    answer = f"Response to: {req.question}"
    log = AIChatLog(question=req.question, answer=answer)
    db.add(log)
    db.commit()
    return {"question": req.question, "answer": answer}
