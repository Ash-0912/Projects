import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


df=pd.read_csv('C:/Users/SESA750454/Documents/Docs/UniData2.csv')

#Preprocessing the Data
df['date']=pd.to_datetime(df['date'],format='%Y%m%d')
df=df.dropna(axis='columns')
df['Month']=df['date'].dt.strftime('%B')
df['Year']=df['date'].dt.year
df=df[df['Year']!=2022]
df.to_csv('DATA.csv',index=False)
#print(df.head())
df=df.drop(columns=['Year','Month'])
#print(df.head())
df=df.set_index('date')
#print(df.head())



'''train, test=train_test_split(df,test_size=0.2, shuffle=False)
print(train)
print(test)'''


#Testing and Training Data
#plt.plot(train.date, train['value'],label='Training Data')
#plt.plot(test.date, test['value'],label='Testing Data')
#plt.legend()
#plt.show()

model=ExponentialSmoothing(np.asarray(df['value']),trend='add',seasonal='add',seasonal_periods=10)
model_fit=model.fit()
pred=model_fit.forecast(92)



'''future_period=len(df)
future_index=pd.date_range(start=df['date'].iloc[-1]+pd.Timedelta(days=1),periods=future_period,freq='D')'''

'''pred=model_fit.predict(start=future_index[0],end=future_index[-1])
print(pred)'''


date_str='2023-12-01'
date_end='2024-03-01'

dd=pd.date_range('2023-12-01','2024-03-01',freq='D')
dailydf = dd.to_frame(index=False,name='date')
dailydf['date']=pd.to_datetime(dailydf["date"]).dt.date
dailydf=dailydf.set_index('date')
dailydf['Forcasted values']=pred
dailydf.to_csv('C:/logs/output.csv')
print(dailydf)
#print(df)'''


'''model_fit.predict()
pred=model_fit.predict(start=dailydf.index[0], end=dailydf.index[-1])
print(pred)'''



