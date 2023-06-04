from fastapi import APIRouter, Depends, HTTPException
import uuid as uuid_pkg
from app.auth.dependencies import atleast_teacher_access
from app.users.models import User
from app.groups.models import Group, GroupCreate
from app.groups.crud import GroupsCRUD
from app.groups.dependencies import get_groups_crud

router = APIRouter()


@router.get("")
async def get_all_groups_data(groups: GroupsCRUD = Depends(get_groups_crud), current_user: User = Depends(atleast_teacher_access)):
    return await groups.all_()


@router.get("/{uuid}")
async def get_group_data(uuid: uuid_pkg.UUID, groups: GroupsCRUD = Depends(get_groups_crud)):
    return await groups.get(uuid)


@router.put("", response_model=Group)
async def create_user_group(group: GroupCreate, current_user: User = Depends(atleast_teacher_access), groups: GroupsCRUD = Depends(get_groups_crud)):
    return await groups.create(group.name, group.color)


@router.patch("")
async def update_user_group():
    pass


@router.delete("")
async def delete_user_group():
    pass
