import pickle 
from model import Model

M, S, feature = Model()


with open("model_data/linreg_model.pkl", "wb") as f:
    pickle.dump(M, f)

with open("model_data/scaler.pkl", "wb") as f:
    pickle.dump(S, f)


feature_names = feature
with open("model_data/feature_names.pkl", "wb") as f:
    pickle.dump(feature_names, f)