import pandas as pd
import re


class DataCleaner:
    def __init__(self, file_path, sheet_name="Sheet1"):
        """
        Initializes the DataCleaner with the file path and sheet name.
        :param file_path: Path to the Excel file.
        :param sheet_name: Name of the sheet to load (default is 'Sheet1').
        """
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)

    def calculate_missing_calorie(self, column):
        """
        Calculates the percentage of missing calorie information
        """
        missing_values = self.df[column].apply(lambda x: x in ["", "not found"] or pd.isna(x))
        return missing_values.sum() / len(self.df[column])

        
        
    def remove_text(self, column, text):
        """
        Removes unwanted text from a specified column.
        :param column: The column name to clean.
        :param text: The text to remove from the column.
        """
        if self.df[column].dtypes != "object":
            raise Exception("Cannot remove text on a non-string column")
        self.df[column] = self.df[column].str.replace(text, "", regex=False)

    def strip_spaces(self, column):
        """
        Strips leading and trailing spaces from a specified column.
        :param column: The column name to strip spaces from.
        """
        if self.df[column].dtypes != "object":
            raise TypeError("Cannot strip spaces on a non-string column")
        self.df[column] = self.df[column].str.strip()

    def handle_missing(self, column, strategy="mean"):
        """
        Handles missing values in a specified column.
        :param column: The column name with missing values.
        :param strategy: The strategy to handle missing values ('mean', 'zero',
        etc.).
        """
        if strategy == "mean":
            mean_value = self.df[column].mean()
            self.df[column] = self.df[column].fillna(mean_value)
        elif strategy == "zero":
            self.df[column] = self.df[column].fillna(0)
        elif strategy == "drop":
            self.df = self.df.dropna(subset=[column])

    def drop(self, columns):
        """
        Drops unwanted columns from the dataset.
        :param columns: List of column names to drop.
        """
        self.df = self.df.drop(columns=columns)

    def save_data(self, output_path="export.xlsx"):
        """
        Saves the cleaned data to a new Excel file.
        :param output_path: Path where the cleaned data should be saved.
        """
        try:
            self.df.to_excel(output_path, index=False, engine="openpyxl")
            print(f"Data successfully saved to {output_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def preview(self, n=5):
        """
        Previews the first few rows of the cleaned data.
        :param n: Number of columns to print.
        """
        return self.df.head(n)

    def to_float(self, column):
        """
        Convert specfied column to float data type.
        :param column: Name of column.
        """

        def clean_numeric(value):
            if isinstance(value, str):
                # Extract only numeric parts (including decimal)
                match = re.search(r"(\d+\.?\d*)", value)
                return (
                    float(match.group(1)) if match else None
                )  # Convert to float or None
            return value  # Keep existing numeric values

        # Apply the cleaning function and convert to float
        self.df[column] = self.df[column].apply(clean_numeric).astype(float)

    def round(self, column, decimals):
        """
        Round specfied column to specified decimal amount.
        :param column: Name of column.
        :param decimals: Number of decimals to round by.
        """
        self.df[column] = self.df[column].round(decimals)

    def new_column(self, column, items):
        """
        Add new column in dataframe.
        :param column: Name of column.
        :param items: List of items to be added to column.
        """
        self.df[column] = items

    def sub_sample_rows(self, column, num):
        """
        Keeps only the first 'num' rows for each unique value in the specified
        column, while skipping rows containing blank entries.

        :param column: The column name to group by (e.g., 'department').
        :param num: The number of rows per group
        """

        # Remove rows with any blank (NaN) values
        self.df = self.df.dropna()

        self.df = (
            self.df.groupby(column, group_keys=False)
            .apply(lambda x: x.iloc[:num])
            .reset_index(drop=True)
        )

    def count_unique_entries(self, column):
        """
        Counts the number of unique entries in the 'column' column

        :param column: The column name whose unique entries are being counted
        """

        return self.df[column].nunique()

    def drop_blank_rows(self):
        """
        Drops rows with any blank or missing (NaN) entries in the DataFrame.
        """
        self.df = self.df.dropna()

    def convert_m_to_grams(self, column):
        """
        Check if it has 'm' after removing 'g'.
        If it does, convert it to grams (multiply by 1000) and remove 'm'.
        """
        # Remove 'g' from the column first
        self.df[column] = self.df[column].str.replace("g", "", regex=False)
        self.strip_spaces(column)

        # Convert entries with 'm' to grams by / by 1000 and remove 'm'
        self.df[column] = self.df[column].apply(
            lambda x: float(x.replace("m", "")) / 1000 if "m" in str(x) else x
        )

        self.to_float(column)

    def convert_units(self, column):
        """
        Check if it has 'm' after removing 'g'.
        If it does, convert it to grams (multiply by 1000) and remove 'm'.
        """
        units = {
            ("mg", "g"): 1 / 1000,
            # ("ml", "l"): 1/1000,
            # ("l", "ml"): 1000,
            ("fl oz", "ml"): 29.5735,
            ("cup", "ml"): 240,
            ("cups", "ml"): 240,
            ("ml", "ml"): 1,
        }

        # if (start_unit.lower(), end_unit.lower()) not in units:
        #     raise KeyError("start to end unit not found")

        self.strip_spaces(column)

        # Convert entries with 'm' to grams by / by 1000 and remove 'm'
        # self.df[column] = self.df[column].apply(
        #     lambda x: float(x.replace(key[0], '')) * value if key[0] in str(x) else x
        # )

        for key, value in units.items():
            print(str(key[0]) + ": " + str(value))
            self.df[column] = self.df[column].apply(
                lambda x: (
                    float(x.replace(key[0], "")) * value
                    if key[0].lower() == str(x.lower())[-(len(key[0])) :]
                    else x
                )
            )
            # self.df[column] = self.df[column].apply(
            #     lambda x: float(x.replace(key[0], '')) * value if str(x).endswith(key[0]) else x
            # )

        self.to_float(column)

    def to_list(self, column):
        res = self.df[column].tolist()
        return res

    def convert_fl_oz_to_ml(self, column):
        """
        Converts values in a specified column from ounces (oz/fl oz) to milliliters (mL).
        :param column: The column name to process.
        """

        def convert(value):
            if isinstance(value, str):
                match = re.search(
                    r"([\d]+(?:\.\d+)?)\s*(?:fl oz|fl. oz|fl. oz.|fluid ounces|Fluid ounce|floz/)",
                    value,
                    re.IGNORECASE,
                )
                if match:
                    try:
                        fl_oz = float(match.group(1))
                        ml = fl_oz * 29.5735  # Convert to mL
                        return f"{ml:.2f} ml"
                    except ValueError:
                        return value  # Return original value if conversion failed
            return value  # Return original value if no conversion is needed

        self.df[column] = self.df[column].apply(convert)

    def convert_oz_to_g(self, column):
        """
        Converts values in a specified column from ounces (oz) to grams (g).
        :param column: The column name to process.
        """

        def convert(value):
            if isinstance(value, str):
                match = re.search(
                    r"([\d]+(?:\.\d+)?)\s*(?:oz|ounces|oz.|Oz.|OZ|ounce)",
                    value,
                    re.IGNORECASE,
                )
                if match:
                    try:
                        ounces = float(match.group(1))
                        grams = ounces * 28.3495  # Convert to g
                        return f"{grams:.2f} g"
                    except ValueError:
                        return value  # Return original value if conversion fails
            return value  # Return original value if no conversion is needed

        self.df[column] = self.df[column].apply(convert)

    def clean_bracketed_values(self, column):
        """
        Pre-process the bracketed values by ignoring (s) or (es) before extracting other values in parentheses.
        This method modifies the "column" by cleaning values like 'tablet(s)' to 'tablets'.
        """

        def clean(value):
            if isinstance(value, str):
                # Remove only (s) or (es) at the end of a word
                value = re.sub(r"\((s|es)\)", "", value, flags=re.IGNORECASE).strip()
            return value  # Return cleaned string

        # Apply the function to the column
        self.df[column] = self.df[column].apply(clean)

    def extract_bracketed_value(self, column):

        def extract(value):
            if isinstance(value, str):
                match = re.search(r"\(([^)]+)\)", value)  # Find text inside parentheses
                if match:
                    extracted = match.group(1).strip()  # Extract and strip whitespace
                    return extracted  # Return extracted value
            return value  # Return original value if no valid match

        self.df[column] = self.df[column].apply(extract)

    def convert_package_based_size(self, column):
        # Define mappings of known units to approximate values
        unit_mapping = {
            "can": "355 ml",
            "bottle": "500 ml",
            "box": "250 g",
            "container": "300 g",
            "bagel": "100 g",
            "slice": "30 g",
            "biscuit": "58 g",
            "breadstick": "30 g",
            "apple": "150 g",
            "k-cup": "10 g",
            "pan fried slice": "40 g",
            "stick": "65 g",
            "pod": "10 g",
            "packet": "3.3 g",
            "tea bag": "8 fl oz",
            "teabag": "8 fl oz",
        }

        def convert(value):
            if isinstance(value, str):
                value_lower = value.lower().strip()

                # Regex to match cases like "1 K-Cup" or "1.0 tea bag"
                match = re.match(r"(\d*\.?\d*)?\s*([\w\s-]+)", value_lower)
                if match:
                    quantity = (
                        float(match.group(1)) if match.group(1) else 1
                    )  # Default to 1 if missing
                    unit = match.group(2).strip().lower()

                    # Iterate through the unit mapping to find a match
                    for key in unit_mapping:
                        if key in unit:
                            base_value = unit_mapping[key]

                            # Extract numeric part from mapping
                            base_match = re.match(
                                r"(\d*\.?\d*)\s*([a-zA-Z\s]+)", base_value
                            )
                            if base_match:
                                base_quantity = float(base_match.group(1))
                                base_unit = base_match.group(2).strip()

                                # Convert value by scaling quantity
                                converted_value = (
                                    f"{int(quantity * base_quantity)} {base_unit}"
                                )
                                return converted_value

            return value  # Return original value if no match found

        self.df[column] = self.df[column].apply(convert)

    def convert_cups_to_ml(self, column):
        def convert(value):
            match = re.search(r"([\d\.]+)\s*(?:cup|cups)", str(value), re.IGNORECASE)
            if match:
                cups = float(match.group(1))
                return f"{cups * 240} ml"
            return value  # Return original value if no match

        self.df[column] = self.df[column].apply(convert)

    def convert_tbsp_to_g(self, column):

        def convert(value):
            match = re.search(
                r"([\d\.]+)\s*(?:tbsp|tablespoon|tablespoons|tbs)",
                str(value),
                re.IGNORECASE,
            )
            if match:
                tbsp = float(match.group(1))
                return f"{tbsp * 21.25} g"
            return value  # Return original value if no match

        self.df[column] = self.df[column].apply(convert)

    def standardize_column(self, column_name):
        """
            Creates a new column standardizing a specified numerical column to a per-100g or per-100ml basis.

            The new column will be named '<column_name> per 100g' or '<column_name> per 100ml'.

        :param column_name: The column to standardize.
        """
        if "servingsize" not in self.df.columns:
            raise ValueError("The DataFrame must contain a 'servingsize' column.")

        if column_name not in self.df.columns:
            raise ValueError(f"Column '{column_name}' not found in DataFrame.")

        # Extract only numeric values from servingsize using regex
        self.df["servingsize_numeric"] = (
            self.df["servingsize"]
            .astype(str)
            .apply(
                lambda x: (
                    float(re.findall(r"\d+", x)[0]) if re.findall(r"\d+", x) else None
                )
            )
        )

        # print(self.df["servingsize_numeric"])

        # Convert the target column to numeric
        self.df[column_name] = pd.to_numeric(self.df[column_name], errors="coerce")

        # Define new column name
        new_column_name = f"{column_name} per 100"

        # Perform calculation
        self.df[new_column_name] = (
            self.df[column_name] / self.df["servingsize_numeric"]
        ) * 100

        # Replace inf values safely
        self.df[new_column_name] = self.df[new_column_name].replace(
            [float("inf"), -float("inf")], None
        )

        # Drop temporary numeric column
        self.df.drop(columns=["servingsize_numeric"], inplace=True)

    def flag_ultra_processed(self, ingredients_column, ultra_processed_ingredients):
        """
        Flags products as ultra-processed if their ingredient list contains any ultra-processed ingredient.

        Args:
        ingredients_column (str): The column name that contains ingredient lists.
        ultra_processed_ingredients (list): List of ultra-processed ingredients to check against.
        """
        # Convert list to lowercase for case-insensitive matching
        ultra_processed_set = set(
            ingredient.lower() for ingredient in ultra_processed_ingredients
        )

        # Function to check if any ultra-processed ingredient is in the row's ingredient list
        def check_ultra_processed(ingredient_list):
            if pd.isna(ingredient_list):  # Handle NaN values
                return 0
            ingredient_list = [
                i.strip().lower() for i in ingredient_list.split(",")
            ]  # Convert to lowercase list
            return (
                1
                if any(
                    ingredient in ultra_processed_set for ingredient in ingredient_list
                )
                else 0
            )

        # Apply function to self.df
        self.df["ultra_processed_flag"] = self.df[ingredients_column].apply(
            check_ultra_processed
        )
        
        self.df.to_excel('data/Cleaned_Product_List_1.xlsx', index=False)

    def flag_high_sugar(
        self,
        ingredients_column,
        total_sugar_column,
        product_aisle_column,
        high_sugar_ingredients,
    ):
        """
        Flags products as high sugar based on their ingredient list and total sugar content.

        Conditions:
        - If an ingredient in the product matches any in the high_sugar_ingredients list, it is flagged.
        - If it's a beverage (contains 'beverage' OR 'tea' in the product aisle column) and has Total sugar >= 5g/100ml, it is flagged.
        - If it's a food (not a beverage) and has Total sugar >= 10g/100g, it is flagged.

        """

        # Convert high-sugar ingredient list to lowercase for case-insensitive matching
        high_sugar_set = set(
            ingredient.lower() for ingredient in high_sugar_ingredients
        )

        def check_high_sugar(row):
            ingredient_list = row[ingredients_column]
            total_sugar = row[total_sugar_column]
            product_aisle = row[product_aisle_column]

            # Check if the ingredient list contains high-sugar ingredients
            if pd.notna(ingredient_list):  # Handle NaN values
                ingredient_list = [
                    i.strip().lower() for i in ingredient_list.split(",")
                ]
                has_high_sugar_ingredient = any(
                    ingredient in high_sugar_set for ingredient in ingredient_list
                )
            else:
                has_high_sugar_ingredient = False

            # Determine if the product is a beverage (only if "beverage" or "tea" appears in the product aisle column)
            is_beverage = isinstance(product_aisle, str) and any(
                x in product_aisle.lower() for x in ["beverage", "tea"]
            )

            # Check if sugar content exceeds the threshold
            if pd.notna(total_sugar):  # Handle NaN values
                if isinstance(total_sugar, (int, float)):  # Ensure it's numeric
                    high_sugar_threshold = (
                        5 if is_beverage else 10
                    )  # 5g/100ml for beverages, 10g/100g for food
                    exceeds_sugar_limit = total_sugar >= high_sugar_threshold
                else:
                    exceeds_sugar_limit = False
            else:
                exceeds_sugar_limit = False

            # Flag as high sugar (1) if either condition is met, else 0
            return 1 if has_high_sugar_ingredient or exceeds_sugar_limit else 0

        # Apply function to each row
        self.df["high_sugar_flag"] = self.df.apply(check_high_sugar, axis=1)

    def flag_high_saturated_fat(
        self,
        ingredients_column,
        sat_fat_column,
        product_aisle_column,
        high_sat_fat_ingredients,
    ):
        """
        Flags products as high in saturated fat based on their ingredient list and total saturated fat content.

        Conditions:
        - If an ingredient in the product matches any in high_sat_fat_ingredients, it is flagged.
        - If it's a beverage (contains 'beverage' OR 'tea' in the product aisle column) and has Total Sat Fat >= 3g/100ml, it is flagged.
        - If it's a food (not a beverage) and has Total Sat Fat >= 4g/100g, it is flagged.
        """

        # Convert high-saturated-fat ingredient list to lowercase for case-insensitive matching
        high_sat_fat_set = set(
            ingredient.lower() for ingredient in high_sat_fat_ingredients
        )

        def check_high_sat_fat(row):
            ingredient_list = row[ingredients_column]
            total_sat_fat = row[sat_fat_column]
            product_aisle = row[product_aisle_column]

            # Check if the ingredient list contains high-saturated-fat ingredients
            if pd.notna(ingredient_list):  # Handle NaN values
                ingredient_list = [
                    i.strip().lower() for i in ingredient_list.split(",")
                ]
                has_high_sat_fat_ingredient = any(
                    ingredient in high_sat_fat_set for ingredient in ingredient_list
                )
            else:
                has_high_sat_fat_ingredient = False

            # Determine if the product is a beverage (if "beverage" or "tea" is in the product aisle)
            is_beverage = isinstance(product_aisle, str) and any(
                x in product_aisle.lower() for x in ["beverage", "tea"]
            )

            # Check if saturated fat content exceeds the given threshold
            if pd.notna(total_sat_fat):  # Handle NaN values
                if isinstance(total_sat_fat, (int, float)):  # Ensure it's numeric
                    high_sat_fat_threshold = (
                        3 if is_beverage else 4
                    )  # 3g/100ml for beverages, 4g/100g for food
                    exceeds_sat_fat_limit = total_sat_fat >= high_sat_fat_threshold
                else:
                    exceeds_sat_fat_limit = False
            else:
                exceeds_sat_fat_limit = False

            # Flag as high in saturated fat (1) if either condition is met, else 0
            return 1 if has_high_sat_fat_ingredient or exceeds_sat_fat_limit else 0

        # Apply function to each row
        self.df["high_saturated_fat_flag"] = self.df.apply(check_high_sat_fat, axis=1)

    def flag_high_calories(self, calories_column, product_aisle_column):
        """
        Flags products as high in calories based on total calories per 100g or 100ml.

        Conditions:
        - If it's a beverage (contains 'beverage' OR 'tea' in the product aisle column) and has Total Calories >= 100 kcal/100ml, it is flagged.
        - If it's a food (not a beverage) and has Total Calories >= 275 kcal/100g, it is flagged.

        Args:
        calories_column (str): Column containing total calories per 100g/ml.
        product_aisle_column (str): Column specifying if the product is a beverage.
        """

        def check_high_calories(row):
            total_calories = row[calories_column]
            product_aisle = row[product_aisle_column]

            # Determine if the product is a beverage (if "beverage" or "tea" is in the product aisle)
            is_beverage = isinstance(product_aisle, str) and any(
                x in product_aisle.lower() for x in ["beverage", "tea"]
            )

            # Set the calorie threshold based on product type
            high_calorie_threshold = (
                100 if is_beverage else 275
            )  # 100 kcal/100ml for beverages, 275 kcal/100g for food

            # Check if calorie content exceeds the threshold
            if pd.notna(total_calories):  # Handle NaN values
                if isinstance(total_calories, (int, float)):  # Ensure it's numeric
                    exceeds_calorie_limit = total_calories >= high_calorie_threshold
                else:
                    exceeds_calorie_limit = False
            else:
                exceeds_calorie_limit = False

            # Flag as high calorie (1) if it exceeds the threshold, else 0
            return 1 if exceeds_calorie_limit else 0

        # Apply function to each row
        self.df["high_calories_flag"] = self.df.apply(check_high_calories, axis=1)

    def flag_high_sodium(
        self,
        ingredients_column,
        sodium_column,
        product_aisle_column,
        high_sodium_ingredients,
    ):
        """
        Flags products as high in sodium if they contain high-sodium ingredients OR exceed sodium limits.

        Conditions:
        - If it's a beverage (contains 'beverage' OR 'tea' in the product aisle column) and Total Sodium ≥ 100 mg/100ml (0.1 g/100ml), it is flagged.
        - If it's a food (not a beverage) and Total Sodium ≥ 400 mg/100g (0.4 g/100g), it is flagged.
        - If it contains any high-sodium ingredients from the provided list, it is flagged.


        """

        # Convert ingredient list to lowercase for case-insensitive matching
        high_sodium_set = set(
            ingredient.lower() for ingredient in high_sodium_ingredients
        )

        def check_high_sodium(row):
            # Get ingredient list, sodium content, and product aisle
            ingredient_list = row[ingredients_column]
            # total_sodium_g = row[sodium_column]
            # Ensure that sodium is casted to numeric instead of string
            total_sodium_g = pd.to_numeric(row[sodium_column], errors="coerce")
            product_aisle = row[product_aisle_column]

            # Convert sodium from grams to mg
            total_sodium_mg: int = (
                total_sodium_g * 1000 if pd.notna(total_sodium_g) else 0
            )

            # Determine if the product is a beverage (if "beverage" or "tea" is in the product aisle)
            is_beverage = isinstance(product_aisle, str) and any(
                x in product_aisle.lower() for x in ["beverage", "tea"]
            )

            # Set sodium threshold based on food vs. beverage
            high_sodium_threshold: int = (
                100 if is_beverage else 400
            )  # 100 mg/100ml for beverages, 400 mg/100g for food

            # Check if sodium content exceeds the threshold
            exceeds_sodium_limit: bool = (
                total_sodium_mg >= high_sodium_threshold
                if pd.notna(total_sodium_mg)
                else False
            )

            # Check if any high-sodium ingredient is present
            contains_high_sodium_ingredient = False
            if pd.notna(ingredient_list):
                ingredient_list = [
                    i.strip().lower() for i in ingredient_list.split(",")
                ]
                contains_high_sodium_ingredient = any(
                    ingredient in high_sodium_set for ingredient in ingredient_list
                )

            # Flag as high sodium (1) if it exceeds the threshold OR contains high-sodium ingredients, else 0
            return 1 if exceeds_sodium_limit or contains_high_sodium_ingredient else 0

        # Apply function to self.df
        self.df["high_sodium_flag"] = self.df.apply(check_high_sodium, axis=1)

    def save_csv(self, output_path="export.csv"):
        """Export current pandas dataframe in CSV formart."""
        self.df.to_csv(output_path, index=False)

    def num_rows(self):
        return self.df.shape[0]

    def num_cols(self):
        return self.df.shape[1]

    def extract_and_convert_weight(self):
        """
        Extracts the weight in grams (g) or ounces (oz) from the 'product' column.
        If ounces (oz) is found, it converts it to grams (g).

        This function will create two new columns:
        - 'weight_grams': Extracted weight in grams (converted if necessary).
        - 'weight_oz': Extracted weight in ounces (if found).
        """

        def extract_and_convert_weight_from_product(product_name):
            """
            Extracts weight from the product description in either grams (g) or ounces (oz).
            If ounces is found, it converts the weight to grams.

            :param product_name: The product description as a string.
            :return: A tuple (grams, ounces), where each is a numeric value or None.
            """
            # Conversion factor from ounces to grams
            OZ_TO_GRAMS = 28.3495

            grams = None
            ounces = None

            # Regex to extract grams (g or grams) from the product description
            grams_match = re.search(
                r"(\d+\.?\d*)\s*(g|grams)", product_name, re.IGNORECASE
            )
            # Regex to extract ounces (oz or ounces) from the product description
            oz_match = re.search(
                r"(\d+\.?\d*)\s*(oz|ounces)", product_name, re.IGNORECASE
            )

            # If grams is found, extract and store the value
            if grams_match:
                grams = float(grams_match.group(1))

            # If ounces is found, extract and convert to grams
            if oz_match:
                ounces = float(oz_match.group(1))
                grams = ounces * OZ_TO_GRAMS  # Convert ounces to grams

            return grams, ounces

        # Apply the extraction and conversion function to the 'product' column
        self.df[["weight_grams", "weight_oz"]] = self.df["product_name"].apply(
            lambda x: pd.Series(extract_and_convert_weight_from_product(x))
        )

    def standardize_serving_size_g(self, product, serving_size):
        units = ["g", "grams", "oz"]

    def flag_nns(self, ingredients_column, nns_ingredients):
        """
        Flags products as containing nns.

        Conditions:
        - If the product's ingredient list contains any of the nns ingredients it's classified as nns

        Args:
        ingredients_column (str): Column containing the list of ingredients each product uses.
        nns_ingredients (str): List containing all ingredients classified as nns.
        """
        # Convert list to lowercase for case-insensitive matching
        nns_ingredients_set = set(ingredient.lower() for ingredient in nns_ingredients)

        # Function to check if any nns ingredient is in the row's ingredient list
        def check_nns(ingredient_list):
            if pd.isna(ingredient_list):  # Handle NaN values
                return 0
            ingredient_list_lower = [
                i.strip().lower() for i in ingredient_list.split(",")
            ]  # Convert to lowercase list
            return (
                1
                if any(
                    ingredient in nns_ingredients_set
                    for ingredient in ingredient_list_lower
                )
                else 0
            )

        # Apply function to self.df
        self.df["nns_flag"] = self.df[ingredients_column].apply(check_nns)

    def extract_blank_rows(self, column):
        self.df = self.df[self.df[column].isna()]

    def standardize_nutrient_columns(self):
        nutrient_columns = [
            "energykcal",
            "fat",
            "saturatedfat",
            "transfat",
            "carbohydrates",
            "sugar",
            "salt",
            "fibre",
            "protein",
        ]
        columns_per_100 = [f"{col} per 100" for col in nutrient_columns]
        self.df.loc[self.df[nutrient_columns].sum(axis=1) == 0, columns_per_100] = 0

    def extract_serving_from_product(self, product_value):
        """
        Extracts serving size from product column, handling different placements and formats.
        """
        if isinstance(product_value, str):
            print("is string")
            # Improved regex to capture more variations of units
            match = re.search(
                r"(\d*\.?\d+)\s*(fl\.?\s*oz|fluid ounce|oz|ml|quart|liter|g|kg|tablet|scoop|cup|bag|bottle)",
                product_value,
                re.IGNORECASE,
            )
            if match:
                return f"{match.group(1)} {match.group(2).replace('fluid ounce', 'fl oz').replace('liter', 'l').replace('kg', 'g')}"  # Normalize units
        return None  # No match found

    def fill_serving_size(self, product_column, serving_size_column):
        """
        Fills missing serving sizes using product column if available.
        """
        self.df[serving_size_column] = self.df[serving_size_column].apply(
            lambda x: (
                x
                if pd.isna(x)
                else self.extract_serving_from_product(self.df[product_column])
            )
        )

    def convert_tsp_to_g(self, column):
        def convert(value):
            match = re.search(
                r"([\d\.]+)\s*(?:tsp|teaspoon|tsp.)", str(value), re.IGNORECASE
            )
            if match:
                tsp = float(match.group(1))
                return f"{tsp * 5.69} g"
            return value  # Return original value if no match

        self.df[column] = self.df[column].apply(convert)

    def convert_l_to_ml(self, column):
        def convert(value):
            match = re.search(
                r"([\d\.]+)\s*(?:l|liter|liter.|liters|liters.|l.|L|L.)",
                str(value),
                re.IGNORECASE,
            )
            if match:
                l = float(match.group(1))
                return f"{l * 1000} ml"
            return value  # Return original value if no match

        self.df[column] = self.df[column].apply(convert)

    def convert_mg_to_g(self, column):
        def convert(value):
            match = re.search(r"([\d\.]+)\s*(?:mg)", str(value), re.IGNORECASE)
            if match:
                mg = float(match.group(1))
                return f"{mg / 1000} g"
            return value  # Return original value if no match

        self.df[column] = self.df[column].apply(convert)

    def convert_weird_g(self, column):
        def convert(value):
            match = re.search(
                r"([\d\.]+)\s*(?:g mix|gram|g without shells)",
                str(value),
                re.IGNORECASE,
            )
            if match:
                val = float(match.group(1))
                return f"{val} g"
            return value  # Return original value if no match

        self.df[column] = self.df[column].apply(convert)

    def price_per_container(self):
        # Convert the target column to numeric
        self.df["servingspercontainer_clean"] = (
            self.df["servingspercontainer"]
            .astype(str)
            .str.extract(r"(\d*\.?\d+)")
            .astype(float)
        )
        self.df["price_per_serving"] = (
            self.df["price"] / self.df["servingspercontainer_clean"]
        )
        self.df.drop(columns=["servingspercontainer_clean"], inplace=True)
        
    def parse_product_name(self, product_name: str):
        """
        Extracts pack quantity, unit size, and units per pack from product name strings.

        Returns:
            dict with keys: 
            {
                "pack_unit": int or None,
                "unit_size": str or None,
                "pack_size": int or None
            }
        """
        result = {
            "pack_unit": None,
            "unit_size": None,
            "pack_size": None
        }
        
        text = product_name.lower()

        # --- 1. Extract pack quantity ---
        pack_unit_patterns = [
            r"\s*bottle",          # " bottle"
            r"\s*cans",           # " cans"
            r"bottles",            # "bottles"
            r"cans",               # "cans"
            r"bottle",             # "bottle"
            r"glass",          # glass
        ]
        servings_per_container_patterns = [
            r"pack of\s*(\d+)",       # "Pack of 2"
            r"Pack of\s*(\d+)",        # "Pack of 2"
            r"(\d+)\s*pack",          # "2 Pack" or "12-Pack"
            r"(\d+)\s*count",         # "2 Count"
            r"(\d+)\s*ct",             # "2ct"
            r"Case of\s*(\d+)",        # "Case of 2"
            r"(/d+)\s*drinks",          # "2 drinks"
            r"(\d+)\s*pk",              # "2 pk
        ]
        # package_patterns = [
        #     r"(\d+(?:\.\d+)?\s*(?:fl oz|oz|liter|litre|l|ml))(?:\s*,?\s*(\d+\s*pack)?)?", # "12 fl oz, 12 pack"
        #     r"(\d+(?:\.\d+)?\s*x\s*(?:fl oz|oz|liter|litre|l|ml))\s*\((?:pack\s*of\s*)?\d+\)", # "12 fl oz (pack of 12)"
        #     r"(\d+(?:\.\d+)?\s*(?:fl oz|oz|liter|litre|l|ml)),?\s*(pack\s*of\s*)?\d+", # "12.0 fl oz, pack of 12"
        #     r"(\d+(?:\.\d+)?\s*pack)", # "12 pack"
        #     r"(\d+(?:\.\d+)?\s*(?:fl oz|oz|liter|litre|l|ml)),?\s*(\d+-pack)", # "11.2 oz, 3-pack"
        #     r"(\d+(?:\.\d+)?\s*Fluid Ounces)", # "12 Fluid Ounces"
        #     r"(\d+\s*Pack\s*-\s*\d+(?:\.\d+)?\s*(?:fl oz|oz|liter|litre|l|ml))", # "8 Pack - 16 OZ"
        #     r"(\d+(?:\.\d+)?\s*-\s*\d+(?:\.\d+)?\s*(?:fl oz|oz|liter|litre|l|ml))", # "12- 16 fl oz"
        #     r"(\d+(?:\.\d+)?\s*(?:fl oz|oz|liter|litre|l|ml))\s*x\s*\d+\s*(?:bottles?)" # "2.0 fl oz x 2 bottles"
        #     r"(\d+(?:\.\d+)?\s*(?:fl oz|oz|liter|litre|l|ml))\s*Cans?,?\s*(\d+\s*pk)", # "12 oz Cans, 12 pk"
        # ]
        unit_patterns = [
            r"(\d+(\.\d+)?)\s*(fl oz|oz|liter|litre|l|ml)",
        ]
        
        # --- 2. Extract pack_unit ---
        for pattern in pack_unit_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result["pack_unit"] = match.group(0)
                break  
        # If none found, assume "Single" if text has "single"
        if result["pack_unit"] is None or "single" in text:
            result["pack_unit"] = "Single"

        # --- 4. Extract servings_per_container ---
        for pattern in servings_per_container_patterns:
            serving_per_match = re.search(pattern, text, re.IGNORECASE)
            if serving_per_match:
                result["pack_size"] = serving_per_match.group(0).strip()
                break
        if result['pack_size'] is None:
            result['pack_size'] = 1
            
        # --- 3. Extract unit_size ---
        nested_pattern = r"(\d+(\.\d+)?)\s*(?:fl oz|oz|liter|litre|l|ml|Fluid Ounces)"
        nested_match = re.search(nested_pattern, text, re.IGNORECASE)
        if nested_match:
            result["unit_size"] = nested_match.group(0).strip()     # e.g., "12 fl oz"
    
            
        return result
    
    def apply_parse_product_name(self, column):
        parsed_data = self.df[column].apply(self.parse_product_name)
        self.df[['pack_unit', 'unit_size', 'pack_size']] = pd.json_normalize(parsed_data)
        return

    def find_serving_info(self, column):
        self.df["serving_size"] = self.df[column].apply(str).apply(
            lambda text: 
                re.search(r"(\d+(?:\.\d+)?\s*(?:fl oz|grams|g))", text, re.IGNORECASE)
                or re.search(r"\d+(?:\.\d+)?\s*ml", text, re.IGNORECASE)
        ).apply(lambda match: match.group(0).strip() if match else None)

    
    def nutr_per_100(self, column):
        self.df[column] = self.df[column].str.replace("%", "", regex=False)
        return
    
    