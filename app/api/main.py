from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import Base, engine, get_db
from app.db.models import ChatMessage
from app.pipeline import RAGPipeline

#  Creates the chat_messages table if it doesn't already exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Enterprice Inteligense GraphRag API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = RAGPipeline()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    id: int
    question: str
    answer: str
    entity_type: str | None
    entity_name: str | None

    class Config:
        from_attributes = True

@app.post("/chat", response_model=ChatResponse)
def post_chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Runs a question through the RAG pipeline and saves the exchange to the database."""

    result = pipeline.ask_debug(request.question)

    chat_message = ChatMessage(
        question = request.question,
        answer=result["answer"],
        entity_type=result.get("entity_type"),
        entity_name=result.get("name"),
    )

    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)

    return chat_message

@app.get("/chat", response_model=list[ChatResponse])
def get_chat(limit: int = 20, db: Session = Depends(get_db)):
    """Returns the most recent chat exchanges, newest first."""

    messages = (
        db.query(ChatMessage)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
        .all()
    )

    return messages
