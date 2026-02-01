from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import secrets

from app.db.postgresql import get_db
from app.models.workspace import Workspace, WorkspaceInvite
from app.models.user import User, UserWorkspace, UserRole
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

class WorkspaceCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

class WorkspaceResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str]
    icon_url: Optional[str]
    owner_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class WorkspaceInviteCreate(BaseModel):
    email: str

@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    workspace_data: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new workspace."""
    # Check if slug is unique
    result = await db.execute(select(Workspace).where(Workspace.slug == workspace_data.slug))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Workspace slug already exists")
    
    workspace = Workspace(
        name=workspace_data.name,
        slug=workspace_data.slug,
        description=workspace_data.description,
        owner_id=current_user.id
    )
    db.add(workspace)
    await db.flush()
    
    # Add creator as owner
    user_workspace = UserWorkspace(
        user_id=current_user.id,
        workspace_id=workspace.id,
        role=UserRole.OWNER
    )
    db.add(user_workspace)
    await db.commit()
    await db.refresh(workspace)
    
    return workspace

@router.get("", response_model=List[WorkspaceResponse])
async def list_workspaces(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all workspaces for current user."""
    result = await db.execute(
        select(Workspace)
        .join(UserWorkspace)
        .where(UserWorkspace.user_id == current_user.id)
    )
    workspaces = result.scalars().all()
    return workspaces

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get workspace details."""
    result = await db.execute(select(Workspace).where(Workspace.id == workspace_id))
    workspace = result.scalar_one_or_none()
    
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Verify user is a member
    member_result = await db.execute(
        select(UserWorkspace).where(
            UserWorkspace.workspace_id == workspace_id,
            UserWorkspace.user_id == current_user.id
        )
    )
    if not member_result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not a member of this workspace")
    
    return workspace

@router.post("/{workspace_id}/invite")
async def invite_to_workspace(
    workspace_id: str,
    invite_data: WorkspaceInviteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Invite a user to workspace."""
    # Verify workspace exists and user has permission
    result = await db.execute(select(Workspace).where(Workspace.id == workspace_id))
    workspace = result.scalar_one_or_none()
    
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Create invite
    token = secrets.token_urlsafe(32)
    invite = WorkspaceInvite(
        workspace_id=workspace_id,
        email=invite_data.email,
        token=token,
        invited_by=current_user.id,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(invite)
    await db.commit()
    
    return {"invite_token": token, "expires_at": invite.expires_at}
