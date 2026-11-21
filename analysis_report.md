# Agriculture Crop Yield & Weather Impact Analysis

## Executive summary

- **Records:** 710 farm records, with 20 rows in repeated-ID groups.
- **Total production:** 42,476.86 tons.
- **Average yield:** 14.37 tons per hectare, calculated as the unweighted mean of valid farm-level production/area ratios.
- **Highest average-yield crop:** Cotton (17.58 tons/ha).
- **IQR outliers:** 79 farms (0 low, 79 high).

## Data quality and preparation

The CSV has 710 rows and 11 source columns. Missing rainfall values: 18; missing soil pH values: 17. Missing `Rainfall_mm` was filled with its observed median (1000.65 mm); missing `Soil_pH` was filled with its observed median (6.39). Median imputation preserves rows and limits sensitivity to extreme values. The script adds a `Duplicate_Farm_Record_ID` flag and retains all rows; repeated IDs are listed separately for review. Yield is undefined for missing or nonpositive area; such rows are excluded from yield statistics. Rainfall categories use one-third quantiles (Low, Moderate, High), with ranking to split any tied values into balanced groups.

| Check | Result | Details |
| --- | --- | --- |
| Rows | 710 | All source rows retained |
| Columns | 11 | Source columns in input CSV |
| Missing Rainfall_mm | 18 | Median imputed: 1000.650 mm |
| Missing Soil_pH | 17 | Median imputed: 6.390 |
| Duplicate Farm_Record_ID rows | 20 | 10 IDs repeat; flagged, not removed |
| Area_Hectares <= 0 or missing | 0 | Yield set missing for invalid area; no division by zero |

## Overall and distribution statistics

Production is summed across records; average yield is the mean of per-record yields, not total production divided by total area. NumPy population variance (`ddof=0`) is reported.

| Records_with_valid_yield | Median | Variance_population_numpy | Q1 | Q2_median | Q3 | IQR |
| --- | --- | --- | --- | --- | --- | --- |
| 710 | 7.93 | 456.81 | 4.04 | 7.93 | 14.45 | 10.41 |

## Crop productivity ranking

| Rank | Crop_Type | Records | Total_Production_Tons | Average_Yield_per_Hectare |
| --- | --- | --- | --- | --- |
| 1 | Cotton | 118 | 7,329.61 | 17.58 |
| 2 | Pulses | 100 | 6,445.61 | 15.95 |
| 3 | Maize | 135 | 8,193.06 | 14.79 |
| 4 | Rice | 132 | 7,631.36 | 13.76 |
| 5 | Wheat | 111 | 6,111.99 | 12.58 |
| 6 | Sugarcane | 114 | 6,765.23 | 11.61 |

## Regional comparison

| Region | Records | Average_Yield_per_Hectare | Median_Yield_per_Hectare |
| --- | --- | --- | --- |
| Central | 127 | 16.21 | 8.23 |
| East | 156 | 14.59 | 7.92 |
| South | 143 | 14.33 | 8.19 |
| West | 158 | 14.16 | 8.39 |
| North | 126 | 12.55 | 7.56 |

## Soil comparison

| Soil_Type | Records | Average_Yield_per_Hectare | Median_Yield_per_Hectare |
| --- | --- | --- | --- |
| Clay | 168 | 16.65 | 7.80 |
| Sandy | 167 | 15.78 | 8.38 |
| Loamy | 164 | 12.86 | 8.21 |
| Black | 211 | 12.62 | 7.61 |

## Irrigated versus rain-fed summary

| Irrigation | Records | Average_Yield_per_Hectare | Median_Yield_per_Hectare |
| --- | --- | --- | --- |
| Irrigated | 351 | 14.44 | 7.78 |
| Rain-fed | 359 | 14.30 | 8.18 |

## Rainfall category comparison

| Rainfall_Category | Records | Rainfall_Min_mm | Rainfall_Max_mm | Average_Yield_per_Hectare | Median_Yield_per_Hectare |
| --- | --- | --- | --- | --- | --- |
| Low | 237 | 200.20 | 715.00 | 16.41 | 8.38 |
| Moderate | 236 | 718.90 | 1,280.50 | 13.45 | 8.17 |
| High | 237 | 1,281.30 | 1,798.60 | 13.24 | 7.60 |

## Crop and season productivity

