from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_chat_service
from app.schemas.chat import ChatQueryRequest, ChatQueryResponse
from app.services.chat.service import ChatService

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("/query", response_model=ChatQueryResponse)
def query(
    request: ChatQueryRequest,
    service: ChatService = Depends(get_chat_service),
) -> ChatQueryResponse:
    return service.query(request)


@router.post("/query/debug", response_model=ChatQueryResponse)
def query_debug(
    request: ChatQueryRequest,
    service: ChatService = Depends(get_chat_service),
) -> ChatQueryResponse:
    request.debug = True
    return service.query(request)

