import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

CLUSTER_COLOURS={
    "High Value Youth" : "#00e676",
    "Attack Core"      : "#ff6b35",
    "Reliable Squad"   :"#4fc3f7",
    "Veteran Depth"    : "#9e9e9e",
    }

def scatter_age_value(df):
    fig=px.scatter(
        df,
        x="Age",
        y="Market Value_m",
        color="cluster_label",
        hover_name="Name",
        size="Market Value_m",
        color_discrete_map=CLUSTER_COLOURS,
        title="Player Age vs Market Value - Clustered By Playing style",
        labels={"Market Value_m":"Market Value (€M)","Age":"Age"}

    )
    fig.update_layout(template="plotly_dark")
    return fig
def correlation_heatmap(df):
    corr=df[["Age","Market Value_m","Position_code"]].corr()
    plt.figure(figsize=(6,5))
    sns.heatmap(corr,annot=True,cmap="coolwarm",fmt=".2f",linewidths=0.5)
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.show()

def position_bar(df):
    counts=df.groupby(["Position","cluster_label"]).size().reset_index(name="count")
    fig=px.bar(
        counts,
        x="Position",
        y="count",
        color="cluster_label",
        color_discrete_map=CLUSTER_COLOURS,
        title="Cluster Distribution by Position",
        barmode="stack"

    )
    fig.update_layout(template="plotly_dark", xaxis_tickangle=-45)
    return fig    