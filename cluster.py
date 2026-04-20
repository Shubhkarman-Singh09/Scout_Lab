import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

FEATURES=["Age","Market Value_m","Position_code"]

CLUSTER_LABELS={
    0: "Veteran Depth",
    1: "Reliable Defenders",
    2: "Attack Core",
    3: "High Value Youth"

}
def find_optimal_k(df:pd.DataFrame):
    X=df[FEATURES]
    scaler=StandardScaler()
    X_scaled=scaler.fit_transform(X)

    intertias=[]
    k_range=range(2,9)

    for k in k_range:
        km=KMeans(n_clusters=k,random_state=42,n_init=10)
        km.fit(X_scaled)
        intertias.append(km.inertia_)
    
    plt.figure(figsize=(8,4))
    plt.plot(k_range,intertias,"bo-",linewidth=2,markersize=6)
    plt.xlabel("Number of Cluster K")
    plt.ylabel("Inertia")
    plt.title("Elbow-Method,Pick K at bend")
    plt.tight_layout()
    plt.show()

def cluster_players(df: pd.DataFrame, k: int = 4) -> pd.DataFrame:
    df = df.copy()
    X = df[FEATURES].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    df["cluster"] = km.fit_predict(X_scaled)

    profiles = df.groupby("cluster")[FEATURES].mean()

    # assign labels based on actual data, not assumptions
    def label_cluster(row):
        if row["Market Value_m"] > 80:
            return "High Value Youth"
        elif row["Age"] > 33 and row["Market Value_m"] < 10:
            return "Veteran Depth"
        elif row["Position_code"] >= 6:
            return "Attack Core"
        else:
            return "Reliable Squad"

    cluster_label_map = {
        c: label_cluster(profiles.loc[c]) for c in profiles.index
    }

    print("\nCluster profiles:")
    print(profiles.round(1))
    print("\nLabel mapping:", cluster_label_map)

    df["cluster_label"] = df["cluster"].map(cluster_label_map)
    return df
