import requests
from bs4 import BeautifulSoup
import json

url = "https://api.brightdata.com/datasets/v3/trigger"
headers = {
	"Authorization": "Bearer 3b369b87f24933189a6a9bcf6edbf1540eaaaba8942627d77866222423d8803f",
	"Content-Type": "application/json",
}
params = {
	"dataset_id": "gd_l95fol7l1ru6rlo116",
	"include_errors": "true",
	"type": "discover_new",
	"discover_by": "keyword",
}
data = {
	"input": [{"keyword":"leggins","domain":"https://www.walmart.com/"},{"keyword":"dress","domain":"https://www.walmart.ca/","all_variations":"false"}],
	"custom_output_fields": ["url","final_price","sku","currency","specifications","image_urls","top_reviews","rating_stars","related_pages","available_for_delivery","available_for_pickup","brand","breadcrumbs","category_ids","review_count","description","product_id","product_name","review_tags","category_url","category_name","category_path","root_category_url","root_category_name","upc","tags","main_image","rating","unit_price","unit","aisle","free_returns","sizes","colors","seller","other_attributes","customer_reviews","nutrition_information","ingredients","initial_price","discount","ingredients_full","categories","brand_walmart_url","rating_count","reviews_count","short_description","product_identifiers","store_name","store_location","retailer","price_range","availability_text","is_available","variants"],
}
response = requests.post(url, headers=headers, params=params, json=data)

print(response.text)

