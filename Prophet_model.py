from sklearn.model_selection import ParameterGrid
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error,mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
import random
from prophet.plot import plot_components_plotly,plot_plotly
from TSUtilities.functions import dampen_prophet



df=pd.read_csv('C:/Users/SESA750454/Documents/Docs/UniData2.csv')

#Preprocessing the Data
df['date']=pd.to_datetime(df['date'],format='%Y%m%d')
df=df.dropna(axis='columns')
df['Month']=df['date'].dt.strftime('%B')
df['Year']=df['date'].dt.year
df=df[df['Year']!=2022]
df.to_csv('UniData.csv',index=False)
#print(df.head())


'''ax = df.plot(x='date', y='value', figsize=(12,6))
xcoords = ['2023-01-01', '2023-02-01','2023-03-01', '2023-04-01', '2023-05-01', '2023-06-01',
          '2023-07-01','2023-08-01','2023-09-01','2023-10-01','2023-11-01']
for xc in xcoords:
    plt.axvline(x=xc, color='black', linestyle='--')'''
train, test=train_test_split(df,test_size=0.1, shuffle=False)

#Testing and Training Data
#plt.plot(train.date, train['value'],label='Training Data')
#plt.plot(test.date, test['value'],label='Testing Data')
#plt.legend()
#plt.show()

df=df.reset_index()\
.rename(columns={'date':'ds','value':'y'})

train_prohet=df.reset_index()\
.rename(columns={'date':'ds','value':'y'})

holiday=pd.read_csv('C:/Users/SESA750454/Documents/Docs/holiday.csv')


holiday=holiday.dropna(axis='columns')
holiday=holiday.reset_index()\
.rename(columns={'Date':'ds','Name':'holiday'})
df['cap']=180
model=Prophet(holidays=holiday,changepoint_prior_scale=0.5,seasonality_prior_scale=12,growth='logistic').add_seasonality(name='monthly',period=30.5,fourier_order=5)
model.add_country_holidays(country_name='GB')
model.fit(df)


test_prohet=test.reset_index()\
.rename(columns={'date':'ds','value':'y'})

test_prohet['cap']=180
pred=model.predict(test_prohet)
print(pred.head())                       



strt='2023-08-01'

future=model.make_future_dataframe(periods=150)
future['cap']=180
forecast=model.predict(future)
print(forecast)
filter = forecast['ds']>=strt
forecast_data = forecast[filter][['ds','yhat']]
forecast_data.to_csv('ForecastData.csv',index=False)




print(forecast)
model.plot_components(forecast)
plt.show()
fig1=model.plot(forecast)
fig1.show()




from prophet.diagnostics import cross_validation
initial_tp=int(len(df)*0.8)
print(initial_tp)
initial_tp_str=f'{initial_tp}days'
cv=cross_validation(model,initial=initial_tp_str ,horizon ='30 days',period='180 days')
print(cv.tail())

from prophet.diagnostics import performance_metrics
df_p = performance_metrics(cv)
print(df_p.tail())

from prophet.plot import plot_cross_validation_metric
fig = plot_cross_validation_metric(cv, metric='mape')
plt.show()




