'''from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
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



x1,x2,x3,y=df['Value_LastDay'],df['Value_2DaysBack'],df['Value_3DaysBack'],df['value']
x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1)
final_x=np.concatenate((x1,x2,x3),axis=1)
#print(final_x)

X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]




param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}


rf_model = RandomForestRegressor()

grid_search = GridSearchCV(rf_model, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)


grid_search.fit(X_train, y_train)


best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

y_val_pred = best_model.predict(X_test)

mse = mean_squared_error(y_test, y_val_pred)
print(f'Best Parameters: {best_params}')
print(f'Mean Squared Error on Validation Set: {mse}')'''



from sklearn import decomposition, datasets
from sklearn import linear_model
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler


