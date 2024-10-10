import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
import pickle

current_dir = os.getcwd()
file_path = os.path.join(current_dir, 'penguins_cleaned.csv')
try:
    penguins = pd.read_csv(file_path)
    
    df = penguins.copy()
    target = 'species'
    encode = ['sex','island']
    
    for col in encode:
        dummy = pd.get_dummies(df[col], prefix=col, dtype=int) #  returns a DataFrame where categorical variables are converted into dummy or indicator variables
        df = pd.concat([df, dummy], axis=1)
        del df[col]
    
    target_map = {'Adelie': 0, 'Chinstrap': 1, 'Gentoo': 2}
    def target_encode(val):
        return target_map[val]
    
    df['species'] = df['species'].apply(target_encode)
    
    X = df.drop('species', axis=1)
    Y = df['species']
    
    clf = RandomForestClassifier()
    clf.fit(X, Y)
    
    pickle.dump(clf, open('penguins_clf.pkl', 'wb'))

except Exception as e:
    print(f"An error occurred: {str(e)}")