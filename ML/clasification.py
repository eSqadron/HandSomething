import numpy as np
import sklearn
from sklearn import tree
import pandas as pd
from sklearn import model_selection
import numpy as np
import pickle

file_list = ["LED_R.csv", "LED_G.csv", "LED_B.csv", "Door.csv", "SYF.csv"]
data = []

for file in file_list:
    new_data = pd.read_csv(file, sep=",").values.tolist()
    data = data + new_data
    

df = pd.DataFrame(data)

df = df.sample(frac=1).reset_index(drop=True)

df_array = df.to_numpy()

X = df_array[:,:-1]
y = df_array[:,-1]

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3, random_state = 42)

clf = tree.DecisionTreeClassifier(max_depth=10)
clf.fit(X_train, y_train)

print(clf.predict_proba(X_test))
print(clf.score(X_test, y_test))

pickle.dump(clf, open("model.sav", "wb"))

