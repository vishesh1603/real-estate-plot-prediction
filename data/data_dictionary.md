# Data Dictionary

## Source
- User-provided archive (`archive_2_.zip`) containing 12 CSV files: real-estate listing exports
  for 4 cities (Chandigarh, Ghaziabad, Lucknow, Pune) × 3 property types (Plot, Villa, Builder Floor).
- Date merged/received: as provided in this project session.
- Files were merged into a single master file: `data/raw/real_estate_master.csv`, with `city` and
  `property_type` columns added during the merge to preserve source origin.

## Row Counts
- **Raw merged rows:** 13,828
- **After cleaning (notebook 01):** see `data/processed/cleaned_listings.csv` shape printed at the
  end of `01_data_cleaning.ipynb` (duplicates, invalid price/area, and extreme per-type outliers removed).
- **Breakdown by city × property_type** (raw, post-merge):

| City | Builder Floor | Plot | Villa |
|---|---|---|---|
| Chandigarh | 1,056 | 779 | 175 |
| Ghaziabad | 5,533 | 723 | 278 |
| Lucknow | 74 | 2,060 | 180 |
| Pune | 123 | 1,870 | 977 |

## Columns (Raw Dataset — 41 total)

| Column | Type | Description |
|---|---|---|
| `location` | text | Locality/neighbourhood name within the city |
| `area` | numeric (sqft) | Plot/property area |
| `price` | numeric (INR) | Listed price |
| `price_currency` | text | Currency label (raw data, mostly INR) |
| `status` | numeric/text | Construction status flag (sparsely populated, e.g. Ready/Under construction) |
| `new/resale` | binary (0/1) | Whether listing is new or resale |
| `price_negotiable` | binary (0/1) | Whether price is marked negotiable |
| `description` | text | Free-text listing description (not used as a model feature) |
| `security_deposit` | numeric (INR) | Security deposit amount, where applicable |
| `facing` | text | Plot/property facing direction (North, East, etc.) |
| `furnished` | binary (0/1) | Furnished status |
| `age of property` | numeric (years) | Age of the property |
| `Lift(s)` … `Landscaped Gardens` | binary (0/1) | Amenity flags (10 core amenities, low missingness, used in modeling) |
| `locality_score` | numeric | Locality quality score (moderately sparse — imputed with median) |
| `project_score`, `builder_experience`, `Golf Course`, `Cafeteria`, and 10 other amenity/score columns | numeric | **Dropped in cleaning** — 80–96% missing, insufficient signal |
| `Car Parking` | binary (0/1) | Parking availability (moderately sparse — imputed with 0) |
| `city` | text | Added during merge: Chandigarh / Ghaziabad / Lucknow / Pune |
| `property_type` | text | Added during merge: Plot / Villa / Builderfloor |

## Derived Columns (added in `01_data_cleaning.ipynb`)
- `price_per_sqft` = `price` / `area`
- `amenity_count` = sum of the 10 core amenity flags present for that listing

## Columns Dropped During Cleaning (>75% missing)
`project_score`, `builder_experience`, `Golf Course`, `Cafeteria`, `Multipurpose Room`,
`Indoor Games`, `Staff Quarter`, `Maintenance Staff`, `Rain Water Harvesting`, `Shopping Mall`,
`ATM`, `Hospital`, `Vaastu Compliant`, `School`, `Intercom`
*(exact list is regenerated and printed at runtime in `01_data_cleaning.ipynb`, Section 2)*

## Notes for Reproducibility
- This dataset is real listing data (not synthetic) — no synthetic-data disclosure is required.
- If any personally identifying information were present in `description` or `location` it should
  be reviewed before public submission; none was identified in this pass, but this should be
  manually re-verified before the dataset is shared outside the group.
