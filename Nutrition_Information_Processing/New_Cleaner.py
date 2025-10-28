from nutr_cleaner import DataCleaner
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "to_be_edited_info/Non_Bev_Sample.xlsx")
ultra_processed_path = os.path.join(current_dir, "ultraprocessed_ingredients.xlsx")
ultra_p_sheet: DataCleaner = DataCleaner(ultra_processed_path)
dc: DataCleaner = DataCleaner(file_path)

dc.unknown_cleaner('servings_per_container')
dc.unknown_cleaner('serving_size')
dc.unknown_cleaner('percent_juice')
dc.unknown_cleaner('calories')
dc.unknown_cleaner('total_fat_absolute')
dc.unknown_cleaner('total_fat_DV')
dc.unknown_cleaner('sodium_absolute')
dc.unknown_cleaner('sodium_DV')
dc.unknown_cleaner('total_carbs_absolute')
dc.unknown_cleaner('total_carbs_DV')
dc.unknown_cleaner('total_sugars_absolute')
dc.unknown_cleaner('included_added_sugars_absolute')
dc.unknown_cleaner('included_added_sugars_DV')
dc.unknown_cleaner('protein_absolute')  
dc.unknown_cleaner('protein_DV')
dc.unknown_cleaner('cholesterol_absolute')
dc.unknown_cleaner('cholesterol_DV')
dc.unknown_cleaner('saturated_fat_absolute')
dc.unknown_cleaner('saturated_fat_DV')
dc.unknown_cleaner('trans_fat_absolute')
dc.unknown_cleaner('trans_fat_DV')
dc.unknown_cleaner('fiber_absolute')
dc.unknown_cleaner('fiber_DV')
dc.unknown_cleaner('polyunsaturated_fat_absolute')
dc.unknown_cleaner('monounsaturated_fat_absolute')

dv_fields = [
    'total_carbs_DV',
    'total_fat_DV',
    'sodium_DV',
    'included_added_sugars_DV',
    'protein_DV',
    'cholesterol_DV',
    'saturated_fat_DV',
    'trans_fat_DV',
    'fiber_DV',
]

for field in dv_fields:
    dc.extract_value(field)

dc.extract_DV('total_carbs_DV')

dc.multiply_columns('total_carbs_DV', 'serving_size', 'Carbs_standardized')

dc.save_data("Nutrition_Information_Processing/temp_storage_of_processed_sheets/non_bev_sample_cleaned_info.xlsx")