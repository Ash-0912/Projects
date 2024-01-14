import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df=pd.read_csv('C:/Users/SESA750454/Documents/Docs/Dateta.csv')
df=df.dropna(axis='columns')
df['date']=pd.to_datetime(df['date'],format='%Y%m%d')
print(df.tail())
df=df.set_index(['date'])
#df.plot(figsize=(12,8))
#plt.show()

df['Value_LastDay']=df['value'].shift(+1)
df['Value_2DaysBack']=df['value'].shift(+2)
df['Value_3DaysBack']=df['value'].shift(+3)
df=df.dropna()
print(df)

from sklearn.linear_model import LinearRegression
lin_model=LinearRegression()

from sklearn.ensemble import RandomForestRegressor
model=RandomForestRegressor(n_estimators=200,max_features=3,random_state=1,min_samples_split=2)

x1,x2,x3,y=df['Value_LastDay'],df['Value_2DaysBack'],df['Value_3DaysBack'],df['value']
x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1)
final_x=np.concatenate((x1,x2,x3),axis=1)
#print(final_x)

X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]

model.fit(X_train,y_train)
lin_model.fit(X_train,y_train)


model_pred=model.predict(X_test)
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"]=(12,8)
plt.plot(model_pred,label='Random_Forest_Prediction')
plt.plot(y_test,label='Actual Values')
plt.legend(loc="upper left")
plt.show()
print(model_pred)



'''lin_pred=lin_model.predict(X_test)
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"]=(12,8)
plt.plot(lin_pred,label='Linear_regression_Prediction')
plt.plot(y_test,label='Actual Values')
plt.legend(loc="upper left")
plt.show()
print(lin_pred)'''


'''future_dates=pd.date_range(df.index[-1],periods=30,freq='D')[1:]
future_x1=df['value'].iloc[-1]
future_x2=df['value'].iloc[-2]
future_x3=df['value'].iloc[-3]'''

'''future_x1,future_x2,future_x3=np.array(future_x1),np.array(future_x2),np.array(future_x3)
future_x1,future_x2,future_x3=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1)
future_x=np.concatenate((future_x1,future_x2,future_x3),axis=1)'''


#future_x=np.array([future_x1,future_x2,future_x3]).reshape(1,-1)
#print(future_x)

future_dates = pd.date_range(df.index[-1], periods=30, freq='D')[1:]  

future_features = np.array([[df['value'].iloc[-1], df['value'].iloc[-2], df['value'].iloc[-3]]])
future_features_l = np.array([[df['value'].iloc[-1], df['value'].iloc[-2], df['value'].iloc[-3]]])

# Predict with the models for each future date
future_model_pred = []
future_lin_pred = []

for date in future_dates:
    # Create features for the current future date
    current_features = np.array([[future_features[-1][0],future_features[-1][1],future_features[-1][2]]])
    #current_features_linear=np.array([[future_features_l[-1][0],future_features_l[-1][1],future_features_l[-1][2]]])
    #print(current_features)

    # Predict with the models for the current future date
    future_model_pred.append(model.predict(current_features)[0])
    #future_lin_pred.append(lin_model.predict(current_features_linear).ravel()[0])

    future_features=np.append(future_features,[[future_model_pred[-1],future_features[-1][0],future_features[-1][1]]],axis=0)
    #future_features_l=np.append(future_features_l,[[future_lin_pred[-1],future_features_l[-1][0],future_features_l[-1][1]]],axis=0)


print(future_model_pred)
#print(future_lin_pred)
#Visualize the results
'''plt.plot(df.index, y, label='Historical Values')
plt.plot(future_dates, future_model_pred, label='Random Forest Forecast', linestyle='--', color='red')
plt.plot(future_dates, future_lin_pred, label='Linear Regression Forecast', linestyle='--', color='blue')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.show()'''


#future_model_pred=[model.predict(future_x)[0] for _ in range(len(future_dates))]
#future_lin_pred=lin_model.predict(future_x)
#print('Forest Regression: ')
#print(future_model_pred)
#print('Linear Regression:')
#print(future_lin_pred)

