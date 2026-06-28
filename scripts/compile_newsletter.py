import json
import os
from datetime import datetime

def compile_newsletter():
    leads_path = "/data/automation-arbitrage/data/leads_master.json"
    output_path = "/data/automation-arbitrage/data/weekly_digest.md"
    
    if not os.path.exists(leads_path):
        print(f"Error: Leads file not found at {leads_path}")
        return
        
    try:
        with open(leads_path, "r", encoding="utf-8") as f:
            leads = json.load(f)
    except Exception as e:
        print(f"Error reading leads: {e}")
        return

    premium_leads = []
    
    for lead in leads:
        # Extract fields
        ceiling = lead.get("funding_ceiling")
        applicants = lead.get("eligible_applicants", [])
        
        # Flex check for Nonprofits in applicants list (case-insensitive)
        is_nonprofit_eligible = any("nonprofit" in app.lower() for app in applicants)
        
        # Filter condition: is nonprofit eligible AND (ceiling is None/null OR ceiling >= 100000)
        if is_nonprofit_eligible and (ceiling is None or ceiling >= 100000):
            premium_leads.append(lead)
            
    print(f"Filtered {len(premium_leads)} premium opportunities from {len(leads)} total leads.")

    # Today's date for header
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Generate Markdown content
    md = []
    md.append(f"# Premium Grant Intelligence Digest")
    md.append(f"**Curated High-Value Funding Opportunities for Nonprofits**")
    md.append(f"**Release Date**: {current_date} | *Giles Industries Automated Intelligence Layer*\n")
    md.append("---")
    md.append("\n## High-Value Opportunities This Week\n")
    
    if not premium_leads:
        md.append("*No premium funding opportunities matching criteria found in this batch.*")
    else:
        for idx, lead in enumerate(premium_leads, 1):
            title = lead.get("opportunity_title", "No Title")
            grant_id = lead.get("grant_id", "N/A")
            agency = lead.get("agency", "Unknown Agency")
            ceiling = lead.get("funding_ceiling")
            close_date = lead.get("close_date", "Unspecified")
            url = lead.get("source_url", "#")
            
            # Format ceiling
            ceiling_str = f"${ceiling:,}" if isinstance(ceiling, (int, float)) else "Unspecified / Open Budget"
            
            md.append(f"### {idx}. {title}")
            md.append(f"- **Grant ID**: `{grant_id}`")
            md.append(f"- **Issuing Agency**: {agency}")
            md.append(f"- **Ceiling Funding**: **{ceiling_str}**")
            md.append(f"- **Close Date / Deadline**: *{close_date}*")
            md.append(f"- **Direct Application Link**: [Apply on Grants.gov]({url})")
            md.append("\n---")
            
    md.append("\n\n*This digest is compiled automatically. For premium custom matching or custom integration assistance, contact your Giles Industries Virtual COO representative.*")

    # Save to output_path
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
        
    print(f"Successfully generated newsletter and saved to {output_path}")

if __name__ == "__main__":
    compile_newsletter()
