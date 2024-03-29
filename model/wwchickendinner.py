## Python Titanic Model, prepared for a wwchickendinner.py file

# Import the required libraries for the TitanicModel class
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder



import pandas as pd
import numpy as np
import seaborn as sns
import json
import os


# {
#     "name": "AI-90002",
#     "age": 22,
#     "sex": "male",
#     "favoritegame": "Maze",
#     "dominanthand": "left",
#     "operatingsystem": "PC",
#     "survivied": 1
#     "year":3
# }
class WwchickendinnerModel:
    """A class used to represent the Titanic Model for passenger survival prediction.
    """
    # a singleton instance of TitanicModel, created to train the model only once, while using it for prediction multiple times
    _instance = None
    
    # constructor, used to initialize the TitanicModel
    def __init__(self):
        # the wwchickendinner ML model
        self.model = None
        self.dt = None
        # define ML features and target
        # self.features = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'alone']
        self.features = ['age', 'sex', 'favoritegame', 'dominanthand', 'operatingsystem', 'years']
        self.target = 'survived'
        # load the wwchickendinner dataset

        self.wwchickendinner_data = pd.read_json('/mnt/c/Users/tthin/group-backend/model/wwchickendinner_data.json')
        print(self.wwchickendinner_data)    
        # self.wwchickendinner_data = sns.load_dataset('titanic')
        # one-hot encoder used to encode 'embarked' column
        self.encoder = OneHotEncoder(handle_unknown='ignore')

    # clean the wwchickendinner dataset, prepare it for training
    def _clean(self):
        # Drop unnecessary columns
        # self.wwchickendinner_data.drop(['alive', 'who', 'adult_male', 'class', 'embark_town', 'deck'], axis=1, inplace=True)

        # Convert boolean columns to integers
        self.wwchickendinner_data['sex'] = self.wwchickendinner_data['sex'].apply(lambda x: 1 if x == 'male' else 0)
        self.wwchickendinner_data['dominanthand'] = self.wwchickendinner_data['dominanthand'].apply(lambda x: 1 if x == 'left' else 0)
        self.wwchickendinner_data['favoritegame'] = self.wwchickendinner_data['favoritegame'].apply(lambda x: 1 if x == 'galaxy' else 0)
        self.wwchickendinner_data['operatingsystem'] = self.wwchickendinner_data['operatingsystem'].apply(lambda x: 1 if x == 'pc' else 0)
        #self.wwchickendinner_data['alone'] = self.wwchickendinner_data['alone'].apply(lambda x: 1 if x == True else 0)

        # Drop rows with missing 'embarked' values before one-hot encoding
        # self.wwchickendinner_data.dropna(subset=['embarked'], inplace=True)
        
        # One-hot encode 'embarked' column
        # onehot = self.encoder.fit_transform(self.wwchickendinner_data[['embarked']]).toarray()
        # cols = ['embarked_' + str(val) for val in self.encoder.categories_[0]]
        # onehot_df = pd.DataFrame(onehot, columns=cols)
        # self.wwchickendinner_data = pd.concat([self.wwchickendinner_data, onehot_df], axis=1)
        # self.wwchickendinner_data.drop(['embarked'], axis=1, inplace=True)

        # Add the one-hot encoded 'embarked' features to the features list
        # self.features.extend(cols)
        
        # Drop rows with missing values
        self.wwchickendinner_data.dropna(inplace=True)

    # train the wwchickendinner model, using logistic regression as key model, and decision tree to show feature importance
    def _train(self):
        # split the data into features and target
        X = self.wwchickendinner_data[self.features]
        y = self.wwchickendinner_data[self.target]
        
        # perform train-test split
        self.model = LogisticRegression(max_iter=1000)
        
        # train the model
        self.model.fit(X, y)
        
        # train a decision tree classifier
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)

    
        
    @classmethod
    def get_instance(cls):
        """ Gets, and conditionaly cleans and builds, the singleton instance of the TitanicModel.
        The model is used for analysis on wwchickendinner data and predictions on the survival of theoritical passengers.
        
        Returns:
            TitanicModel: the singleton _instance of the TitanicModel, which contains data and methods for prediction.
        """        
        # check for instance, if it doesn't exist, create it
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        # return the instance, to be used for prediction
        return cls._instance

    def predict(self, passenger):
        """ Predict the survival probability of a passenger.

        Args:
            passenger (dict): A dictionary representing a passenger. The dictionary should contain the following keys:
                'pclass': The passenger's class (1, 2, or 3)
                'sex': The passenger's sex ('male' or 'female')
                'age': The passenger's age
                'sibsp': The number of siblings/spouses the passenger has aboard
                'parch': The number of parents/children the passenger has aboard
                'fare': The fare the passenger paid
                'embarked': The port at which the passenger embarked ('C', 'Q', or 'S')
                'alone': Whether the passenger is alone (True or False)

        Returns:
           dictionary : contains die and survive probabilities 
        """
        
        print(passenger)
        # clean the passenger data
        passenger_df = pd.DataFrame(passenger, index=[0])
        # passenger_df['sex'] = passenger_df['sex'].apply(lambda x: 1 if x == 'male' else 0)
        passenger_df['sex'] = passenger_df['sex'].apply(lambda x: 1 if x == 'male' else 0)
        passenger_df['dominanthand'] = passenger_df['dominanthand'].apply(lambda x: 1 if x == 'left' else 0)
        passenger_df['favoritegame'] = passenger_df['favoritegame'].apply(lambda x: 1 if x == 'galaxy' else 0)
        passenger_df['operatingsystem'] = passenger_df['operatingsystem'].apply(lambda x: 1 if x == 'pc' else 0)
        
        # passenger_df['alone'] = passenger_df['alone'].apply(lambda x: 1 if x == True else 0)
        # onehot = self.encoder.transform(passenger_df[['embarked']]).toarray()
        # cols = ['embarked_' + str(val) for val in self.encoder.categories_[0]]
        # onehot_df = pd.DataFrame(onehot, columns=cols)
        # passenger_df = pd.concat([passenger_df, onehot_df], axis=1)
        passenger_df.drop(['name'], axis=1, inplace=True)
        

        # predict the survival probability and extract the probabilities from numpy array
        die, survive = np.squeeze(self.model.predict_proba(passenger_df))
        # return the survival probabilities as a dictionary
        return {'die': die, 'survive': survive}
    
    def feature_weights(self):
        """Get the feature weights
        The weights represent the relative importance of each feature in the prediction model.

        Returns:
            dictionary: contains each feature as a key and its weight of importance as a value
        """
        # extract the feature importances from the decision tree model
        importances = self.dt.feature_importances_
        # return the feature importances as a dictionary, using dictionary comprehension
        return {feature: importance for feature, importance in zip(self.features, importances)} 
    
