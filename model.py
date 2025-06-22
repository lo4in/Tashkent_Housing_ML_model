import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from preprocessing import load_and_preprocess

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

def Model():
    data = load_and_preprocess()

    data['price_log'] = np.log1p(data['price'])

    X = data.drop(columns=['price', 'price_log'])
    Y_log = data['price_log'].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, Y_train_log, Y_test_log = train_test_split(X_scaled, Y_log, test_size=0.3, random_state=69)

    model = LinearRegression()
    model.fit(X_train, Y_train_log)

    y_train_pred_log = model.predict(X_train)
    y_test_pred_log = model.predict(X_test)

    Y_train = np.expm1(Y_train_log)
    Y_test = np.expm1(Y_test_log)
    y_train_pred = np.expm1(y_train_pred_log)
    y_test_pred = np.expm1(y_test_pred_log)


    print("Train R²:", model.score(X_train, Y_train_log))
    print("Test R²:", model.score(X_test, Y_test_log))

    from sklearn.metrics import root_mean_squared_error

    print("Train RMSE:", root_mean_squared_error(Y_train, y_train_pred ))
    print("Test RMSE:", root_mean_squared_error(Y_test, y_test_pred))

    return model, scaler, X.columns

def Plot_model():
    plt.figure(figsize=(8,5))
    plt.scatter(Y_test, y_test_pred, alpha=0.4)
    plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'r--')
    plt.xlabel("Истинная цена")
    plt.ylabel("Предсказанная цена")
    plt.title("Факт vs Предсказание (Test)")
    plt.grid(True)
    plt.show()

# if __name__ =='__main__':
#     Model()