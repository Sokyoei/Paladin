import uuid

from django.http import HttpRequest
from ninja import Router

from django_learn.utils.ninja_utils import ApiResponse

from .models import SwallowedStarRole
from .schemas import SwallowedStarRoleCreate, SwallowedStarRoleResponse, SwallowedStarRoleUpdate

ss_router = Router(tags=["吞噬星空"])


@ss_router.post("/roles", summary="新建角色", response=ApiResponse[SwallowedStarRoleResponse])
def create_ss_role(request: HttpRequest, role: SwallowedStarRoleCreate):
    new_role = SwallowedStarRole.objects.create(**role.dict())
    return ApiResponse.success(SwallowedStarRoleResponse.from_orm(new_role))


@ss_router.delete("/roles/{role_id}", summary="删除角色", response=ApiResponse)
def delete_ss_role(request: HttpRequest, role_id: uuid.UUID):
    try:
        role = SwallowedStarRole.objects.get(id=role_id)
        role_data = SwallowedStarRoleResponse(role.from_db(role))
        role.delete()
        return ApiResponse.success(role_data)
    except SwallowedStarRole.DoesNotExist:
        return ApiResponse.fail_404("角色不存在")


@ss_router.patch("/roles/{role_id}", summary="更新角色", response=ApiResponse)
def update_ss_role(request: HttpRequest, role_id: uuid.UUID, role_update: SwallowedStarRoleUpdate):
    try:
        role = SwallowedStarRole.objects.get(id=role_id)
        update_data = role_update.dict(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(role, field, value)
        role.save()
        return ApiResponse.success(SwallowedStarRoleResponse.from_orm(role))
    except SwallowedStarRole.DoesNotExist:
        return ApiResponse.fail_404("角色不存在")


@ss_router.get("/roles/{role_id}", summary="查找角色", response=ApiResponse[SwallowedStarRoleResponse])
def search_ss_role(request: HttpRequest, role_id: uuid.UUID):
    try:
        role = SwallowedStarRole.objects.get(id=role_id)
        return ApiResponse.success(SwallowedStarRoleResponse.from_orm(role))
    except SwallowedStarRole.DoesNotExist:
        return ApiResponse.fail_404("角色不存在")


@ss_router.get("/roles", summary="获取所有角色", response=ApiResponse[SwallowedStarRoleResponse])
def get_all_ss_roles(request: HttpRequest):
    roles = SwallowedStarRole.objects.all()
    role_list = [SwallowedStarRoleResponse.from_orm(role) for role in roles]
    return ApiResponse.success(role_list)
