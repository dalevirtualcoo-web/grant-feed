import json
import os
from datetime import datetime

def compile_calendar():
    leads_path = "/data/automation-arbitrage/data/leads_master.json"
    output_path = "/data/automation-arbitrage/data/grant_calendar.ics"
    
    if not os.path.exists(leads_path):
        print(f"Error: Leads database not found at {leads_path}")
        return
        
    try:
        with open(leads_path, "r", encoding="utf-8") as f:
            leads = json.load(f)
    except Exception as e:
        print(f"Error reading leads: {e}")
        return

    print(f"Loaded {len(leads)} leads for calendar compilation.")

    # ICS File Header
    ics = []
    ics.append("BEGIN:VCALENDAR")
    ics.append("VERSION:2.0")
    ics.append("PRODID:-//Giles Industries//Giles Grant Intelligence//EN")
    ics.append("CALSCALE:GREGORIAN")
    ics.append("METHOD:PUBLISH")
    ics.append("X-WR-CALNAME:Free Grant Deadlines Feed")
    ics.append("X-WR-TIMEZONE:UTC")
    ics.append("X-WR-CALDESC:Real-time federal grant opportunity deadlines. Provided by Giles Grant Intelligence (GGI).")

    for lead in leads:
        title = lead.get("opportunity_title", "Grant Opportunity")
        grant_id = lead.get("grant_id", "N/A")
        agency = lead.get("agency", "Unknown Agency")
        close_date = lead.get("close_date")
        url = lead.get("source_url", "https://dalevirtualcoo-web.github.io/grant-feed/data/index.html")
        
        # If no valid close date, we cannot place it on the calendar
        if not close_date or close_date == "Unspecified":
            continue
            
        try:
            # Parse YYYY-MM-DD
            dt = datetime.strptime(close_date, "%Y-%m-%d")
            # Format for ICS All-Day Event (DTSTART;VALUE=DATE:YYYYMMDD)
            date_str = dt.strftime("%Y%m%d")
            
            # Unique UID for each event to prevent calendar duplication
            uid = f"grant-{grant_id}-deadline@gilesindustries.com"
            
            ics.append("BEGIN:VEVENT")
            ics.append(f"UID:{uid}")
            ics.append(f"DTSTART;VALUE=DATE:{date_str}")
            ics.append(f"DTEND;VALUE=DATE:{date_str}")
            ics.append(f"SUMMARY:DEADLINE: {grant_id} - {title[:60]}...")
            
            # Event Description with our upgrade pitch and direct links
            description = (
                f"Grant ID: {grant_id}\\n"
                f"Issuing Agency: {agency}\\n\\n"
                f"This is a public, open-access grant tracker provided by Giles Grant Intelligence (GGI).\\n\\n"
                f"Upgrade to our Premium Feed to unlock full application links and locked 7-figure opportunities: "
                f"https://dalevirtualcoo-web.github.io/grant-feed/data/index.html#pricing"
            )
            ics.append(f"DESCRIPTION:{description}")
            ics.append(f"URL;VALUE=URI:{url}")
            ics.append("STATUS:CONFIRMED")
            ics.append("SEQUENCE:0")
            ics.append("END:VEVENT")
        except Exception as e:
            print(f"Error parsing date {close_date} for grant {grant_id}: {e}")

    ics.append("END:VCALENDAR")

    # Ensure data directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(ics))
        
    print(f"Successfully compiled Grant iCal calendar and saved to {output_path}")

if __name__ == "__main__":
    compile_calendar()