| Crop_Type | Season | Records | Total_Production_Tons | Average_Yield_per_Hectare | Median_Yield_per_Hectare |
| --- | --- | --- | --- | --- | --- |
| Cotton | Zaid | 42 | 2,917.12 | 19.81 | 11.01 |
| Cotton | Rabi | 42 | 2,489.00 | 19.20 | 7.74 |
| Cotton | Kharif | 34 | 1,923.49 | 12.80 | 7.25 |
| Maize | Rabi | 39 | 2,400.64 | 17.74 | 8.38 |
| Maize | Zaid | 47 | 3,011.20 | 16.28 | 9.42 |
| Maize | Kharif | 49 | 2,781.22 | 11.03 | 6.89 |
| Pulses | Rabi | 32 | 2,147.64 | 18.48 | 10.59 |
| Pulses | Kharif | 31 | 1,728.51 | 17.74 | 7.97 |
| Pulses | Zaid | 37 | 2,569.46 | 12.28 | 8.38 |
| Rice | Kharif | 48 | 2,773.48 | 15.37 | 8.67 |
| Rice | Zaid | 52 | 2,970.58 | 14.38 | 7.02 |
| Rice | Rabi | 32 | 1,887.30 | 10.35 | 8.41 |
| Sugarcane | Zaid | 32 | 1,878.11 | 15.99 | 7.89 |
| Sugarcane | Rabi | 37 | 2,364.36 | 10.17 | 9.07 |
| Sugarcane | Kharif | 45 | 2,522.76 | 9.68 | 6.23 |
| Wheat | Kharif | 37 | 2,348.84 | 14.19 | 8.40 |
| Wheat | Rabi | 38 | 1,972.40 | 14.16 | 6.35 |
| Wheat | Zaid | 36 | 1,790.75 | 9.26 | 4.73 |

## Correlations

Pearson correlations, using median-imputed rainfall, are shown below. These are associations in this dataset, which the assignment identifies as synthetic; they do not establish causal effects.

| Variable | Rainfall_mm | Fertilizer_kg_per_ha | Yield_per_Hectare |
| --- | --- | --- | --- |
| Rainfall_mm | 1.00 | 0.02 | -0.05 |
| Fertilizer_kg_per_ha | 0.02 | 1.00 | -0.03 |
| Yield_per_Hectare | -0.05 | -0.03 | 1.00 |

## IQR yield outliers

Outlier cutoffs are Q1 − 1.5 × IQR = -11.58 and Q3 + 1.5 × IQR = 30.07 tons/ha. The full record-level list is in `yield_outliers_iqr.csv`.

