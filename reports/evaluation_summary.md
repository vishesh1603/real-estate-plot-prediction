# Model Evaluation Summary

**Best model:** XGBRegressor

## Overall Metrics
- MAE: Rs. 1,414,993
- RMSE: Rs. 3,032,542
- R2 Score: 0.8579
- MAPE: 25.30%

## Model Comparison

| Model             |   MAE (INR) |   RMSE (INR) |   R2 Score |   MAPE (%) |
|:------------------|------------:|-------------:|-----------:|-----------:|
| XGBoost           | 1.41499e+06 |  3.03254e+06 |     0.8579 |      25.3  |
| Random Forest     | 1.37893e+06 |  3.26705e+06 |     0.835  |      23.86 |
| Gradient Boosting | 1.56775e+06 |  3.32304e+06 |     0.8293 |      27.63 |
| Decision Tree     | 1.7092e+06  |  3.98428e+06 |     0.7547 |      29.76 |
| Linear Regression | 3.15046e+06 |  1.48037e+07 |    -2.387  |      50.03 |

## Error by City

| city_decoded   |   abs_pct_error |
|:---------------|----------------:|
| Ghaziabad      |           19.35 |
| Base/Reference |           23.81 |
| Lucknow        |           33.42 |
| Pune           |           34.6  |
