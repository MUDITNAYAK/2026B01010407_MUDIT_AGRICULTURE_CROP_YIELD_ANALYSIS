"""Agriculture Crop Yield & Weather Impact Analysis.

Requires: pandas and numpy.
Run: python crop_yield_analysis.py [path/to/16_crop_yield.csv] [output_dir]

The script preserves every source row, imputes missing Rainfall_mm and Soil_pH
with each column's median, and records those actions in the output report.
Duplicate Farm_Record_ID rows are flagged rather than removed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

DEFAULT_INPUT = Path(r"C:\Users\acer\Downloads\16_crop_yield.csv")
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "crop_yield_results"

def markdown_table(frame: pd.DataFrame, digits: int = 2) -> str:
    """Format a dataframe as a compact Markdown table without extra packages."""
    view = frame.copy()
    for col in view.select_dtypes(include="number").columns:
        if pd.api.types.is_integer_dtype(view[col].dtype):
            view[col] = view[col].map(lambda x: "" if pd.isna(x) else f"{x:,d}")
        else:
            view[col] = view[col].map(lambda x: "" if pd.isna(x) else f"{x:,.{digits}f}")
    headers = [str(c) for c in view.columns]
    rows = [[str(v) for v in row] for row in view.itertuples(index=False, name=None)]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def main(input_path: Path, output_dir: Path) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"CSV not found: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(input_path)

    required = {
        "Farm_Record_ID", "Region", "Crop_Type", "Season", "Area_Hectares",
        "Production_Tons", "Rainfall_mm", "Fertilizer_kg_per_ha", "Soil_Type",
        "Soil_pH", "Irrigation",
    }
    missing_columns = required.difference(raw.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    df = raw.copy()
    numeric = ["Area_Hectares", "Production_Tons", "Rainfall_mm", "Fertilizer_kg_per_ha", "Soil_pH"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    missing_before = df.isna().sum()
    duplicate_id_mask = df["Farm_Record_ID"].duplicated(keep=False)
    duplicate_rows = df.loc[duplicate_id_mask].sort_values("Farm_Record_ID").copy()

    # Median imputation is robust to extreme values and retains all records.
    imputation = {}
    for col in ("Rainfall_mm", "Soil_pH"):
        median = df[col].median()
        imputation[col] = {"median": median, "count": int(df[col].isna().sum())}
        df[col] = df[col].fillna(median)

    valid_area = df["Area_Hectares"].gt(0)
    df["Yield_per_Hectare"] = np.where(
        valid_area, df["Production_Tons"] / df["Area_Hectares"], np.nan
    )
    df["Duplicate_Farm_Record_ID"] = duplicate_id_mask

    total_production = df["Production_Tons"].sum(min_count=1)
    average_yield = df["Yield_per_Hectare"].mean()

    crop = (df.groupby("Crop_Type", dropna=False)
            .agg(Records=("Farm_Record_ID", "size"), Total_Production_Tons=("Production_Tons", "sum"),
                 Average_Yield_per_Hectare=("Yield_per_Hectare", "mean"))
            .sort_values("Average_Yield_per_Hectare", ascending=False).reset_index())
    crop.insert(0, "Rank", np.arange(1, len(crop) + 1))
    region = (df.groupby("Region", dropna=False)
              .agg(Records=("Farm_Record_ID", "size"), Average_Yield_per_Hectare=("Yield_per_Hectare", "mean"),
                   Median_Yield_per_Hectare=("Yield_per_Hectare", "median"))
              .sort_values("Average_Yield_per_Hectare", ascending=False).reset_index())
    soil = (df.groupby("Soil_Type", dropna=False)
            .agg(Records=("Farm_Record_ID", "size"), Average_Yield_per_Hectare=("Yield_per_Hectare", "mean"),
                 Median_Yield_per_Hectare=("Yield_per_Hectare", "median"))
            .sort_values("Average_Yield_per_Hectare", ascending=False).reset_index())
    irrigation = (df.groupby("Irrigation", dropna=False)
                  .agg(Records=("Farm_Record_ID", "size"), Average_Yield_per_Hectare=("Yield_per_Hectare", "mean"),
                       Median_Yield_per_Hectare=("Yield_per_Hectare", "median"))
                  .sort_values("Average_Yield_per_Hectare", ascending=False).reset_index())

    corr_cols = ["Rainfall_mm", "Fertilizer_kg_per_ha", "Yield_per_Hectare"]
    correlations = df[corr_cols].corr(method="pearson")
    crop_season = (df.groupby(["Crop_Type", "Season"], dropna=False)
                   .agg(Records=("Farm_Record_ID", "size"), Total_Production_Tons=("Production_Tons", "sum"),
                        Average_Yield_per_Hectare=("Yield_per_Hectare", "mean"),
                        Median_Yield_per_Hectare=("Yield_per_Hectare", "median"))
                   .reset_index().sort_values(["Crop_Type", "Average_Yield_per_Hectare"], ascending=[True, False]))

    yields = df["Yield_per_Hectare"].dropna().to_numpy(dtype=float)
    q1, median_yield, q3 = np.quantile(yields, [0.25, 0.50, 0.75])
    yield_stats = pd.DataFrame([{
        "Records_with_valid_yield": len(yields), "Median": np.median(yields),
        "Variance_population_numpy": np.var(yields), "Q1": q1, "Q2_median": median_yield,
        "Q3": q3, "IQR": q3 - q1,
    }])
    lower_fence, upper_fence = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    outliers = df.loc[df["Yield_per_Hectare"].lt(lower_fence) | df["Yield_per_Hectare"].gt(upper_fence),
                      ["Farm_Record_ID", "Region", "Crop_Type", "Season", "Area_Hectares", "Production_Tons", "Yield_per_Hectare"]].copy()
    outliers["Outlier_Direction"] = np.where(outliers["Yield_per_Hectare"] < lower_fence, "Low", "High")
    outliers["IQR_Lower_Fence"] = lower_fence
    outliers["IQR_Upper_Fence"] = upper_fence
    outliers = outliers.sort_values("Yield_per_Hectare")

    # Split imputed rainfall into three approximately equal-frequency groups.
    df["Rainfall_Category"] = pd.qcut(
        df["Rainfall_mm"].rank(method="first"), q=3, labels=["Low", "Moderate", "High"]
    )
    rainfall = (df.groupby("Rainfall_Category", observed=False)
                .agg(Records=("Farm_Record_ID", "size"), Rainfall_Min_mm=("Rainfall_mm", "min"),
                     Rainfall_Max_mm=("Rainfall_mm", "max"), Average_Yield_per_Hectare=("Yield_per_Hectare", "mean"),
                     Median_Yield_per_Hectare=("Yield_per_Hectare", "median"))
                .reset_index())

    quality = pd.DataFrame([
        {"Check": "Rows", "Result": len(df), "Details": "All source rows retained"},
        {"Check": "Columns", "Result": len(raw.columns), "Details": "Source columns in input CSV"},
        {"Check": "Missing Rainfall_mm", "Result": int(missing_before["Rainfall_mm"]),
         "Details": f"Median imputed: {imputation['Rainfall_mm']['median']:.3f} mm"},
        {"Check": "Missing Soil_pH", "Result": int(missing_before["Soil_pH"]),
         "Details": f"Median imputed: {imputation['Soil_pH']['median']:.3f}"},
        {"Check": "Duplicate Farm_Record_ID rows", "Result": int(duplicate_id_mask.sum()),
         "Details": f"{int(df.loc[duplicate_id_mask, 'Farm_Record_ID'].nunique())} IDs repeat; flagged, not removed"},
        {"Check": "Area_Hectares <= 0 or missing", "Result": int((~valid_area).sum()),
         "Details": "Yield set missing for invalid area; no division by zero"},
    ])

    # Five restrained, association-based recommendations with observed anchors.
    best_crop = crop.iloc[0]
    best_soil = soil.iloc[0]
    best_irrigation = irrigation.iloc[0]
    rain_corr = correlations.loc["Rainfall_mm", "Yield_per_Hectare"]
    fertilizer_corr = correlations.loc["Fertilizer_kg_per_ha", "Yield_per_Hectare"]
    recs = [
        f"{best_crop['Crop_Type']} has the highest sample mean yield ({best_crop['Average_Yield_per_Hectare']:.2f} tons/ha). Treat this as a comparison point, then check crop-specific costs, quality, and local suitability before changing crop plans.",
        f"{best_soil['Soil_Type']} soil has the highest observed mean yield ({best_soil['Average_Yield_per_Hectare']:.2f} tons/ha). Compare within the same crop and region before drawing soil-management conclusions.",
        f"{best_irrigation['Irrigation']} farms have the higher overall average yield ({best_irrigation['Average_Yield_per_Hectare']:.2f} tons/ha). Evaluate irrigation alongside crop mix, rainfall, and farm size; this summary does not establish an irrigation effect.",
        f"Rainfall and yield show a Pearson association of {rain_corr:.2f}; fertilizer and yield show {fertilizer_corr:.2f}. Use these as exploratory signals and collect repeated, locally measured observations before adjusting input rates.",
        "Review IQR-flagged farms against source records, units, area measurement, and crop context before excluding them or using them as targets. Extreme ratios may reflect small areas or data entry issues.",
    ]

    tables = {
        "data_quality.csv": quality,
        "crop_productivity_ranking.csv": crop,
        "region_yield_comparison.csv": region,
        "soil_yield_comparison.csv": soil,
        "irrigation_summary.csv": irrigation,
        "correlation_matrix.csv": correlations.reset_index(names="Variable"),
        "crop_season_comparison.csv": crop_season,
        "yield_statistics.csv": yield_stats,
        "yield_outliers_iqr.csv": outliers,
        "rainfall_category_comparison.csv": rainfall,
        "duplicate_id_rows.csv": duplicate_rows,
    }
    for name, table in tables.items():
        table.to_csv(output_dir / name, index=False)
    df.to_csv(output_dir / "cleaned_crop_yield_with_metrics.csv", index=False)

    report = f"""# Agriculture Crop Yield & Weather Impact Analysis

