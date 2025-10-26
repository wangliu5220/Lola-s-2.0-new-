from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

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

@app.get(
    path="/qdrant",
    status_code=status.HTTP_200_OK,
    summary="",
    responses={
    },
)
def handleProductQuery():
    return 0


@app.get(
    path="/postgres",
    status_code=status.HTTP_200_OK,
    summary="",
    responses={
    },
)
def handleUserQuery():
    return 0