# Wczytaj dane z pliku JSON
import numpy as np
import pandas as pd

# Wczytaj dane z pliku JSON
df = pd.read_json("mileage.json")

# Przekształć kolumnę "Data" do formatu daty
df["Date"] = pd.to_datetime(df["Date"])
# Usuń nawiasy kwadratowe i cudzysłowy
df["Mileage"] = (
    df["Mileage"].str.replace("[", "").str.replace("]", "").str.replace("'", "")
)
# Przekształć kolumnę "Przebieg" do formatu liczbowego
df["Mileage"] = df["Mileage"].astype(int)

print(df[0:3])

# Posortuj DataFrame według daty
df = df.sort_values("Date")

import matplotlib.pyplot as plt

# ---
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

# Oblicz trend liniowy
x = np.array(range(len(df))).reshape(-1, 1)
y = df["Mileage"].values
model = LinearRegression().fit(x, y)
trend = model.predict(x)

# Oblicz odległość każdego punktu od linii trendu
distances = np.abs(y - trend)

# Podziel odległości na 2 grupy za pomocą K-Means
kmeans = KMeans(n_clusters=2, random_state=0).fit(distances.reshape(-1, 1))
df["group"] = kmeans.labels_

# Wyodrębnij grupy
group1 = df[df["group"] == 0]
group2 = df[df["group"] == 1]

# Wykres dla grupy 1
plt.plot(group1["Date"], group1["Mileage"], label="Group 1", linestyle="", marker="o")

# Wykres dla grupy 2
plt.plot(group2["Date"], group2["Mileage"], label="Group 2", linestyle="", marker="o")

# Dodaj legendę
plt.legend()

# Wyświetl wykres
plt.show()

# Wyodrębnij podgrupy z grupy 1 na podstawie kolumny 'Type'
group1_car = group1[group1["Type"] == "car"]
group1_truck = group1[group1["Type"] == "truck"]

# Wykres dla grupy 1 typu car
plt.plot(
    group1_car["Date"],
    group1_car["Mileage"],
    label="L3H2",
    linestyle="",
    marker="o",
    color="red",
)

# Wykres dla grupy 1 typu truck
plt.plot(
    group1_truck["Date"],
    group1_truck["Mileage"],
    label="L4H2",
    linestyle="",
    marker="o",
    color="green",
)

# Wykres dla grupy 2
plt.plot(
    group2["Date"],
    group2["Mileage"],
    label="Osobowy",
    linestyle="",
    marker="o",
    color="blue",
)

# Dodaj legendę
plt.legend()

# Wyświetl wykres
plt.show()
