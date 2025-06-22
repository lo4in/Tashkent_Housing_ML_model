import numpy as np
import pickle
import pandas as pd


with open("model_data/linreg_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model_data/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("model_data/feature_names.pkl", "rb") as f:
    feature_names = pickle.load(f)


print("Введите значения для следующего объекта(oт 0 до доступного номера):")

input_dict = {}


numerical_features = ['rooms', 'live area', 'area', 'floor', 'floor max', 'ceiling height', 'appartament has']

for feature in numerical_features:
    val = float(input(f"{feature}: "))
    input_dict[feature] = val


categorical_features = {
    'location': ['Юнусабадский район', 'Мирабадский район', 'Чиланзарский район' ],  # добавь все нужные районы
    'saler type': ['Бизнес', 'Частное лицо'],
    'building type': ['Кирпичный', 'Монолитный', 'Панельный'],
    'layout': ['Раздельная', 'Смежная', 'Студия'],
    'bathroom': ['Раздельный', 'Совмещенный'],
    'repair': ['Евроремонт', 'Средний'],
    'commission': ['Да', 'Нет']
}

for category, options in categorical_features.items():
    val = input(f"{category} ({', '.join(options)}): ")
    for opt in options:
        col_name = f"{category}_{opt}"
        input_dict[col_name] = 1 if val == opt else 0


df_input = pd.DataFrame([input_dict])


for col in feature_names:
    if col not in df_input.columns:
        df_input[col] = 0 


df_input = df_input[feature_names]


X_input_scaled = scaler.transform(df_input)


predicted_log_price = model.predict(X_input_scaled)
predicted_price = np.expm1(predicted_log_price)

print(f"\nПредсказанная цена аренды: {int(predicted_price[0]):,} сум")
