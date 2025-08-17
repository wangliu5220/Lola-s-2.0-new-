import Non_AI_Link_Scraping.Walmart_bs4 as Walmart_bs4
import os
import json


mock_links = [
    "https://www.walmart.com/ip/Coca-Cola-Mini-Soda-Pop-Fridge-Pack-7-5-fl-oz-Cans-10-Pack/125411280?athcpid=125411280&athpgid=AthenaContentPage_1001680&athcgid=null&athznid=ItemCarousel_8ae3b15c-272e-48e9-a6d9-111bb0c0fec6_items&athieid=v0&athstid=CS020&athguid=pLBLMGla_h7pLBbMmVflw37iNPPYmwonI6pw&athancid=null&athena=true&athbdg=L1600",
    "https://www.walmart.com/ip/Diet-Dr-Pepper-Soda-Pop-2-L-Bottle/16940508?classType=REGULAR&athbdg=L1600&from=/search",
    "https://www.walmart.com/ip/Great-Value-2-Reduced-Fat-Milk-Gallon-Refrigerated/10450115?classType=REGULAR&athbdg=L1600",
    "https://www.walmart.com/ip/Shamrock-Farms-Lactose-Free-Rockin-Protein-Builder-Chocolate-12-fl-oz-Bottle/21685899?classType=REGULAR&adsRedirect=true",
    "https://www.walmart.com/ip/Great-Value-1-Low-fat-Chocolate-Milk-Gallon-Plastic-Jug-128-Fl-Oz/17248403?classType=REGULAR",
    "https://www.walmart.com/ip/Chobani-Oatmilk-Zero-Sugar-Unsweetened-52-fl-oz/5853809550?classType=REGULAR&adsRedirect=true",
    "https://www.walmart.com/ip/Polar-Zero-Calorie-Lime-Sparkling-Seltzer-Water-12-fl-oz-8-Pack-Cans/505115147?athcpid=505115147&athpgid=AthenaItempage&athcgid=null&athznid=ci&athieid=v0&athstid=CS055~CS004&athguid=vKhIvxPOHnjgNeX52pvNkwNxzs2n61T8K4MU&athancid=5853809550&athposb=0&athena=true&athbdg=L1600",
    "https://www.walmart.com/ip/Synergy-The-Real-Kombucha-Gingerade-16-fl-oz/51259259?adsRedirect=true",
    "https://www.walmart.com/ip/Tropicana-Classic-Lemonade-Made-with-Real-Lemons-46-fl-oz-Bottle/5349984438?adsRedirect=true",
    "https://www.walmart.com/ip/Naked-Juice-Green-Machine-Flavored-100-Juice-Smoothie-Blend-15-2-fl-oz/10801719?classType=VARIANT&from=/search",
    "https://www.walmart.com/ip/Java-Monster-Loca-Moca-Coffee-Energy-Drink-11-fl-oz-6pk/957052004?classType=VARIANT",
    "https://www.walmart.com/ip/TAZO-Matcha-Latte-Green-Tea-32-oz-Carton/20709848?athcpid=20709848&athpgid=AthenaContentPage_1001320&athcgid=null&athznid=ItemCarousel_e2140114-d4e9-4603-b21f-e29c3b7295e0_items&athieid=v0&athstid=CS020&athguid=eaycUWOVh2Pm-BCcvGqIqC0SOfCp8FikdbBr&athancid=null&athena=true",
    "https://www.walmart.com/ip/Vita-Coco-Pure-Coconut-Water-1-Liter/34789040?classType=VARIANT&athbdg=L1200",
    "https://www.walmart.com/ip/4-pack-Jumex-Mango-Nectar-from-Concentrate-11-3-Fl-oz/14762319347?classType=VARIANT&from=/search",
    "https://www.walmart.com/ip/OLIPOP-Prebiotic-Soda-Classic-Root-Beer-12-fl-oz-4-Pack-Pantry-Packs/6925153849?athcpid=6925153849&athpgid=AthenaItempage&athcgid=null&athznid=si&athieid=v0_eeMzkuNDQsNjk1Mi4yOSwwLjAwNTk3MjUxNjEyNjQxMjc4LDAuNV8_cuW3siYnIiOnsiYXRocnMiOjAuMCwiYXRocyI6MC4wfSwiZm4iOnsiYXRocyI6MC4wMDIzNDExNjYzMTI4NTc2MjF9LCAiYnJ2IjoiaHYxIn1d&athstid=CS055~CS004&athguid=G05xzTAehwvmP8DiRc6LQBueJdEEGzTyKEEf&athancid=2292221250&athposb=0&athena=true",
    "https://www.walmart.com/ip/Carnation-Breakfast-Essentials-Nutritional-Protein-Packed-Drink-Shakes-Rich-Milk-Chocolate-8-fl-oz-6-Pack/34259082?classType=REGULAR&adsRedirect=true",
    "https://www.walmart.com/ip/Starbucks-Frappuccino-White-Chocolate-Mocha-Iced-Coffee-Drink-13-7-fl-oz-12-Pack-Bottles/2601000072?classType=VARIANT&adsRedirect=true",
    "https://www.walmart.com/ip/Horizon-Organic-High-Vitamin-D-Whole-Milk-High-Vitamin-D-Whole-64-fl-oz-Carton/10309701?classType=REGULAR&adsRedirect=true",
    "https://www.walmart.com/ip/Great-Value-Mountain-Lightning-Citrus-Flavored-Soda-Pop-2-Liter-Bottle/35506012?athcpid=35506012&athpgid=AthenaContentPage_1001680&athcgid=null&athznid=ItemCarousel_90ce338a-ba50-419c-9341-6f8b72233362_items&athieid=v0&athstid=CS020&athguid=XXpkw5cFGtHtrIZBtYxDCJwUfO2RmrkrAo7p&athancid=null&athena=true&athbdg=L1300",
    "https://www.walmart.com/ip/Culture-Pop-Soda-Watermelon-Probiotic-Soda-12-fl-oz/436428978?classType=REGULAR&athbdg=L1200&adsRedirect=true",
    "https://www.walmart.com/ip/Minute-Maid-No-Pulp-Orange-Fruit-Juice-59-fl-oz-Carton/22176380?athcpid=22176380&athpgid=AthenaItempage&athcgid=null&athznid=si&athieid=v0_eeMzcuNDYsMzM4Mi4yNzk5OTk5OTk5OTk3LDAuMDExMDY5OTAwOTQ0NzYzMDEzLDAuNV8_cuW3siYnIiOnsiYXRocnMiOjAuMCwiYXRocyI6MC4wfSwiZm4iOnsiYXRocyI6MC4wMDM2Nzc5NDI1ODkzOTAwNjYzfSwgImJydiI6Imh2MSJ9XQ&athstid=CS055~CS004&athguid=YYimtgCgkzgTN6D3gmzsxxu_P6FfOQzOmcZJ&athancid=13689271530&athposb=0&athena=true&athbdg=L1600",
    "https://www.walmart.com/ip/Sparkling-Ice-Naturally-Flavored-Sparkling-Water-Black-Raspberry-17-fl-oz/21268881?adsRedirect=true",
    "https://www.walmart.com/ip/Sanzo-Lychee-Sparkling-Water-12-Cans-Made-with-Real-Fruit-No-Added-Sugar-Carbonated-Water-Flavored/9247067342?adsRedirect=true",
    "https://www.walmart.com/ip/Core-Power-Protein-Shake-with-26g-Protein-by-fairlife-Milk-Vanilla-14-fl-oz/822766999?classType=VARIANT&athbdg=L1102&from=/search"
]

def main():
    OUTPUT_FILE = "mock_data.jsonl"
    
    with open(OUTPUT_FILE, 'w') as file:
        for link in mock_links:
            try:
                product_info = Walmart_bs4.extract_product_info(link, {})
                if product_info:
                    file.write(json.dumps(product_info)+"\n")
            except Exception as e:
                print(f"Failed to process URL {link}. Error {e}")

    return 0


if __name__ == "__main__":
    main()
