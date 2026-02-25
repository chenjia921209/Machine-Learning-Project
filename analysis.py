import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def analyze_nutrients(df):

    # filter the nutrient columns that we want to analyze
    target_nutrients = ["Fat", "Protein", "Carbohydrates"]
    new_columns = ["food", "Caloric Value"] + target_nutrients
    df = df[new_columns]

    print("Example data:")
    print(df.head(5).to_string(index=False))
    print("\n")
          

    """ calculate ratios for nutrient analysis """
    # Remove rows with non-positive values in key columns to avoid division by zero
    df = df[(df["Caloric Value"] > 0) & (df["Protein"] > 0) & (df["Fat"] > 0)]

    #1. Calculate the protein-to-calorie ratio (better for muscle building)
    df["Protein_to_Calorie_Ratio"] = np.divide(df["Protein"], df["Caloric Value"])

    #2. calculate the protein to fat ratio (better for muscle building)
    df["Protein_to_Fat_Ratio"] = np.divide(df["Protein"], df["Fat"])
                                        
    #3.calculate the carbohydrate to protein ratio (better for body fat reduction)
    df["Carbohydrate_to_Protein_Ratio"] = np.divide(df["Carbohydrates"], df["Protein"]) 


    # find top 10 foods for muscle building and fat loss people
    top10_for_fat_loss = df.sort_values(by="Carbohydrate_to_Protein_Ratio").head(10)               
    top10_for_muscle_building = df.sort_values(by=["Protein_to_Calorie_Ratio", "Protein_to_Fat_Ratio"], ascending=False).head(10) #ascending=False for descending order
    # Exclude foods with zero carbohydrates for fat loss analysis
    top10_for_fat_loss_nonzero = df[df["Carbohydrates"] > 0].sort_values(by="Carbohydrate_to_Protein_Ratio").head(10)

    # Display the results

    # Create a formatted table to make it more readable
    column_mapping_muscle = {
        "food": "Food Name",
        "Caloric Value": "Calories",
        "Fat": "Fat(g)",
        "Protein": "Protein(g)",
        "Protein_to_Calorie_Ratio": "Protein/Calorie",
        "Protein_to_Fat_Ratio": "Protein/Fat"
    }
    display_columns_muscle = [
        "Food Name", 
        "Calories", 
        "Fat(g)", 
        "Protein(g)", 
        "Protein/Calorie", 
        "Protein/Fat"
    ]

    display_table(
        df = top10_for_muscle_building, 
        title = "Top 10 foods in this dataset for muscle building:", 
        columns_mapping = column_mapping_muscle, 
        display_columns = display_columns_muscle
    )

    columns_mapping_fat_loss = {
        "food": "Food Name",
        "Caloric Value": "Calories",
        "Carbohydrates": "Carbohydrates(g)",
        "Protein": "Protein(g)",
        "Carbohydrate_to_Protein_Ratio": "Carbohydrates/Protein"
    }
    display_columns_fat_loss = [
        "Food Name", 
        "Calories", 
        "Carbohydrates(g)", 
        "Protein(g)", 
        "Carbohydrates/Protein", 
    ]

    display_table(
        df = top10_for_fat_loss, 
        title = "Top 10 food in this dataset for fat loss", 
        columns_mapping = columns_mapping_fat_loss, 
        display_columns = display_columns_fat_loss
    )
    display_table(
        df = top10_for_fat_loss_nonzero, 
        title = "Top 10 food in this dataset for fat loss (excluding zero carbohydrate foods like seafood):",
        columns_mapping =  columns_mapping_fat_loss, 
        display_columns = display_columns_fat_loss
    )

    # Summary statistics for nutrient ratios
    print("\nSummary statistics for nutrient ratios:")
    print(df[["Protein_to_Calorie_Ratio", "Carbohydrate_to_Protein_Ratio", "Protein_to_Fat_Ratio"]].describe().round(3))

    print("\n")

    return top10_for_muscle_building, top10_for_fat_loss, top10_for_fat_loss_nonzero

