from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db_session
from app.models.tool_config import ToolConfig
from app.schemas.tool_config import (
    ToolConfigSchema,
    ToolConfigUpdate,
    ToolConfigListResponse,
)

router = APIRouter(prefix="/api/v1/config/tools", tags=["tool_config"])

@router.get("/", response_model=ToolConfigListResponse)
def list_tools(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    """List all weather tool API configurations."""
    from app.config import settings, mask_api_key
    tools = db.query(ToolConfig).all()
    
    result = []
    for t in tools:
        key = t.api_key or ""
        if not key:
            if t.id == "weather_query":
                key = settings.tavily_api_key
            elif t.id == "alert_query":
                key = settings.qweather_api_key
                
        masked = mask_api_key(key) if key else ""
        
        schema_data = ToolConfigSchema.model_validate(t)
        schema_data.masked_api_key = masked
        result.append(schema_data)
        
    return ToolConfigListResponse(tools=result)

@router.put("/{tool_id}", response_model=ToolConfigSchema)
def update_tool(
    tool_id: str,
    req: ToolConfigUpdate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    """Update a weather tool API configuration."""
    from app.config import settings, mask_api_key
    tool_cfg = db.query(ToolConfig).filter(ToolConfig.id == tool_id).first()
    if not tool_cfg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool configuration '{tool_id}' not found.",
        )
    
    update_data = req.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(tool_cfg, key, val)
    
    db.commit()
    db.refresh(tool_cfg)
    
    key = tool_cfg.api_key or ""
    if not key:
        if tool_cfg.id == "weather_query":
            key = settings.tavily_api_key
        elif tool_cfg.id == "alert_query":
            key = settings.qweather_api_key
            
    masked = mask_api_key(key) if key else ""
    
    schema_data = ToolConfigSchema.model_validate(tool_cfg)
    schema_data.masked_api_key = masked
    return schema_data
