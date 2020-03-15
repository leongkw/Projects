### IMPORTING CONFIGURATION FILE ###
import yaml
with open(r'mlp/config.yml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
print("Configuration file loaded.")

import warnings
warnings.filterwarnings('ignore')

### IMPORTING MODULES ###
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score,train_test_split
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
if config['models']['RandomForestRegressor']:
    from sklearn.ensemble import RandomForestRegressor
if config['models']['LGBMRegressor']:
    from lightgbm import LGBMRegressor


### FUNCTIONS LIBRARY ###
def generate_eval_metrics(model,y_test,x_test, y_train, x_train):
    if config['eval_metric']['show_mae']:
        print('MAE:',mean_absolute_error(y_test,model.predict(x_test)))
    if config['eval_metric']['show_rmse']:
        print('RMSE:', np.sqrt(mean_squared_error(y_test,model.predict(x_test))))    
    if config['eval_metric']['show_r2']:
        print('R2:',r2_score(y_test,model.predict(x_test)))
    if config['eval_metric']['show_cv']:
        print(config['eval_metric']['cv_scoring'],'CV:',np.average(cross_val_score(model,x_train,y_train,cv=config['eval_metric']['cv_folds'])))


### LOADING DATASET ###
try:
	df = pd.read_csv(config['source'])
	print('Dataset successfully loaded')
	print('Data Columns:', list(df.columns))

except:
	print('Dataset failed to load')



### DATA PROCESSING ###
df['hr'] = df['hr'].apply(lambda x : str(x) + ':00:00')
df['date-time'] = df['date'] + ' ' + df['hr']
print('Merged date columns and hour columns together')
df['date-time'] = pd.to_datetime(df['date-time'])
print("Converted merged date-time column into date-time format")
df.index = df['date-time']
df = df.drop(['date', 'hr', 'date-time'], axis=1)
print("Set date-time column as index and dropped old date and hour columns")


temp_list = []
for weather in df['weather']:
    if weather == 'clear' or weather == 'lear' or weather == 'CLEAR':
        temp_list.append('clear')
    
    elif weather == 'cloudy' or weather == 'loudy' or weather == 'CLOUDY':
        temp_list.append('cloudy')
    
    elif weather == 'light snow/rain' or weather == 'LIGHT SNOW/RAIN':
        temp_list.append('light snow/rain')
    
    else:
        temp_list.append('heavy snow/rain')

df['weather'] = temp_list
print('Clean-up of weather column complete.')

df['total_users'] = df['registered-users'] + df['guest-users']
df = df.drop(['registered-users', 'guest-users'], axis=1)
print('Combined guest users and registered users columns into total users')


df['hour'] = [x.hour for x in df.index]
df['month'] = [x.month for x in df.index]
df['day_week'] = [x.weekday() for x in df.index]
df['day_week'] = df['day_week'].map({0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun',})
df['day_month'] = [x.day for x in df.index]
print("Created new features: hour, month, day_week, day_month.")


### DROPPING COLUMNS FROM DROP LIST ###
if config['to_drop']:
    df.drop(config['drop_list'],axis=1,inplace=True)
print("Columns dropped:",config['drop_list'])
print('Columns remaining:',list(df.columns))


### CREATING BINARY DUMMY COLUMNS FOR NEW FEATURES
for column in df.columns:
    if df[column].dtypes=='O':
        df = pd.concat([df,pd.get_dummies(df[column],drop_first=False)],axis=1)
        df.drop(column,axis=1,inplace=True)
print('Created binary dummy columns for all categorical features.')


### TRAIN-TEST-SPLIT ###
features = [x for x in df.columns if x != 'total_users']
target = ['total_users']
x = df[features]
y = df[target]
del df

if type(config['train_test_split']['test_size']) != float:
    raise ValueError('Your test_size parameter needs to be a float.')
else:
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=config['train_test_split']['test_size'], random_state=config['train_test_split']['random_state'])
    print("Train-test split complete.")
    print("Test size:",config['train_test_split']['test_size'])

### MODELLING ###
if config['models']['RandomForestRegressor']:
    print("---Random Forest---")
    model = RandomForestRegressor()
    model.set_params(**config['RandomForest'])
    model.fit(x_train,y_train)
    generate_eval_metrics(model, y_test, x_test, y_train, x_train)

if config['models']['LGBMRegressor']:
    print("---LightGBM---")
    model = LGBMRegressor()
    model.set_params(**config['LightGBM'])
    model.fit(x_train,y_train)
    generate_eval_metrics(model, y_test, x_test, y_train, x_train)