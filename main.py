import pandas as pd
from analysis import analyze_nutrients, analyze_unhealthy_foods, correlation_analysis
import chart

def main():
    df = pd.read_csv("merged_food_data.csv")

    # Copy df for unhealthy analysis (full nutrient set)
    df_full = df.copy()

    top10_muscle, top10_fatloss, top10_nonzero = analyze_nutrients(df)
    analyze_unhealthy_foods(df)

    correlation_analysis(df_full)

    chart.bar_chart(
        df = top10_nonzero,
        column = "Carbohydrate_to_Protein_Ratio",
        title = "Top 10 Foods for Fat Loss (Non-zero Carbohydrates)",
        xlabel = "Carb/Protein Ratio",
        ylabel = "Food Name"
    )

    chart.bar_chart(
        df = top10_muscle,
        column = "Protein_to_Calorie_Ratio",
        title = "Top 10 Foods for Muscle Building",
        xlabel = "Protein/Calorie Ratio",
        ylabel ="Food Name",
    )

    chart.bar_chart(
        df=top10_muscle,
        column="Protein_to_Fat_Ratio",
        title="Top 10 Foods for Muscle Building",
        xlabel="Protein/Fat Ratio",
        ylabel="Food Name",
    )

if __name__ == "__main__":
    main()