def initWwchickendinner():
    """ Initialize the Titanic Model.
    This function is used to load the Titanic Model into memory, and prepare it for prediction.
    """
    WwchickendinnerModel.get_instance()
    
def testWwchickendinner():
    """ Test the Titanic Model
    Using the TitanicModel class, we can predict the survival probability of a passenger.
    Print output of this test contains method documentation, passenger data, survival probability, and survival weights.
    """
     
    # setup passenger data for prediction
    print(" Step 1:  Define theoritical passenger data for prediction: ")
    passenger = {
        'name': ['John Mortensen'],
        'pclass': [2],
        'sex': ['male'],
        'age': [64],
        'sibsp': [1],
        'parch': [1],
        'fare': [16.00],
        'embarked': ['S'],
        'alone': [False]
    }
    print("\t", passenger)
    print()

    # get an instance of the cleaned and trained Titanic Model
    wwchickendinnerModel = WwchickendinnerModel.get_instance()
    print(" Step 2:", wwchickendinnerModel.get_instance.__doc__)
   
    # print the survival probability
    print(" Step 3:", wwchickendinnerModel.predict.__doc__)
    probability = wwchickendinnerModel.predict(passenger)
    print('\t death probability: {:.2%}'.format(probability.get('die')))  
    print('\t survival probability: {:.2%}'.format(probability.get('survive')))
    print()
    
    # print the feature weights in the prediction model
    print(" Step 4:", wwchickendinnerModel.feature_weights.__doc__)
    importances = wwchickendinnerModel.feature_weights()
    for feature, importance in importances.items():
        print("\t\t", feature, f"{importance:.2%}") # importance of each feature, each key/value pair
        
if __name__ == "__main__":
    print(" Begin:", testWwchickendinner.__doc__)
    testWwchickendinner()