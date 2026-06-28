import urllib.request
import json
import os

def ingest_data():
    url = "https://api.grants.gov/v1/api/search2"
    output_path = "/data/automation-arbitrage/data/raw_input.txt"
    payload = {"oppStatuses": "posted", "rows": 20}
    
    print(f"Sending POST request to Grants.gov search API: {url}")
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, 
            data=data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            },
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            res_data = response.read()
            
        res_json = json.loads(res_data.decode("utf-8"))
        opp_hits = res_json.get("data", {}).get("oppHits", [])
        
        if not opp_hits:
            print("Warning: No opportunities found in the API response.")
            
        # Write clean, raw string payload (formatted JSON list) to raw_input.txt
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(opp_hits, f, indent=2)
            
        print(f"Successfully ingested {len(opp_hits)} live records into {output_path}")
        return True
    except Exception as e:
        print(f"Error during Grants.gov API ingestion: {e}")
        return False

if __name__ == "__main__":
    ingest_data()
