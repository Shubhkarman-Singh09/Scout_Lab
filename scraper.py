import requests
HEADERS={
    "User-Agent":(
        "Mozilla/5.0(Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36(KHTML,like Gecko)"
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language":"en-US,en;q=0.9",
    "Accept":"text/html,application/xhtml+xml,application/xml:q=0.9,*/*;q=0/8"
}
def fetch_squad(team_id:str,team_slug:str)->str:
    url=f"https://www.transfermarkt.com/{team_slug}/kader/verein/{team_id}"
    response=requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text
