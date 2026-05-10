import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.message import Message


class ConversationService:
    @staticmethod
    def create(db: Session, user_id: int, title: str, model_id: str) -> Conversation:
        conv = Conversation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title or "新对话",
            model_id=model_id,
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)
        return conv

    @staticmethod
    def list_by_user(db: Session, user_id: int, page: int = 1, page_size: int = 20) -> tuple[List[Conversation], int]:
        query = db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    @staticmethod
    def get(db: Session, conversation_id: str, user_id: int) -> Optional[Conversation]:
        return db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        ).first()

    @staticmethod
    def rename(db: Session, conversation_id: str, user_id: int, title: str) -> Optional[Conversation]:
        conv = ConversationService.get(db, conversation_id, user_id)
        if conv:
            conv.title = title
            conv.updated_at = datetime.now()  # SQLite 不支持 onupdate，手动更新
            db.commit()
            db.refresh(conv)
        return conv

    @staticmethod
    def delete(db: Session, conversation_id: str, user_id: int) -> bool:
        conv = ConversationService.get(db, conversation_id, user_id)
        if conv:
            db.delete(conv)
            db.commit()
            return True
        return False

    @staticmethod
    def batch_delete(db: Session, conversation_ids: List[str], user_id: int) -> int:
        deleted = db.query(Conversation).filter(
            Conversation.id.in_(conversation_ids),
            Conversation.user_id == user_id,
        ).delete(synchronize_session=False)
        db.commit()
        return deleted

    @staticmethod
    def get_messages(db: Session, conversation_id: str, user_id: int) -> List[Message]:
        conv = ConversationService.get(db, conversation_id, user_id)
        if not conv:
            return []
        return db.query(Message).filter(
            Message.conversation_id == conversation_id,
        ).order_by(Message.created_at.asc()).all()

    @staticmethod
    def add_message(db: Session, conversation_id: str, role: str, content: str, tool_calls: Optional[dict] = None) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
        )
        db.add(msg)
        # 更新所属对话的 updated_at（SQLite 不支持 onupdate）
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conv:
            conv.updated_at = datetime.now()
        db.commit()
        db.refresh(msg)
        return msg