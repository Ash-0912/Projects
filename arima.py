import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import boxcox
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

df=pd.read_csv('C:/Users/SESA750454/Documents/Docs/Dateta.csv')
df['date']=pd.to_datetime(df['date'],format='%Y%m%d')
df=df.dropna(axis='columns')
df=df.set_index(['date'])
#df['value'].plot(figsize=(12,6))
#plt.show()

'''df['date']=df['date'].dt.to_period('M')
Monthly_value=df.groupby('date').sum().reset_index()
Monthly_value['date']=Monthly_value['date'].dt.to_timestamp()
print(Monthly_value.head)'''

'''train,test=train_test_split(df,test_size=0.1,shuffle=False)

scaler = MinMaxScaler()
train['value'] = scaler.fit_transform(train)
test['value'] = scaler.transform(test)'''



#y=Monthly_value['value']

#tranformed_data,lambda_value=boxcox(y)

#plt.figure(figsize=(12,6))

'''plt.subplot(1,2,1)
plt.plot(y)
plt.title('Original data')

plt.subplot(1,2,2)
plt.plot(tranformed_data)
plt.title('transformed values')
#plt.show()'''

#Monthly_value['trans']=tranformed_data
#print(Monthly_value)

differenced_data=df['value'].diff().dropna()
differenced_data.plot(figsize=(15,5))
#plt.show()


from statsmodels.tsa.stattools import adfuller

def ad_test(dataset):
    dftest=adfuller(dataset,autolag='AIC')
    print("1. ADF:",dftest[0])
    print("2. P-Value:",dftest[1])
    print("3. No. of lags:",dftest[2])
    print("4. No. of observations used for adf aregression and critical values calculation:",dftest[3])
    print("S. Critical Values:")
    for key,val in dftest[4].items():
        print("\t",key,":",val)


ad_test(df)

#figuring out order
from pmdarima import auto_arima

import warnings
warnings.filterwarnings("ignore")

#stepwise_fit=auto_arima(differenced_data, trace=True,suppress_warnings=True,seasonal=True,seasonal_test='ocsb')

#stepwise_fit.summary()

#supervised_data=Monthly_value.drop(['value'],axis=1)
#Monthly_value=Monthly_value.set_index(['date'])
#print(Monthly_value)

import statsmodels.api as sm
#from sklearn.model_selection import train_test_split

#train=df.iloc[:-30]
#test=df.iloc[-30:]
#test,train=train_test_split(differenced_data,train_size=0.2,shuffle=False)
#rint(train.shape,test.shape)

model=sm.tsa.arima.ARIMA(differenced_data,order=(1,0,1))
model=model.fit()
pred=model.predict()
print(pred)
pred_forecast=df['value'].iloc[-1]+np.cumsum(pred)
print(pred_forecast)



'''start=len(train) 
end=len(train)+len(test)-1
pred=model.predict(start=start,end=end,type='levels')
pred.index=Monthly_value.index[start:end+1]
print(pred)

plt.rcParams["figure.figsize"]=(12,8)
plt.plot(pred,label='Linear_regression_Prediction')
plt.plot(test,label='Actual Values')
plt.legend(loc="upper left")
plt.show()

print(test['value'].mean())

from sklearn.metrics import mean_squared_error
from math import sqrt
rmse=sqrt(mean_squared_error(pred,test['value']))
print(rmse)


fore=model.forecast()
print(fore)
#index_future_dates=pd.date_range(start='2023-11-30',end='2023-12-30')
#pred=model.predict('2024-01-01').rename('ARIMA Predictions')
#print(pred)'''

future_periods=30
forecast=model.forecast(steps=future_periods)
print(forecast)

final_forecast=df['value'].iloc[-1]+np.cumsum(forecast)
print(final_forecast)
