import pandas as pd
def clean_market_value(val:str)-> float:
    val=val.replace("€", "").replace(",", "").strip()
    if "m" in val:
        return float(val.replace("m",""))
    if"k" in val:
        return float(val.replace("k",""))/1000
    return 0.0
POSITION_MAP={
    "Goalkeeper"        : 1,
    "Centre-Back"       : 2,
    "Left-Back"         : 3,
    "Right-Back"        : 3,
    "Defensive Midfield": 4,
    "Central Midfield"  : 5,
    "Attacking Midfield": 6,
    "Left Winger"       : 7,
    "Right Winger"      : 7,
    "Second Striker"    : 8,
    "Centre-Forward"    : 9,
}

def engineer_features(df: pd.DataFrame)->pd.DataFrame:
    df=df.copy()
    df["Age"]= pd.to_numeric(df["Age"],errors="coerce")
    df["Market Value_m"]=df["Market Value"].apply(clean_market_value)
    df["Position_code"]=df["Position"].map(POSITION_MAP).fillna(5)
    df.dropna(subset=["Age","Market Value_m"],inplace=True)
    df.reset_index(drop=True,inplace=True)

    return df



    