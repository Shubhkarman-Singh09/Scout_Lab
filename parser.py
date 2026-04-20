from bs4 import BeautifulSoup
import pandas as pd
def parse_squad(html:str)-> pd.DataFrame:
    soup=BeautifulSoup(html,"lxml")

    rows=soup.find_all("tr",class_=["odd","even"])
    print(f"find{len(rows)} rows")

    players=[]
    for row in rows:
        name_tag=row.find("td",class_="hauptlink")
        if not name_tag:
            continue

        name=name_tag.get_text(strip=True)
        tds=row.find_all("td")
        img_tag = row.find("img", class_="bilderrahmen-fixed")
        photo = (
        img_tag.get("data-src")
        or img_tag.get("data-lazy-src")
        or "https://img.a.transfermarkt.technology/portrait/header/default.jpg"
        ) if img_tag else "https://img.a.transfermarkt.technology/portrait/header/default.jpg"

        player={
            "Jersey Number":tds[0].get_text(strip=True),
            "Name":     tds[3].get_text(strip=True),
            "Position": tds[4].get_text(strip=True),
            "Age":      tds[5].get_text(strip=True),
            "Contract": tds[7].get_text(strip=True),
            "Market Value": tds[8].get_text(strip=True),
            "Photo"       : photo
        }
        players.append(player)
    
    return pd.DataFrame(players)

if __name__ == "__main__":
    with open("data/raw.html", "r", encoding="utf-8") as f:
        html = f.read()
    df = parse_squad(html)
    print(df[["Name", "Photo"]].to_string())