| Farm_Record_ID | Region | Crop_Type | Season | Area_Hectares | Production_Tons | Yield_per_Hectare | Outlier_Direction | IQR_Lower_Fence | IQR_Upper_Fence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CR00500 | West | Wheat | Kharif | 3.74 | 113.35 | 30.31 | High | -11.58 | 30.07 |
| CR00500 | West | Wheat | Kharif | 3.74 | 113.35 | 30.31 | High | -11.58 | 30.07 |
| CR00174 | Central | Rice | Rabi | 3.26 | 100.07 | 30.70 | High | -11.58 | 30.07 |
| CR00100 | East | Rice | Zaid | 2.84 | 87.36 | 30.76 | High | -11.58 | 30.07 |
| CR00337 | East | Wheat | Zaid | 3.79 | 117.72 | 31.06 | High | -11.58 | 30.07 |
| CR00436 | Central | Rice | Kharif | 3.27 | 103.01 | 31.50 | High | -11.58 | 30.07 |
| CR00194 | North | Rice | Rabi | 3.19 | 101.86 | 31.93 | High | -11.58 | 30.07 |
| CR00552 | South | Maize | Kharif | 3.47 | 111.74 | 32.20 | High | -11.58 | 30.07 |
| CR00034 | South | Cotton | Zaid | 3.72 | 119.95 | 32.24 | High | -11.58 | 30.07 |
| CR00622 | North | Sugarcane | Kharif | 2.79 | 90.06 | 32.28 | High | -11.58 | 30.07 |
| CR00539 | East | Maize | Rabi | 1.80 | 58.51 | 32.51 | High | -11.58 | 30.07 |
| CR00597 | South | Wheat | Rabi | 3.62 | 118.55 | 32.75 | High | -11.58 | 30.07 |
| CR00426 | South | Wheat | Rabi | 3.04 | 99.83 | 32.84 | High | -11.58 | 30.07 |
| CR00267 | West | Sugarcane | Rabi | 2.08 | 68.45 | 32.91 | High | -11.58 | 30.07 |
| CR00490 | North | Maize | Kharif | 3.43 | 116.77 | 34.04 | High | -11.58 | 30.07 |
| CR00270 | East | Rice | Zaid | 1.03 | 35.31 | 34.28 | High | -11.58 | 30.07 |
| CR00400 | South | Pulses | Kharif | 2.49 | 86.86 | 34.88 | High | -11.58 | 30.07 |
| CR00305 | West | Maize | Zaid | 2.42 | 85.26 | 35.23 | High | -11.58 | 30.07 |
| CR00512 | Central | Sugarcane | Zaid | 2.57 | 91.22 | 35.49 | High | -11.58 | 30.07 |
| CR00233 | West | Sugarcane | Kharif | 2.39 | 85.39 | 35.73 | High | -11.58 | 30.07 |
| CR00150 | West | Sugarcane | Zaid | 1.42 | 51.15 | 36.02 | High | -11.58 | 30.07 |
| CR00365 | East | Cotton | Rabi | 0.84 | 30.86 | 36.74 | High | -11.58 | 30.07 |
| CR00003 | West | Maize | Zaid | 0.70 | 25.86 | 36.94 | High | -11.58 | 30.07 |
| CR00476 | South | Rice | Rabi | 2.23 | 84.99 | 38.11 | High | -11.58 | 30.07 |
| CR00139 | West | Wheat | Kharif | 2.98 | 115.04 | 38.60 | High | -11.58 | 30.07 |
| CR00534 | East | Maize | Zaid | 0.73 | 28.39 | 38.89 | High | -11.58 | 30.07 |
| CR00598 | West | Pulses | Rabi | 2.67 | 107.03 | 40.09 | High | -11.58 | 30.07 |
| CR00695 | North | Cotton | Zaid | 2.65 | 108.89 | 41.09 | High | -11.58 | 30.07 |
| CR00138 | North | Maize | Zaid | 1.50 | 61.80 | 41.20 | High | -11.58 | 30.07 |
| CR00238 | Central | Maize | Zaid | 0.93 | 39.19 | 42.14 | High | -11.58 | 30.07 |
| CR00578 | East | Wheat | Kharif | 2.38 | 100.33 | 42.16 | High | -11.58 | 30.07 |
| CR00000 | West | Rice | Kharif | 1.93 | 82.95 | 42.98 | High | -11.58 | 30.07 |
| CR00374 | South | Sugarcane | Rabi | 2.18 | 95.45 | 43.78 | High | -11.58 | 30.07 |
| CR00211 | South | Wheat | Rabi | 2.59 | 116.15 | 44.85 | High | -11.58 | 30.07 |
| CR00204 | East | Rice | Kharif | 0.96 | 43.11 | 44.91 | High | -11.58 | 30.07 |
| CR00007 | East | Rice | Kharif | 0.53 | 24.35 | 45.94 | High | -11.58 | 30.07 |
| CR00574 | West | Cotton | Kharif | 1.30 | 59.86 | 46.05 | High | -11.58 | 30.07 |
| CR00116 | North | Maize | Kharif | 2.51 | 118.50 | 47.21 | High | -11.58 | 30.07 |
| CR00470 | Central | Maize | Zaid | 1.50 | 71.55 | 47.70 | High | -11.58 | 30.07 |
| CR00196 | South | Pulses | Rabi | 1.38 | 67.49 | 48.91 | High | -11.58 | 30.07 |
| CR00664 | West | Pulses | Kharif | 1.30 | 63.75 | 49.04 | High | -11.58 | 30.07 |
| CR00197 | Central | Rice | Zaid | 1.59 | 78.17 | 49.16 | High | -11.58 | 30.07 |
| CR00290 | East | Maize | Rabi | 1.60 | 79.66 | 49.79 | High | -11.58 | 30.07 |
| CR00087 | South | Pulses | Zaid | 1.00 | 54.81 | 54.81 | High | -11.58 | 30.07 |
| CR00180 | East | Cotton | Kharif | 1.39 | 77.59 | 55.82 | High | -11.58 | 30.07 |
| CR00368 | West | Maize | Zaid | 2.04 | 114.22 | 55.99 | High | -11.58 | 30.07 |
| CR00161 | West | Rice | Kharif | 1.47 | 86.28 | 58.69 | High | -11.58 | 30.07 |
| CR00537 | North | Wheat | Kharif | 1.62 | 96.11 | 59.33 | High | -11.58 | 30.07 |
| CR00231 | South | Cotton | Kharif | 1.66 | 100.48 | 60.53 | High | -11.58 | 30.07 |
| CR00050 | West | Wheat | Zaid | 1.66 | 102.12 | 61.52 | High | -11.58 | 30.07 |
| CR00638 | West | Rice | Zaid | 1.08 | 68.09 | 63.05 | High | -11.58 | 30.07 |
| CR00170 | North | Rice | Zaid | 1.70 | 110.17 | 64.81 | High | -11.58 | 30.07 |
| CR00497 | Central | Cotton | Zaid | 1.53 | 99.33 | 64.92 | High | -11.58 | 30.07 |
| CR00152 | East | Pulses | Kharif | 1.50 | 97.50 | 65.00 | High | -11.58 | 30.07 |
| CR00468 | West | Maize | Kharif | 1.40 | 92.59 | 66.14 | High | -11.58 | 30.07 |
| CR00626 | East | Pulses | Zaid | 1.45 | 97.94 | 67.54 | High | -11.58 | 30.07 |
| CR00479 | Central | Cotton | Zaid | 1.55 | 105.75 | 68.23 | High | -11.58 | 30.07 |
| CR00585 | North | Sugarcane | Zaid | 1.39 | 99.65 | 71.69 | High | -11.58 | 30.07 |
| CR00607 | North | Rice | Kharif | 1.47 | 105.66 | 71.88 | High | -11.58 | 30.07 |
| CR00283 | Central | Rice | Kharif | 0.90 | 65.10 | 72.33 | High | -11.58 | 30.07 |
| CR00224 | South | Maize | Zaid | 0.84 | 62.61 | 74.54 | High | -11.58 | 30.07 |
| CR00641 | Central | Rice | Zaid | 0.57 | 42.66 | 74.84 | High | -11.58 | 30.07 |
| CR00371 | South | Maize | Zaid | 0.87 | 66.46 | 76.39 | High | -11.58 | 30.07 |
| CR00216 | East | Pulses | Kharif | 0.52 | 46.55 | 89.52 | High | -11.58 | 30.07 |
| CR00252 | West | Wheat | Kharif | 1.18 | 106.39 | 90.16 | High | -11.58 | 30.07 |
| CR00459 | South | Cotton | Zaid | 0.95 | 86.44 | 90.99 | High | -11.58 | 30.07 |
| CR00246 | North | Sugarcane | Kharif | 1.15 | 110.72 | 96.28 | High | -11.58 | 30.07 |
| CR00256 | Central | Rice | Zaid | 1.14 | 112.09 | 98.32 | High | -11.58 | 30.07 |
| CR00198 | North | Cotton | Rabi | 0.66 | 65.25 | 98.86 | High | -11.58 | 30.07 |
| CR00621 | South | Cotton | Rabi | 0.63 | 66.98 | 106.32 | High | -11.58 | 30.07 |
| CR00491 | Central | Sugarcane | Zaid | 0.59 | 63.95 | 108.39 | High | -11.58 | 30.07 |
| CR00063 | Central | Cotton | Rabi | 0.98 | 110.93 | 113.19 | High | -11.58 | 30.07 |
| CR00373 | East | Pulses | Kharif | 1.00 | 119.29 | 119.29 | High | -11.58 | 30.07 |
| CR00653 | Central | Cotton | Zaid | 0.86 | 118.60 | 137.91 | High | -11.58 | 30.07 |
| CR00066 | Central | Maize | Rabi | 0.82 | 117.29 | 143.04 | High | -11.58 | 30.07 |
| CR00235 | West | Cotton | Rabi | 0.70 | 106.43 | 152.04 | High | -11.58 | 30.07 |
| CR00073 | East | Wheat | Rabi | 0.62 | 95.95 | 154.76 | High | -11.58 | 30.07 |
| CR00262 | South | Maize | Rabi | 0.52 | 88.62 | 170.42 | High | -11.58 | 30.07 |
| CR00277 | East | Pulses | Rabi | 0.67 | 117.54 | 175.43 | High | -11.58 | 30.07 |