## Executive summary

- **Records:** {len(df):,} farm records, with {int(duplicate_id_mask.sum())} rows in repeated-ID groups.
- **Total production:** {total_production:,.2f} tons.
- **Average yield:** {average_yield:,.2f} tons per hectare, calculated as the unweighted mean of valid farm-level production/area ratios.
- **Highest average-yield crop:** {best_crop['Crop_Type']} ({best_crop['Average_Yield_per_Hectare']:.2f} tons/ha).
- **IQR outliers:** {len(outliers)} farms ({int((outliers['Outlier_Direction'] == 'Low').sum())} low, {int((outliers['Outlier_Direction'] == 'High').sum())} high).

## Data quality and preparation

The CSV has {len(raw):,} rows and {len(raw.columns)} source columns. Missing rainfall values: {int(missing_before['Rainfall_mm'])}; missing soil pH values: {int(missing_before['Soil_pH'])}. Missing `Rainfall_mm` was filled with its observed median ({imputation['Rainfall_mm']['median']:.2f} mm); missing `Soil_pH` was filled with its observed median ({imputation['Soil_pH']['median']:.2f}). Median imputation preserves rows and limits sensitivity to extreme values. The script adds a `Duplicate_Farm_Record_ID` flag and retains all rows; repeated IDs are listed separately for review. Yield is undefined for missing or nonpositive area; such rows are excluded from yield statistics. Rainfall categories use one-third quantiles (Low, Moderate, High), with ranking to split any tied values into balanced groups.

