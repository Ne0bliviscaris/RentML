import pandas as pd
from sklearn.neighbors import KNeighborsClassifier


def predict_car(mileage, date, df, car_type=None):
    """Predict car model based on mileage and date"""
    if car_type:
        df = df[df["Car type"] == car_type]

    df = df.copy()
    df["date_ordinal"] = df["Date"].map(pd.Timestamp.toordinal)

    model = KNeighborsClassifier(n_neighbors=3)
    x_train = df[["date_ordinal", "Mileage"]]
    model.fit(x_train, df["Car"])

    date_ordinal = pd.Timestamp(date).toordinal()
    prediction = model.predict(pd.DataFrame([[date_ordinal, mileage]], columns=x_train.columns))
    return prediction[0]
