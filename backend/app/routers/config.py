from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.config import settings
from app.schemas.config import ConfigResponse, ConfigUpdate

router = APIRouter(prefix="/api/v1/config", tags=["config"])

@router.get("/", response_model=ConfigResponse)
def get_config(current_user: dict = Depends(get_current_user)):
    """获取当前配置（非敏感字段显示为掩码）"""
    return settings.get_config_dict(mask_secrets=True)

@router.put("/", response_model=ConfigResponse)
def update_config(update: ConfigUpdate, current_user: dict = Depends(get_current_user)):
    """更新配置"""
    update_dict = update.model_dump(exclude_unset=True)
    settings.update_config(**update_dict)
    return settings.get_config_dict(mask_secrets=True)