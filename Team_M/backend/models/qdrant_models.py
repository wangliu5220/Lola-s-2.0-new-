from typing import Annotated
from pydantic import BaseModel, Field

class ProductRequest(BaseModel):
    content: Annotated[
        str,
        Field(
            max_length=50000,
            description="Snippet content",
            examples=[
                "aw4u39qtameogjsdjsHHajn09se4upnta-7F",
                "The mitochondia is the powerhouse of the cell.",
            ],
        ),
    ]