import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def load_and_preprocess(path = 'data/full_olx_dataset.csv'):
    df1 = pd.read_csv(path)


    df = df1.drop(['name', 'link', 'date', 'kitchen area', 'Year of construction', 'near by'], axis =1)
    

    df[['building type', 'layout', 'bathroom', 'repair']] = df[['building type', 'layout', 'bathroom', 'repair']].fillna('Unknown')

    df = pd.get_dummies(df, columns =['location', 'saler type', 'building type', 'layout', 'bathroom', 'furnished', 'repair', 'commission'], dummy_na=False)

    # print(df.isna().sum())




    df['live area'] = (
        df['live area']
        .astype(str)
        .str.replace("м²", "", regex=False)
        .str.replace(" ", "")  
        .str.strip()
        .astype(float)
        .replace(["", "nan", "None"], pd.NA)
    )

    df = df.applymap(lambda x: x.replace(" ", "") if isinstance(x, str) else x)






    df['appartament has'] = df['appartament has'].fillna("").apply(lambda x: len(x.split(',')))


    # plt.show()
    def normalize_ceiling(value):
        try:
            value = float(str(value).strip())
            return value / 100 if value > 10 else value
        except:
            return np.nan  

    df['ceiling height'] = df['ceiling height'].apply(normalize_ceiling)

    # print(df['ceiling height'])


    from sklearn.impute import SimpleImputer

    imputer = SimpleImputer(strategy='mean')

    imputer.fit(df)

    a = imputer.transform(df)

    data = pd.DataFrame(data = a, columns = df.columns)




    # print(data.isna().sum()/len(df))




    # data['price_USD'] = data['price']/12565.88
    pop = data['price'].quantile(0.99)
    mean_price = data['price'].mean()

    data.loc[data['price'] > pop, 'price'] = mean_price






    g = data['rooms'].quantile(0.99)
    data.loc[data['rooms'] > g, 'rooms'] = g

    data['rooms'].hist(bins = 100)



    l = data['live area'].quantile(0.99)

    data.loc[data['live area'] > l, 'live area'] = l

    m = data['area'].quantile(0.99)

    data.loc[data['area'] > m, 'area'] = m


    # data['area'].hist(bins= 100)
    # plt.show()
    data = data[data['ceiling height'] >= 2.0]

    #print(data['live area'].describe().T)
    
    data = data[data['live area'] >= 30]
    data = data[data['area'] >= 30]
    
    data = data[data['price'] <= 15000000]

    data = data.drop(columns=[col for col in data.columns if col.startswith('furnished_')])

    data['floor_ratio'] = data['floor'] / data['floor max']
    data['room_density'] = data['area'] / data['rooms']
    data['price_per_m2'] = data['price'] / data['area']
    # data['price'] = np.log1p(data['price'])  # перед скейлингом

    # print(data.describe().T)
    # print(data.describe().T)

    return data



# if __name__ == '__main__':


#     load_and_preprocess()
