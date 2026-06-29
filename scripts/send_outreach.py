import json
import os
import urllib.request

def load_env():
    env_path = "/data/automation-arbitrage/.env"
    if not os.path.exists(env_path):
        return {}
    env = {}
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

def send_automated_outreach():
    env = load_env()
    resend_api_key = env.get("RESEND_API_KEY") or os.environ.get("RESEND_API_KEY")
    queue_path = "/data/automation-arbitrage/data/outreach_queue.json"
    
    if not resend_api_key:
        print("Note: RESEND_API_KEY not found in .env. Skipping automated API dispatch.")
        print("Outreach drafts remain safely queued in outreach_queue.json.")
        return
        
    if not os.path.exists(queue_path):
        print("Error: Outreach queue not found at " + queue_path)
        return
        
    with open(queue_path, "r", encoding="utf-8") as f:
        queue = json.load(f)
        
    pending = [email for email in queue if email.get("status") == "pending_send"]
    
    if not pending:
        print("No pending emails to send.")
        return
        
    print(f"Starting B2B dispatch for {len(pending)} campaign(s)...")
    
    # We load custom sending domain or default to resend's onboarded address
    # Resend allows sending from re_onboarding@resend.dev by default for testing
    from_address = env.get("OUTREACH_FROM_EMAIL", "Zac Giles <onboarding@resend.dev>")
    
    success_count = 0
    for email in pending:
        payload = {
            "from": from_address,
            "to": [email["recipient_email"]],
            "subject": email["subject"],
            "text": email["body"]
        }
        
        req = urllib.request.Request(
            "https://api.resend.com/emails",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                status = response.status
                res_data = response.read()
            if status in (200, 201):
                email["status"] = "sent"
                success_count += 1
                print(f"Campaign successfully delivered to {email['recipient_email']}")
            else:
                print(f"Failed to deliver to {email['recipient_email']}. Status code: {status}")
        except Exception as e:
            print(f"Error during API delivery to {email['recipient_email']}: {e}")
            
    # Save sent status back to local queue
    with open(queue_path, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)
        
    print(f"Dispatch complete. Successfully sent {success_count} emails.")

if __name__ == "__main__":
    send_automated_outreach()
