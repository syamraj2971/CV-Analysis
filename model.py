import pickle
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from data_prep import DataPrep
from sklearn.feature_extraction.text import TfidfVectorizer

class Model():
    def __init__(self):
        self.rfr = RandomForestRegressor(bootstrap=True,
         max_features='sqrt',
         min_samples_leaf=1,
         min_samples_split=2,
         n_estimators= 200)
        self.rfc = RandomForestClassifier(max_features='sqrt', n_estimators=110)
        self.tfidf = TfidfVectorizer(stop_words='english', strip_accents='ascii')

    def fit(self, X, y, regression=True):
        X = self.tfidf.fit_transform(X)
        if regression:
            self.rfr = self.rfr.fit(X, y)
        else:
            self.rfc = self.rfc.fit(X, y)

    def predict(self, X, regression=True):
        X = self.tfidf.transform(X)
        if regression:
            return self.rfr.predict(X)
        else:
            return self.rfc.predict(X)

    def predict_proba(self, X, regression=False):
        X = self.tfidf.transform(X)
        if regression:
            raise ValueError('Cannot predict probabilites of a regression!')
        else:
            return self.rfc.predict_proba(X)

if __name__ == '__main__':
    traits = ['OPN', 'CON', 'EXT', 'AGR', 'NEU']
    model = Model()

    for trait in traits:
        dp = DataPrep()
        X_regression, y_regression = dp.prep_data('status', trait, regression=True, model_comparison=False)
        print(len(X_regression),X_regression[0],y_regression[0])
        print("=======================================================")
        X_categorical, y_categorical = dp.prep_data('status', trait, regression=False, model_comparison=False)
        print('Fitting trait ' + trait + ' regression model...')
        print(len(X_categorical),X_categorical)
        model.fit(X_regression, y_regression, regression=True)
        print('Done!')
        print('Fitting trait ' + trait + ' categorical model...')
        model.fit(X_categorical, y_categorical, regression=False)
        print('Done!')
        with open('static/' + trait + '_model.pkl', 'wb') as f:
            # Write the model to a file.
            pickle.dump(model, f)