{markdown_table(quality)}

## Overall and distribution statistics

Production is summed across records; average yield is the mean of per-record yields, not total production divided by total area. NumPy population variance (`ddof=0`) is reported.

{markdown_table(yield_stats)}

## Crop productivity ranking

{markdown_table(crop)}

## Regional comparison

{markdown_table(region)}

## Soil comparison

{markdown_table(soil)}

## Irrigated versus rain-fed summary

{markdown_table(irrigation)}

## Rainfall category comparison

{markdown_table(rainfall)}

## Crop and season productivity

{markdown_table(crop_season)}

## Correlations

Pearson correlations, using median-imputed rainfall, are shown below. These are associations in this dataset, which the assignment identifies as synthetic; they do not establish causal effects.

{markdown_table(correlations.reset_index(names='Variable'))}

## IQR yield outliers

Outlier cutoffs are Q1 − 1.5 × IQR = {lower_fence:.2f} and Q3 + 1.5 × IQR = {upper_fence:.2f} tons/ha. The full record-level list is in `yield_outliers_iqr.csv`.

{markdown_table(outliers)}

## Cautious agronomic observations and recommendations

These points describe patterns in the supplied data. They are not causal conclusions or universal agronomic advice.

1. {recs[0]}
2. {recs[1]}
3. {recs[2]}
4. {recs[3]}
5. {recs[4]}

## Interpretation limits

- The dataset is synthetic and observational; correlations and group averages are descriptive associations only.
- Duplicate IDs are retained to preserve source data. Check `duplicate_id_rows.csv` before treating records as independent farms.
- Rainfall and pH median imputation can soften true variation; compare results with complete-case data in any consequential follow-up.
- Group averages can reflect differences in crop, season, farm size, and location. The comparisons do not control for these factors.
- Yield outliers should be verified in context, not automatically removed.

## Files produced

The Python script also writes cleaned record-level data, all summary tables, the duplicate-ID detail, and the outlier list as CSV files in this results folder.
"""
    (output_dir / "analysis_report.md").write_text(report, encoding="utf-8")
    print(f"Analysis complete. Results: {output_dir}")
    print(f"Rows: {len(df)} | total production: {total_production:.2f} tons | average yield: {average_yield:.2f} tons/ha")
    print(f"Duplicate-ID rows: {int(duplicate_id_mask.sum())} | IQR outliers: {len(outliers)}")


if __name__ == "__main__":
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    destination = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT
    main(source, destination)