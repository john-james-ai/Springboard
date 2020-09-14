Write a summary of the work in this notebook. Capture the fact that you gained a baseline idea of performance by simply taking the average price and how well that did. Then highlight that you built a linear model and the features that found. Comment on the estimate of its performance from cross-validation and whether its performance on the test split was consistent with this estimate. Also highlight that a random forest regressor was tried, what preprocessing steps were found to be best, and again what its estimated performance via cross-validation was and whether its performance on the test set was consistent with that. State which model you have decided to use going forwards and why. This summary should provide a quick overview for someone wanting to know quickly why the given model was chosen for the next part of the business problem to help guide important business decisions.

# Summary

## Baseline

Before training models, a baseline model was created based upon the mean of the target values in the training set. This baseline model achieved a coefficient of determination of $R^2=0$ on the training set and slightly worse on the test set. To  obtain a more robust view of performance, the baseline was evaluated using several metrics including mean absolute error (MAE), mean squared error (MSE).

| Metric                            | Training Set | Test Set |
| --------------------------------- | ------------ | -------- |
| Coefficient of Determination (R2) | 0            | -0.00312 |
| Mean Absolute Error (MAE)         | 17.92346     | 19.13614 |
| Mean Squared Error (MSE)          | 614.1334     | 581.4365 |

## Models

Having established a baseline, the data was preprocessed and two models were developed: Linear Regression and Random Forests Regression.

### Preprocessing

Prior to modeling, the missing values were imputed with the median values for the variable. Next, the features were scaled to have zero mean and unit variance.  

### Linear Regression

A grid search cross-validation was performed with linear regression to identify the best k features and to estimate the associated model performance. The following eight features produced the best $R^2\approx0.73$ via cross-validation:

- Vertical Drop
- Snow Making
- Total Chairs
- Fast Quads
- Runs
- Longest Run
- Trams
- Skiable Terrain.

### Random Forests

A random forests model was fit achieving a cross-validation $R^2=0.708$. The feature importances were extracted from the random forests regressor object yielding the following top four features:

- fastQuads
- Runs
- Snow Making
- Vertical Drop

This agreed with our features used in linear regression. The following summarizes the performance of the two models.

| Model                     | Mean R2  | STD R2   |
| ------------------------- | -------- | -------- |
| Linear Regression         | 0.632887 | 0.027982 |
| Random Forests Regression | 0.708161 | 0.065647 |