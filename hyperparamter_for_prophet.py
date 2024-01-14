from sklearn.model_selection import ParameterGrid
import itertools
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from prophet import Prophet
import pandas as pd
from pandas import concat
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import train_test_split
import random

df=pd.read_csv('C:/Users/SESA750454/Documents/Docs/UniData.csv')
df['date']=pd.to_datetime(df['date'],format='%Y%m%d')

train, test=train_test_split(df,test_size=0.1, shuffle=False)

df=df.reset_index()\
.rename(columns={'date':'ds','value':'y'})

train_prohet=train.reset_index()\
.rename(columns={'date':'ds','value':'y'})

holiday=pd.read_csv('C:/Users/SESA750454/Documents/Docs/holiday.csv')


holiday=holiday.dropna(axis='columns')
holiday=holiday.reset_index()\
.rename(columns={'Date':'ds','Name':'holiday'})

model=Prophet(holidays=holiday)
model.add_country_holidays(country_name='GB')
model.fit(train_prohet)



params_grid = {'changepoint_prior_scale':[0.001,0.05,0.08,0.5],
              'seasonality_prior_scale':[0.01,1,5,10,12,25],}

'''all_params = [dict(zip(params_grid.keys(), v)) for v in itertools.product(*params_grid.values())]
rmses = []

for params in all_params:
    m = Prophet(**params).fit(train_prohet)  
    initial_tp=int(len(df)*0.8)
    initial_tp_str=f'{initial_tp}days'
    df_cv = cross_validation(m, initial=initial_tp_str, period='30 days', horizon = '30 days')
    df_p = performance_metrics(df_cv, rolling_window=1)
    rmses.append(df_p['rmse'].values[0])


tuning=pd.DataFrame(all_params)
tuning['rmse'] = rmses
print(tuning)

print(dict(tuning.sort_values('rmse').reset_index(drop=True).iloc[0]))


params_dictionary = dict(tuning.sort_values('rmse').reset_index(drop=True).drop('rmse',axis='columns').iloc[0])

m = Prophet(changepoint_prior_scale = params_dictionary['changepoint_prior_scale'], 
            seasonality_prior_scale = params_dictionary['seasonality_prior_scale'])
m.fit(train_prohet)

future = m.make_future_dataframe(periods=120)
fcst_prophet_train = m.predict(future)
print(fcst_prophet_train)

strt='2023-11-30'
end='2023-11-01'
filter = fcst_prophet_train['ds']>=strt
predicted_df = fcst_prophet_train[['ds','yhat']]'''



#mean_absolute_percentage_error(predicted_df['ytrue'], predicted_df['yhat'])









grid = ParameterGrid(params_grid)
cnt = 0
for p in grid:
    cnt = cnt+1

print('Total Possible Models',cnt)

holiday=holiday.dropna(axis='columns')
holiday=holiday.reset_index()\
.rename(columns={'Date':'ds','Name':'holiday'})

strt='2023-10-02'
end='2023-12-01'

model_parameters = pd.DataFrame(columns = ['MAPE','Parameters'])
for p in grid:
    test = pd.DataFrame()
    print(p)
    random.seed(0)
    train_model =Prophet(changepoint_prior_scale = p['changepoint_prior_scale'],
                         seasonality_prior_scale=p['seasonality_prior_scale'],
                         daily_seasonality=True,
                         yearly_seasonality=True,
                         weekly_seasonality=True,
                         holidays=holiday, 
                         interval_width=0.95,growth='logistic')
    train_model.add_country_holidays(country_name='GB')
    train_prohet['cap']=180
    train_model.fit(train_prohet)
    train_forecast = train_model.make_future_dataframe(periods=60, freq='D',include_history = False)
    train_forecast['cap']=180
    train_forecast = train_model.predict(train_forecast)

    test=train_forecast[['ds','yhat']]
    Actual = df[(df['ds']>strt) & (df['ds']<=end)]
    MAPE = [mean_absolute_percentage_error(Actual['y'],abs(test['yhat']))]
    print('Mean Absolute Percentage Error(MAPE)------------------------------------',MAPE)
    
    
'''p=pd.DataFrame(p,index=[1])
    MAPE=pd.DataFrame(MAPE)
    model_parameters = pd.concat({'MAPE':MAPE,'Parameters':p},ignore_index=True)
    print(model_parameters)'''