def analyze_unhealthy_foods(df):
    '''based on FDA guidelines
    suger <= 1 - 5g
    sodium <= 230mg
    satuated fat <= 2g
    satuated fat /total fat >=0.2
    '''
    # filter the nutrient columns that we want to analyze
    target_nutrients = ["Saturated Fats", "Sugars", "Fat", "Sodium"]
    new_columns = ["food", "Caloric Value"] + target_nutrients
    df = df[new_columns]

    # filter out unhealthy foods first baaed on FDA guidelines
    df = df.copy()
    df = df[
        (df["Sugars"] > 5) |
        (df["Sodium"] > 230/1000) |
        (df["Saturated Fats"] > 2) |
        (df["Saturated Fats"] / df["Fat"] > 0.2)
    ]

    print("Example data:")
    print(df.head(5).to_string(index=False))
    print("\n")

    """ calculate unhealthy nutrient densities and use max normalization to compute unhealthy score """
    max_sugar = df['Sugars'].max()
    max_sat_fat = df['Saturated Fats'].max()
    max_sodium = df['Sodium'].max()

    # normalize the unhealthy nutrients
    df['Sugar_norm'] = df['Sugars'] / max_sugar
    df['Saturated_Fat_norm'] = df['Saturated Fats'] / max_sat_fat
    df['Sodium_norm'] = df['Sodium'] / max_sodium

    # compute unhealthy score as normalized values
    df['unhealthy_score'] = (df['Sugar_norm'] + df['Saturated_Fat_norm'] + df['Sodium_norm']) 

    # Minimum Caloric Value (per 100g) to be considered in 'unhealthy' ranking
    df = df[(df["Caloric Value"] > 100)] 

    # calculate unhealthy nutrient densities
    df["Sugar_Density"] = np.divide(df["Sugars"], df["Caloric Value"])
    df["Saturated_Fat_Density"] = np.divide(df["Saturated Fats"], df["Caloric Value"])
    df['Sodium_Density'] = np.divide(df['Sodium'], df['Caloric Value'])

    # find top 10 unhealthy foods based on sugar density, saturated fat density and carbohydrate density
    top10_unhealthy_foods = df.sort_values(by="unhealthy_score", ascending=False).head(10)


    top10_high_sugar = df.sort_values(by="Sugar_Density", ascending=False).head(10)
    top10_high_saturated_fat = df.sort_values(by="Saturated_Fat_Density", ascending=False).head(10)
    top10_high_sodium = df.sort_values(by="Sodium_Density", ascending=False).head(10)

    columns_mapping_sugar = {
        "food": "Food Name",
        "Caloric Value": "Calories",
        "Sugars": "Sugars(g)",
        "Sugar_Density": "Sugar/Calorie"
    }
    display_columns_sugar = [
        "Food Name", 
        "Calories", 
        "Sugars(g)", 
        "Sugar/Calorie"
    ]
    display_table(
        df = top10_high_sugar,
        title = "Top 10 foods in this dataset with highest Sugar Density:",
        columns_mapping = columns_mapping_sugar,
        display_columns = display_columns_sugar,
    )

    columns_mapping_saturated_fat = {
        "food": "Food Name",
        "Caloric Value": "Calories",
        "Saturated Fats": "Saturated Fats(g)",
        "Saturated_Fat_Density": "Saturated Fat/Calorie"
    }
    display_columns_saturated_fat = [
        "Food Name",
        "Calories",
        "Saturated Fats(g)",
        "Saturated Fat/Calorie"
    ]
    display_table(
        df = top10_high_saturated_fat,
        title = "Top 10 foods in this dataset with highest Saturated Fat Density:",
        columns_mapping = columns_mapping_saturated_fat,
        display_columns = display_columns_saturated_fat,
    )

    columns_mapping_sodium = {
        "food": "Food Name",
        "Caloric Value": "Calories",
        "Sodium": "Sodium(g)",
        "Sodium_Density": "Sodium/Calorie"
    }
    display_columns_sodium = [
        "Food Name",
        "Calories",
        "Sodium(g)",
        "Sodium/Calorie"
    ]
    display_table(
        df = top10_high_sodium,
        title = "Top 10 foods in this dataset with highest Sodium Density:",
        columns_mapping = columns_mapping_sodium,
        display_columns = display_columns_sodium,
    )

    # Display the results
    columns_mapping_unhealthy = {
        "food": "Food Name",
        "Caloric Value": "Calories",
        "Sugars": "Sugars(g)",
        "Saturated Fats": "Saturated Fats(g)",
        "Sodium": "Sodium(g)",
        "unhealthy_score": "Unhealthy Score"
    }
    display_columns_unhealthy = [
        "Food Name", 
        "Calories", 
        "Sugars(g)", 
        "Saturated Fats(g)", 
        "Sodium(g)",
        "Unhealthy Score"
    ]

    display_table(
        df = top10_unhealthy_foods, 
        title = "Top 10 Unhealthy Foods in this dataset:", 
        columns_mapping = columns_mapping_unhealthy, 
        display_columns = display_columns_unhealthy,
    )
    
    # Summary statistics for unhealthy nutrient densities
    print("\nSummary statistics for unhealthy nutrient densities:")
    print(df[["Sugar_Density", "Saturated_Fat_Density", "Sodium_Density","unhealthy_score"]].describe().round(3))
    print("\n")

    # return top10_unhealthy_foods


def display_table(df, title, columns_mapping, display_columns):
    """ Display a formatted table with given title and column mappings """
    print(title)
    # select the most relevant columns and round to 3 decimal places
    table = df.rename(columns=columns_mapping)[display_columns].round(3)
    # display the table without index
    print(table.to_string(index=False))
    print("\n")

def correlation_analysis(df):
    """ Perform correlation analysis between different nutrients """
    corr_df = df[[
        "Protein",
        "Fat",
        "Carbohydrates",
        "Saturated Fats",
        "Sugars",
        "Sodium",
        "Caloric Value"
    ]].corr()


    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    plt.title("Correlation Heatmap of Nutrients")
    plt.show()

    print("\n")