import pandas as pd
import joblib
from models import random_forest_regression as rf
from sklearn.model_selection import train_test_split, GridSearchCV


def read_and_process_data(file_path):
    df = pd.read_csv(file_path)
    y = df['Price']
    df = df.drop('Price', axis=1)

    categorical_columns = ['CarBrand', 'CarModel', 'Condition', 'GearBox', 'Fuel', 'CarOrigin', 'CarType']
    df[categorical_columns] = df[categorical_columns].apply(lambda x: x.str.lower())
    df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(df, y, train_size=0.8, random_state=42)

    encoded_columns = df.columns
    joblib.dump(encoded_columns, 'models/encoded_columns.pkl')

    return X_train, X_test, y_train, y_test


def perform_grid_search(model, param_grid, X_train, y_train):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='neg_mean_absolute_error', cv=5)
    grid_search.fit(X_train, y_train)

    print("Best Hyperparameters: ", grid_search.best_params_)
    print("Best Score (Negative MAE): ", grid_search.best_score_)

    return grid_search.best_params_


def train_and_evaluate_model(model_params, X_train, X_test, y_train, y_test):
    model = rf.RandomForestRegressor(**model_params)
    rf_reg = rf.ModelRandomForestRegressor(model)
    rf_reg.train(X_train, y_train)
    rf_y_pred = rf_reg.predict(X_test)

    rf_score_mae, rf_score_rmse, rf_score_mape, rf_r2 = rf_reg.evaluate(y_test, rf_y_pred)

    joblib.dump(rf_reg, 'models/random_forest_model.pkl')

    return rf_reg, rf_y_pred, rf_score_mae, rf_score_rmse, rf_score_mape, rf_r2


def plot_results(rf_reg, X_test, y_test, rf_y_pred):
    rf_reg.plot_line(20, 5, X_test, y_test)
    rf_reg.plot_scatter(20, 5, rf_y_pred, y_test)
    rf_reg.plot_residuals(20, 5, rf_y_pred, y_test)

def load_model():
    loaded_model = joblib.load('models/random_forest_model.pkl')
    return loaded_model


if __name__ == "__main__":
    file_path = "data/processing_car.csv"
    X_train, X_test, y_train, y_test = read_and_process_data(file_path)

    model = rf.RandomForestRegressor()
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 1, 2, 3],
    }

    # best_params = perform_grid_search(model, param_grid, X_train, y_train)
    #
    # rf_reg, rf_y_pred, rf_score_mae, rf_score_rmse, rf_score_mape, rf_r2 = \
    #     train_and_evaluate_model(best_params, X_train, X_test, y_train, y_test)
    #
    # plot_results(rf_reg, X_test, y_test, rf_y_pred)


    # read model, visualize

    model = load_model()
    y_pred = model.predict(X_test)
    rf_score_mae, rf_score_rmse, rf_score_mape, rf_r2 = model.evaluate(y_test, y_pred)
    plot_results(model, X_test, y_test, y_pred)

