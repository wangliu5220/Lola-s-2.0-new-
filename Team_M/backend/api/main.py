from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from Team_M.backend.models.qdrant_models import ProductRequest
from Team_M.backend.services.qdrant_service import QdrantService
from typing import Annotated

app = FastAPI(
    title="Lola's 2.0 Backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post(
    path="/qdrant",
    status_code=status.HTTP_200_OK,
    summary="",
    responses={
    },
)
def handleProductQuery(
    request: ProductRequest,
    qdrant_svc: Annotated[QdrantService, Depends()]
):
    return qdrant_svc.query(request)


@app.post(
    path="/postgres",
    status_code=status.HTTP_200_OK,
    summary="",
    responses={
    },
)
def handleUserQuery():
    return 0