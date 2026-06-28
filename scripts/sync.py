import json
import os
import urllib.request

def sync_leads():
    leads_path = "/data/automation-arbitrage/data/leads_master.json"
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if not os.path.exists(leads_path):
        print(f"No leads master file found at {leads_path}")
        return
        
    try:
        with open(leads_path, "r", encoding="utf-8") as f:
            leads = json.load(f)
    except Exception as e:
        print(f"Error loading leads file: {e}")
        return

    # Filter out leads that are already synced
    unsynced_leads = [l for l in leads if not l.get("synced", False)]
    
    if not unsynced_leads:
        print("No new unsynced leads found.")
        return
        
    print(f"Found {len(unsynced_leads)} unsynced leads.")
    
    if not supabase_url or not supabase_key:
        print("SUPABASE_URL or SUPABASE_KEY environment variables not set. Skipping remote sync.")
        print("Leads will remain saved locally in leads_master.json.")
        return

    # Format endpoint (e.g. Supabase REST API endpoint for a 'leads' table)
    # Typically: {supabase_url}/rest/v1/leads
    endpoint = f"{supabase_url.rstrip('/')}/rest/v1/leads"
    
    print(f"Syncing {len(unsynced_leads)} leads to Supabase REST API...")
    
    # We sync in batches or individually. Let's do a batch request as per standard Supabase REST API
    # Headers: apikey, Authorization, Content-Type, Prefer (resolution of duplicates)
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }
    
    # We only POST the fields without the 'synced' metadata field to Supabase
    payload_leads = []
    for lead in unsynced_leads:
        payload_lead = {k: v for k, v in lead.items() if k != "synced"}
        payload_leads.append(payload_lead)
        
    try:
        data = json.dumps(payload_leads).encode("utf-8")
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req) as response:
            status = response.status
            
        if status in (200, 201):
            print("Successfully synced leads to Supabase!")
            # Mark them as synced in our local JSON
            for lead in leads:
                if not lead.get("synced", False):
                    lead["synced"] = True
                    
            with open(leads_path, "w", encoding="utf-8") as f:
                json.dump(leads, f, indent=2)
            print("Local leads database updated with sync status.")
        else:
            print(f"Failed to sync. Server returned status code: {status}")
            
    except Exception as e:
        print(f"Error syncing to Supabase: {e}")

if __name__ == "__main__":
    sync_leads()
