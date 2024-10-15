import pandas as pd
from numpy import *
import numpy as np
from sklearn import preprocessing
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn import neighbors
import pickle
from sklearn.model_selection import train_test_split
data = pd.read_csv('train.csv')
array = data.values
# print(array)

# processing data
for i in range(len(array)):
    if array[i][0] == "Male":
        array[i][0] = 1
    else:
        array[i][0] = 0

# print(array)

df = pd.DataFrame(array)

# print(df.head())

maindf = df[[0, 1, 2, 3, 4, 5, 6]]
mainarray = maindf.values
print(mainarray)

temp = df[7]
train_y = temp.values
# print(train_y)
# print(mainarray)
train_y = temp.values

for i in range(len(train_y)):
    train_y[i] = str(train_y[i])


mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg', max_iter=1000)
mul_lr.fit(mainarray, train_y)





# save the model to disk
pickle.dump(mul_lr, open("./model.pkl", 'wb'))







from sklearn.metrics import confusion_matrix
X_train, X_test, y_train, y_test = train_test_split( mainarray, train_y, test_size=0.33, random_state=42)




y_pred = mul_lr.predict(X_test)
for i in range(len(y_pred)) :
    y_pred[i]=str((y_pred[i]))



for i in range(len(y_test)) :
    y_test[i]=str((y_test[i]))

from sklearn.metrics import confusion_matrix
print("confusion_matrix")
print(confusion_matrix(y_test, y_pred))


# Finding precision and recall
from sklearn.metrics import precision_score, recall_score
print("precision_score")
print(precision_score(y_test, y_pred ,average='macro'))
print("recall_score")
print(recall_score(y_test, y_pred, average='macro'))

# To compute the F1 score, simply call the f1_score() function:
from sklearn.metrics import f1_score

print("f1_score")
print(f1_score(y_test, y_pred, average='macro'))

from sklearn.metrics import accuracy_score
print("accuracy_score")
print(accuracy_score(y_test, y_pred))

DF = pd.DataFrame(y_pred,columns=['Predicted Personality.'])
DF.index=DF.index+1
DF.index.names = ['Person No']
DF.to_csv("output.csv")