## Cautious agronomic observations and recommendations

These points describe patterns in the supplied data. They are not causal conclusions or universal agronomic advice.

1. Cotton has the highest sample mean yield (17.58 tons/ha). Treat this as a comparison point, then check crop-specific costs, quality, and local suitability before changing crop plans.
2. Clay soil has the highest observed mean yield (16.65 tons/ha). Compare within the same crop and region before drawing soil-management conclusions.
3. Irrigated farms have the higher overall average yield (14.44 tons/ha). Evaluate irrigation alongside crop mix, rainfall, and farm size; this summary does not establish an irrigation effect.
4. Rainfall and yield show a Pearson association of -0.05; fertilizer and yield show -0.03. Use these as exploratory signals and collect repeated, locally measured observations before adjusting input rates.
5. Review IQR-flagged farms against source records, units, area measurement, and crop context before excluding them or using them as targets. Extreme ratios may reflect small areas or data entry issues.

## Interpretation limits

- The dataset is synthetic and observational; correlations and group averages are descriptive associations only.
- Duplicate IDs are retained to preserve source data. Check `duplicate_id_rows.csv` before treating records as independent farms.
- Rainfall and pH median imputation can soften true variation; compare results with complete-case data in any consequential follow-up.
- Group averages can reflect differences in crop, season, farm size, and location. The comparisons do not control for these factors.
- Yield outliers should be verified in context, not automatically removed.

## Files produced

The Python script also writes cleaned record-level data, all summary tables, the duplicate-ID detail, and the outlier list as CSV files in this results folder.
