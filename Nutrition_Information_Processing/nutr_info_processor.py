import pandas as pd


def match_and_concatenate_rows(file_path1, file_path2, sheet_name1, sheet_name2, column_name):
    df1 = pd.read_excel(file_path1, sheet_name=sheet_name1)
    df2 = pd.read_excel(file_path2, sheet_name=sheet_name2)
    
    # Convert the 'universal_product_code' column to the same data type in both dataframes
    df1['universal_product_code'] = df1['universal_product_code'].astype(str).apply(lambda x: x.zfill(12))
    df2['universal_product_code'] = df2['universal_product_code'].astype(str)
    print(df1['universal_product_code'])
    print(df2['universal_product_code'])
    # Merge the two dataframes on the 'universal_product_code' column
    merged_df = pd.merge(df1, df2, left_on=column_name, right_on=column_name, how='left')
    
    return merged_df

def flag_missing_ingredients(df):
    # df['no_image_ingred'] = df['ingredients/0'].isna().apply(lambda x: 1 if x else 0)
    # df['no_image_ingred'] = df['ingredients/0'].apply(lambda x: 1 if x in ['', 'unknown', 'Unknown', 'UNKNOWN','<UNKNOWN>',None, 'nan'] else 0)
    df['no_image_ingred'] = df['ingredients/0'].apply(lambda x: 1 if pd.isna(x) or x in ['', 'unknown', 'Unknown', 'UNKNOWN','<UNKNOWN>'] else 0)

def sort_columns(df):
    df = df.reindex(sorted(df.columns), axis=1)
    return df

def main():
    file_path1 = 'Nutrition_Information_Processing/to_be_edited_info/finalized_web_scraped_data.xlsx'
    file_path2 = 'Nutrition_Information_Processing/to_be_edited_info\Final_AI_response.xlsx'
    sheet_name1 = 'Sheet 1'
    sheet_name2 = 'Sheet 1'
    column_name = 'universal_product_code'
    
    final_df = match_and_concatenate_rows(file_path1, file_path2, sheet_name1, sheet_name2, column_name)
    final_df['no_image_ingred'] = 0
    flag_missing_ingredients(final_df)
    print(final_df['ingredients/0'][5])
    print(pd.isna(final_df['ingredients/0'][5]))
    print(final_df['no_image_ingred'][5])
    sort_columns(final_df)

    
    try:
        final_df.to_excel('Nutrition_Information_Processing/merged_nutrition_information.xlsx', index=False)
    except Exception as e:
        print(f"An error occurred while saving the final dataframe to an Excel file: {e}")


if __name__ == "__main__":
    main()