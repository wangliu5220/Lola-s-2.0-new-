from nutr_cleaner import DataCleaner
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "temp_storage_of_processed_sheets\merged_nutrition_information_8_18.xlsx")
ultra_processed_path = os.path.join(current_dir, "ultraprocessed_ingredients.xlsx")
ultra_p_sheet: DataCleaner = DataCleaner(ultra_processed_path)
dc: DataCleaner = DataCleaner(file_path)

percent_missing_calories = dc.calculate_missing_calorie("calories_x")
print(percent_missing_calories)

columns_to_merge = [
    'ingredients/0',
    'ingredients/1',
    'ingredients/2',
    'ingredients/3',
    'ingredients/4',
    'ingredients/5',
    'ingredients/6',
    'ingredients/7',
    'ingredients/8',
    'ingredients/9',
    'ingredients/10',
    'ingredients/11',
    'ingredients/12',
    'ingredients/13',
    'ingredients/14',
    'ingredients/15',
    'ingredients/16',
    'ingredients/17',
    'ingredients/18',
    'ingredients/19',
    'ingredients/20',
    'ingredients/21',
    'ingredients/22',
    'ingredients/23',
    'ingredients/24',
    'ingredients/25',
    'ingredients/26',
    'ingredients/27',
    'ingredients/28',
    'ingredients/29',
    'ingredients/30',
    'ingredients/31',
    'ingredients/32',
    'ingredients/33',
    'ingredients/34',
    'ingredients/35',
    'ingredients/36',
    'ingredients/37',
    'ingredients/38',
    'ingredients/39',
    'ingredients/40',
    'ingredients/41',
    'ingredients/42',
    'ingredients/43',
    'ingredients/44',
    'ingredients/45',
    'ingredients/46',
    'ingredients/47',
    'ingredients/48',
]
dc.df['ingredients'] = dc.df[columns_to_merge].map(str).agg(', '.join, axis=1)
dc.remove_text('ingredients', 'nan, ')
dc.remove_text('ingredients', ', nan')
dc.df['ingredients'] = dc.df['ingredients'].str.upper(
    
)
dc.find_serving_info('serving_size')

# Modifies the dataframe by added specific columns in requested order
dc.df = dc.df[[
    'dep/cat/shelf1',
    'dep/cat/shelf2',
    'dep/cat/shelf3',
    'product_name_x',
    'brand',
    'short_description',
    'serving_size',
    'percent_juice', 
    'calories_y',
    'total_fat_absolute',
    'total_fat_DV',
    'saturated_fat_absolute',
    'saturated_fat_DV',
    'total_carbs_absolute',
    'total_carbs_DV',
    'total_sugars_absolute',
    'included_added_sugars_absolute',
    'included_added_sugars_DV',
    'protein_absolute',
    'protein_DV',
    'cholesterol_absolute',
    'cholesterol_DV',
    'trans_fat_absolute',
    'trans_fat_DV',
    'polyunsaturated_fat_absolute',
    'monounsaturated_fat_absolute',
    'fiber_absolute',
    'fiber_DV',
    'sodium_absolute',
    'sodium_DV',
    'ingredients',
    'product_URL',
    'thumbnail_image_url',
    'image_url_1',
    'image_url_2',
    'image_url_3',
    'image_url_4',
    'image_url_5',
    'image_url_6',
    'image_url_7',
    'image_url_8',
    'image_url_9',
    'image_url_10',
    'image_url_11',
    'image_url_12',
    'price',
    'universal_product_code',
    'zip_code',
    'snap_eligible',
    'avg_rating',
    'review_count'
]]
dc.df.rename(columns = {'calories_y': 'calories'}, inplace = True)
dc.df.rename(columns={'product_name_x': 'product_name'}, inplace=True)
dc.apply_parse_product_name('product_name')

# Rename dep, shelf, and aisle columns 
dc.df.rename(columns={'dep/cat/shelf1': 'department'}, inplace=True)
dc.df.rename(columns={'dep/cat/shelf2': 'aisle'}, inplace=True)
dc.df.rename(columns={'dep/cat/shelf3': 'shelf'}, inplace=True)

# Standerdizing the serving size column
dc.add_spacer('serving_size')
dc.convert_fl_oz_to_ml('serving_size')
dc.convert_cups_to_ml('serving_size')
dc.convert_l_to_ml('serving_size')
dc.convert_oz_to_g('serving_size')

dc.add_spacer('calories')

# Changing <UNKNOWN> vals to blanks
dc.unknown_cleaner('serving_size')
dc.unknown_cleaner('calories')
dc.unknown_cleaner('total_sugars_absolute')
dc.unknown_cleaner('price')
dc.unknown_cleaner('sodium_absolute')
dc.unknown_cleaner('saturated_fat_absolute')
for col in dc.df.columns:
    dc.unknown_cleaner(col)



#start adding new per 100 columns 
dc.call_nutr_per_100('serving_size', 'calories')
dc.call_nutr_per_100('serving_size', 'total_sugars_absolute')
dc.call_nutr_per_100('serving_size', 'sodium_absolute')
dc.call_nutr_per_100('serving_size', 'saturated_fat_absolute')
dc.call_nutr_per_100('serving_size', 'price')

# Check ultraprocessed
UPF_list = []

ultra_p_sheet.to_list(UPF_list,['industrialised ingredient search terms','Alternative English Names','E/INS Numbers'])
dc.flag_ultra_processed('ingredients', UPF_list)
dc.preview()

# Re-adding new columns and reordering
dc.df = dc.df[[
    'department',
    'aisle',
    'shelf',
    'product_name',
    'brand',
    'short_description',
    'serving_size',
    'pack_unit',
    'unit_size',
    'pack_size',
    'percent_juice', 
    'calories',
    'total_fat_absolute',
    'total_fat_DV',
    'saturated_fat_absolute',
    'saturated_fat_DV',
    'total_carbs_absolute',
    'total_carbs_DV',
    'total_sugars_absolute',
    'included_added_sugars_absolute',
    'included_added_sugars_DV',
    'protein_absolute',
    'protein_DV',
    'cholesterol_absolute',
    'cholesterol_DV',
    'trans_fat_absolute',
    'trans_fat_DV',
    'polyunsaturated_fat_absolute',
    'monounsaturated_fat_absolute',
    'fiber_absolute',
    'fiber_DV',
    'sodium_absolute',
    'sodium_DV',
    'price_per_100',
    'calories_per_100',
    'total_sugars_absolute_per_100',
    'sodium_absolute_per_100',
    'saturated_fat_absolute_per_100',
    'ingredients',
    'product_URL',
    'thumbnail_image_url',
    'image_url_1',
    'image_url_2',
    'image_url_3',
    'image_url_4',
    'image_url_5',
    'image_url_6',
    'image_url_7',
    'image_url_8',
    'image_url_9',
    'image_url_10',
    'image_url_11',
    'image_url_12',
    'price',
    'universal_product_code',
    'zip_code',
    'snap_eligible',
    'avg_rating',
    'review_count',
    'ultra_processed_flag',
]]
dc.save_data("Nutrition_Information_Processing\edited.xlsx")
