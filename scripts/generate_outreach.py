import json
import os

def generate_outreach_templates():
    prospects = [
        {
            "non_profit_name": "The Center for Mind-Body Medicine",
            "website": "https://cmbm.org",
            "location": "Washington, DC",
            "executive_name": "James S. Gordon, MD",
            "executive_title": "Founder & CEO",
            "contact_email": "info@cmbm.org",
            "target_grant": "PAR-25-274",
            "grant_match_rationale": "Specializes in clinical-level mind-body and trauma-relief training/intervention trials.",
            "grant_title": "Feasibility Clinical Trials of Mind and Body Interventions for NCCIH High Priority Research Topics",
            "funding_ceiling": 225000,
            "deadline": "November 17, 2026"
        },
        {
            "non_profit_name": "Mind & Life Institute",
            "website": "https://www.mindandlife.org",
            "location": "Charlottesville, VA",
            "executive_name": "Sheila Kinkade",
            "executive_title": "Head of Strategic Communications & Foundation Relations",
            "contact_email": "info@mindandlife.org",
            "target_grant": "PAR-25-274",
            "grant_match_rationale": "An anchor institution funding and evaluating contemplative science and mind-body research.",
            "grant_title": "Feasibility Clinical Trials of Mind and Body Interventions for NCCIH High Priority Research Topics",
            "funding_ceiling": 225000,
            "deadline": "November 17, 2026"
        },
        {
            "non_profit_name": "Institute of Noetic Sciences (IONS)",
            "website": "https://noetic.org",
            "location": "Novato, CA",
            "executive_name": "Helané Wahbeh",
            "executive_title": "Director of Research",
            "contact_email": "membership@noetic.org",
            "target_grant": "PAR-25-274",
            "grant_match_rationale": "Conducts dedicated clinical and direct-experience wellness studies in an active lab setting.",
            "grant_title": "Feasibility Clinical Trials of Mind and Body Interventions for NCCIH High Priority Research Topics",
            "funding_ceiling": 225000,
            "deadline": "November 17, 2026"
        },
        {
            "non_profit_name": "Humin",
            "website": "https://www.humin.org",
            "location": "Madison, WI",
            "executive_name": "Christina Glavas",
            "executive_title": "CEO",
            "contact_email": "info@humin.org",
            "target_grant": "PAR-25-274",
            "grant_match_rationale": "Translates emotional neuroscientific research into practical wellness tools and clinical interventions.",
            "grant_title": "Feasibility Clinical Trials of Mind and Body Interventions for NCCIH High Priority Research Topics",
            "funding_ceiling": 225000,
            "deadline": "November 17, 2026"
        },
        {
            "non_profit_name": "Multidisciplinary Association for Psychedelic Studies (MAPS)",
            "website": "https://maps.org",
            "location": "San Jose, CA",
            "executive_name": "Rick Doblin, Ph.D.",
            "executive_title": "Founder & President",
            "contact_email": "askmaps@maps.org",
            "target_grant": "PAR-25-274",
            "grant_match_rationale": "Vast infrastructure running rigorous Phase 2 and 3 FDA-regulated clinical trials on mind-body therapies.",
            "grant_title": "Feasibility Clinical Trials of Mind and Body Interventions for NCCIH High Priority Research Topics",
            "funding_ceiling": 225000,
            "deadline": "November 17, 2026"
        },
        {
            "non_profit_name": "AnitaB.org",
            "website": "https://anitab.org",
            "location": "Belmont, CA",
            "executive_name": "Brenda Darden Wilkerson",
            "executive_title": "President & CEO",
            "contact_email": "info@anitab.org",
            "target_grant": "NSF-26-501",
            "grant_match_rationale": "Focuses on diversifying the technological workforce and expanding technical training pathways.",
            "grant_title": "Advanced Technological Education",
            "funding_ceiling": 4000000,
            "deadline": "October 15, 2026"
        },
        {
            "non_profit_name": "Girls Who Code",
            "website": "https://girlswhocode.com",
            "location": "New York, NY",
            "executive_name": "Tarika Barrett, Ph.D.",
            "executive_title": "CEO",
            "contact_email": "info@girlswhocode.com",
            "target_grant": "NSF-26-501",
            "grant_match_rationale": "National footprint in technical training, computing literacy, and high-tech career pipeline programs.",
            "grant_title": "Advanced Technological Education",
            "funding_ceiling": 4000000,
            "deadline": "October 15, 2026"
        },
        {
            "non_profit_name": "Project Lead The Way (PLTW)",
            "website": "https://www.pltw.org",
            "location": "Indianapolis, IN",
            "executive_name": "Dr. David Dimmett",
            "executive_title": "President & CEO",
            "contact_email": "pltw@pltw.org",
            "target_grant": "NSF-26-501",
            "grant_match_rationale": "Premier STEM learning provider with proven capacity to scale technology education nationally.",
            "grant_title": "Advanced Technological Education",
            "funding_ceiling": 4000000,
            "deadline": "October 15, 2026"
        },
        {
            "non_profit_name": "Code.org",
            "website": "https://code.org",
            "location": "Seattle, WA",
            "executive_name": "Hadi Partovi",
            "executive_title": "Founder & CEO",
            "contact_email": "info@code.org",
            "target_grant": "NSF-26-501",
            "grant_match_rationale": "Vast curriculum-building capabilities, scaling technical education across school systems and workforce pipelines.",
            "grant_title": "Advanced Technological Education",
            "funding_ceiling": 4000000,
            "deadline": "October 15, 2026"
        },
        {
            "non_profit_name": "MESA USA",
            "website": "https://mesausa.org",
            "location": "Oakland, CA",
            "executive_name": "Thomas Morrison",
            "executive_title": "Director",
            "contact_email": "info@mesausa.org",
            "target_grant": "NSF-26-501",
            "grant_match_rationale": "Decades of localized experience developing STEM pipelines and academic retention for technological careers.",
            "grant_title": "Advanced Technological Education",
            "funding_ceiling": 4000000,
            "deadline": "October 15, 2026"
        }
    ]

    outreach_queue = []

    for p in prospects:
        name = p["executive_name"]
        title = p["executive_title"]
        org = p["non_profit_name"]
        grant_id = p["target_grant"]
        grant_title = p["grant_title"]
        ceiling = p["funding_ceiling"]
        deadline = p["deadline"]
        rationale = p["grant_match_rationale"]
        email = p["contact_email"]
        
        ceiling_str = f"${ceiling:,}" if ceiling else "Unspecified"
        
        subject = f"Active Funding Opportunity: {ceiling_str} {grant_id} Grant for {org}"
        
        body = (
            f"Hi {name},\n\n"
            f"I was reviewing {org}'s outstanding work, particularly your focus on "
            f"how you {rationale.lower()} In relation to active federal funding cycles, I wanted to "
            f"ensure that this high-value funding opportunity was on your radar:\n\n"
            f"The federal program is: \"{grant_title}\" (Grant ID: {grant_id}). "
            f"The funding ceiling for this call is {ceiling_str}, and it is explicitly open to eligible "
            f"501(c)(3) non-profit organizations. The deadline for proposal submissions is {deadline}.\n\n"
            f"To assist your team in assessing this program quickly, we have mapped out the full eligibility parameters, "
            f"historical match metrics, and direct application links on our live dashboard:\n"
            f"https://dalevirtualcoo-web.github.io/grant-feed/data/index.html\n\n"
            f"We also compile real-time deadline notifications. If you would like to sync active federal cutoffs "
            f"directly with your team's Outlook or Apple calendar, you can subscribe to our free iCal feed:\n"
            f"https://dalevirtualcoo-web.github.io/grant-feed/data/grant_calendar.ics\n\n"
            f"If {org} lacks the direct internal capacity or bandwidth to assemble "
            f"the proposal package before the {deadline} cutoff, our consulting team at Giles Industries "
            f"assembles turnkey, high-scoring application packages on a value-play basis. Let me know if you would like "
            f"to schedule a quick call to discuss proposal development.\n\n"
            f"Best of luck with your funding cycles this season.\n\n"
            f"Best regards,\n\n"
            f"Zac Giles\n"
            f"Managing Director, Giles Industries\n"
            f"bubbagiles@icloud.com"
        )
        
        outreach_queue.append({
            "recipient_email": email,
            "recipient_name": name,
            "recipient_title": title,
            "organization": org,
            "subject": subject,
            "body": body,
            "status": "pending_send"
        })

    output_path = "/data/automation-arbitrage/data/outreach_queue.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(outreach_queue, f, indent=2)
        
    print(f"Successfully generated {len(outreach_queue)} highly-personalized outreach drafts at {output_path}")

if __name__ == "__main__":
    generate_outreach_templates()
