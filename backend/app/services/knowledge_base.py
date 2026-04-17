from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.term import Term
from app.models.alert import Alert


class KnowledgeBaseService:
    @staticmethod
    def build_context(db: Session, knowledge_base_ids: Optional[List[str]]) -> str:
        if not knowledge_base_ids:
            return ""
        parts: List[str] = []
        if "kb_weather" in knowledge_base_ids:
            terms = db.query(Term).limit(20).all()
            if terms:
                parts.append("【气象术语库】")
                for t in terms:
                    parts.append(f"- {t.term}（{t.category or '通用'}）: {t.definition}")
        if "kb_alert" in knowledge_base_ids:
            alerts = db.query(Alert).limit(20).all()
            if alerts:
                parts.append("【预警信号库】")
                for a in alerts:
                    parts.append(f"- {a.alert_type}{a.level}预警: 标准={a.criteria}; 防御={a.response_guide or '无'}")
        return "\n".join(parts)
