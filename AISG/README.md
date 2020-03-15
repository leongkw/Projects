# Introduction

This is a ML pipeline created for purposes of AISG technical assessment.

The flow of the pipeline is as follows:
1. Execute run.sh to install required libraries/modules and to run ml_script
2. ml_script loads configuration data from config yaml file
3. ml_script loads data from specified source from config yaml - Source can be configured or changed.
4. ml_script processes data by performing the following actions: 
- Combine date and hr column into a single column, converting it into date-time format
- Set combined date-time column as index
- Clean up weather column by standardizing the weather labels
- Create hour, day, day_week, day_month columns from combined date-time column as new features
5. ml_script drops the unnceccesary columns - Can be configured or changed.
6. ml_script creates binary dummies for categorical features
7. ml_script performs train-test-split - test_size can be configured.
8. ml_script trains the models (LightGMB Regressor & Random Forest Regressor) - Can be switched on and off.
9. ml_script prints out the metrics used to evaluate models (R2, CV, RSME, MAE) - Can be switched on and off.


# Requirements

1. pandas==0.25.2
2. numpy==1.18.1
3. sklearn==0.0
4. lightgbm==2.3.1
5. PyYAML==5.1.2


# Model Choice
We'll try to model the data using two methods:

1. LightGBM Regressor
2. Random Forest Regressor

Since total users is a continuous variable, a regression based approach might be suitable.

I am not considering deep-learning models because the amount of data available (~18k rows) might not be sufficient. In such cases, it is likely that non deep-learning models will outperform deep-learning models.

Also, I have some doubts as to whether a time-series model will be effective, given that there is only data for 2 years.


# Configuration
### source
Origin of dataset. Can be changed to load from a url or from local storage.

### to_drop
True/False. Used to control whether ml_script will drop specified columns or not.

### drop_list
List of column names that will be dropped by ml_scipt. Can be changed depending on needs.

### eval_metric
- show_mae: True/False. If True, MAE will be shown.
- show_rsme: True/False. If True, RSME will be shown.
- show_r2: True/False. If True, R2 will be shown.
- show_cv: True/False. If True, CV will be shown.
- cv_folds: Takes in an integer. Used to specify how many folds of cross-validation.
- cv_scoring: Takes in a string. Used to specify which metric to use for cross-validation.

### train_test_split:
- test_size: Takes in a float. Used to specify testing set size
- random_state: Takes in an integer. Used to set random state to ensure reproducibility of results.

### models:
- RandomForestRegressor: True/False. If True, ml_script will generate and fit a Random Forest Regressor model.
- LGBMRegressor: True/False. If True, ml_script will generate and fit a LightGBM Regressor model.

### RandomForest:
This portion contains all the configurable parameters for the Random Forest Regressor model.

### LightGBM
This portion contains all the configurable parameters for the LightGBM Regressor model.