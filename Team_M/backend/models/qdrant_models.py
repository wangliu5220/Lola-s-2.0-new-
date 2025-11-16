from typing import Annotated
from pydantic import BaseModel, Field

class ProductRequest(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=255,
            description="Product name",
            examples=[
                "Organic Apple Juice",
                "Great Value Whole Vitamin D Milk, Gallon, Plastic, Jug, 128 fl oz",
            ],
        ),
    ]
    description: Annotated[
        str,
        Field(
            max_length=50000,
            description="Snippet content",
            examples=[
                "Straight from the orchard, our organic apple juice is made from 100% pure pressed apples with no added sugars or preservatives.",
                "Enjoy the wholesome goodness of Great Value Whole Vitamin D Milk Gallon in a plastic jug, 128 Fl Oz. This Grade A quality milk is pasteurized and delivers fresh from the farm taste. It offers an abundance of nutritional benefits such as protein, calcium, potassium and vitamins A and D. Our farms have pledged to not treat any cows with any artificial growth hormones. Great Value products provide families with affordable, high quality grocery options. With our wide range of product categories spanning grocery and household consumables, we offer you a variety of products for your family's needs. Our products are conveniently available online and in Walmart stores nationwide.",
            ],
        ),
    ]
