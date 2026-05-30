from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_current_user, get_db_session
from app.database import SessionLocal
from app.models.model_config import ModelConfig
from app.schemas.model_config import (
    ModelConfigSchema,
    ModelConfigCreate,
    ModelConfigUpdate,
    ModelConfigListResponse,
)

router = APIRouter(prefix="/api/v1/config/models", tags=["model_config"])

@router.get("/", response_model=ModelConfigListResponse)
def list_models(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    """List all LLM model configurations."""
    from app.services.llm import get_model_config
    from app.config import mask_api_key
    models = db.query(ModelConfig).order_by(ModelConfig.created_at.asc()).all()
    
    result = []
    for m in models:
        cfg = get_model_config(m.id, db=db)
        key = cfg.get("api_key") or ""
        masked = mask_api_key(key) if key else ""
        
        schema_data = ModelConfigSchema.model_validate(m)
        schema_data.masked_api_key = masked
        result.append(schema_data)
        
    return ModelConfigListResponse(models=result)

@router.post("/", response_model=ModelConfigSchema)
def create_model(
    req: ModelConfigCreate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    """Create a new model configuration."""
    from app.services.llm import get_model_config
    from app.config import mask_api_key
    existing = db.query(ModelConfig).filter(ModelConfig.id == req.id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Model ID '{req.id}' already exists.",
        )
    model_cfg = ModelConfig(**req.model_dump())
    db.add(model_cfg)
    db.commit()
    db.refresh(model_cfg)
    
    cfg = get_model_config(model_cfg.id, db=db)
    key = cfg.get("api_key") or ""
    schema_data = ModelConfigSchema.model_validate(model_cfg)
    schema_data.masked_api_key = mask_api_key(key) if key else ""
    return schema_data

@router.put("/{model_id}", response_model=ModelConfigSchema)
def update_model(
    model_id: str,
    req: ModelConfigUpdate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    """Update an existing model configuration."""
    from app.services.llm import get_model_config
    from app.config import mask_api_key
    model_cfg = db.query(ModelConfig).filter(ModelConfig.id == model_id).first()
    if not model_cfg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model configuration '{model_id}' not found.",
        )
    
    update_data = req.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(model_cfg, key, val)
    
    db.commit()
    db.refresh(model_cfg)
    
    cfg = get_model_config(model_cfg.id, db=db)
    key = cfg.get("api_key") or ""
    schema_data = ModelConfigSchema.model_validate(model_cfg)
    schema_data.masked_api_key = mask_api_key(key) if key else ""
    return schema_data

@router.delete("/{model_id}")
def delete_model(
    model_id: str,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    """Delete a model configuration."""
    model_cfg = db.query(ModelConfig).filter(ModelConfig.id == model_id).first()
    if not model_cfg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model configuration '{model_id}' not found.",
        )
    
    db.delete(model_cfg)
    db.commit()
    return {"detail": f"Model configuration '{model_id}' deleted."}
