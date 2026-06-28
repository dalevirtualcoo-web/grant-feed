import json
import os
from datetime import datetime

def build_portal():
    leads_path = "/data/automation-arbitrage/data/leads_master.json"
    stripe_config_path = "/data/automation-arbitrage/data/stripe_config.json"
    output_path = "/data/automation-arbitrage/data/index.html"
    
    if not os.path.exists(leads_path):
        print(f"Error: Leads database not found at {leads_path}")
        return
        
    try:
        with open(leads_path, "r", encoding="utf-8") as f:
            leads = json.load(f)
    except Exception as e:
        print(f"Error reading leads: {e}")
        return

    # Load Stripe Payment Link
    stripe_link = "#STRIPE_CHECKOUT_URL"
    if os.path.exists(stripe_config_path):
        try:
            with open(stripe_config_path, "r", encoding="utf-8") as f:
                stripe_config = json.load(f)
            stripe_link = stripe_config.get("payment_url", "#STRIPE_CHECKOUT_URL")
            print(f"Stripe Payment Link loaded: {stripe_link}")
        except Exception as e:
            print(f"Warning: Could not read stripe_config.json: {e}")

    print(f"Loaded {len(leads)} leads from {leads_path}")

    # Build the HTML content
    html = []
    
    # 1. Header and setup
    html.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Grant Intelligence Portal</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts Inter & Playfair Display -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        serif: ['Playfair Display', 'serif'],
                    }
                }
            }
        }
    </script>
    <style>
        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(229, 231, 235, 0.5);
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-900 font-sans min-h-screen flex flex-col">

    <!-- Navigation Header -->
    <header class="glass-card sticky top-0 z-40 border-b border-slate-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-200">
                    <span class="text-white text-xl font-bold font-serif">G</span>
                </div>
                <div>
                    <span class="font-bold tracking-tight text-slate-900 block text-lg font-serif">Giles Industries</span>
                    <span class="text-xs text-indigo-600 font-medium tracking-widest uppercase">Grant Intelligence Feed</span>
                </div>
            </div>
            <div class="flex items-center gap-4">
                <a href="#pricing" class="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 transition rounded-xl shadow-md shadow-indigo-100">
                    Upgrade to Premium
                </a>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="py-12 bg-white border-b border-slate-100">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <span class="px-3 py-1 text-xs font-semibold text-indigo-700 bg-indigo-50 rounded-full inline-block mb-4 tracking-wider uppercase">Live B2B Curation Engine</span>
            <h1 class="text-4xl sm:text-5xl font-bold text-slate-950 font-serif leading-tight mb-4">
                Automated Non-Profit <br class="hidden sm:inline">Grant Intelligence Feed
            </h1>
            <p class="text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
                Skip searching federal directories. Our autonomous pipeline ingests, validates, structures, and alerts you to newly active high-value federal grant programs the second they are published.
            </p>
        </div>
    </section>

    <!-- Main Content Layout -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <!-- Left Side Feed Columns -->
            <div class="lg:col-span-2 space-y-12">
""")

    # --- 2. Free Public Insights Section (First 2 leads) ---
    html.append("""
                <!-- Free Public Insights -->
                <div>
                    <div class="flex items-center justify-between mb-6">
                        <h2 class="text-2xl font-bold text-slate-950 font-serif">Free Public Insights</h2>
                        <span class="px-2.5 py-1 text-xs font-semibold text-emerald-700 bg-emerald-50 rounded-full border border-emerald-100 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> Live Streams Active
                        </span>
                    </div>
                    <div class="grid grid-cols-1 gap-6">
    """)

    free_leads = leads[:2]
    for lead in free_leads:
        title = lead.get("opportunity_title", "No Title Specified")
        grant_id = lead.get("grant_id", "N/A")
        agency = lead.get("agency", "Unknown Agency")
        ceiling = lead.get("funding_ceiling")
        close_date = lead.get("close_date", "Unspecified")
        url = lead.get("source_url", "#")
        
        # Safely format funding ceiling
        ceiling_str = f"${ceiling:,}" if isinstance(ceiling, (int, float)) else "Funding Level Unspecified"
        
        html.append(f"""
                        <!-- Free Card -->
                        <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition duration-200 relative overflow-hidden group">
                            <div class="absolute top-0 left-0 w-1.5 h-full bg-indigo-500"></div>
                            <div class="flex justify-between items-start gap-4 mb-3">
                                <div>
                                    <span class="px-2.5 py-0.5 text-xs font-bold text-indigo-700 bg-indigo-50 rounded-md uppercase tracking-wider">{grant_id}</span>
                                    <span class="ml-2 text-xs text-slate-500 font-medium">{agency}</span>
                                </div>
                                <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Public Access</span>
                            </div>
                            <h3 class="text-lg font-bold text-slate-950 leading-snug group-hover:text-indigo-600 transition mb-3">{title}</h3>
                            <div class="grid grid-cols-2 gap-4 border-t border-slate-100 pt-3 text-sm">
                                <div>
                                    <span class="text-slate-400 block text-xs uppercase tracking-wider font-semibold">Funding Ceiling</span>
                                    <span class="font-bold text-slate-800 text-base">{ceiling_str}</span>
                                </div>
                                <div>
                                    <span class="text-slate-400 block text-xs uppercase tracking-wider font-semibold">Close Date</span>
                                    <span class="font-medium text-slate-700">{close_date}</span>
                                </div>
                            </div>
                            <div class="mt-4 flex items-center justify-end">
                                <a target="_blank" href="{url}" class="text-sm font-semibold text-indigo-600 hover:text-indigo-700 flex items-center gap-1 group-hover:underline">
                                    Apply Directly <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                                </a>
                            </div>
                        </div>
        """)

    html.append("""
                    </div>
                </div>
    """)

    # --- 3. Premium Intelligence Feed (Index 2 and beyond) ---
    html.append("""
                <!-- Premium Locked Feed -->
                <div class="relative">
                    <div class="flex items-center justify-between mb-6">
                        <h2 class="text-2xl font-bold text-slate-950 font-serif">Premium Intelligence Feed</h2>
                        <span class="px-2.5 py-1 text-xs font-semibold text-slate-600 bg-slate-100 rounded-full border border-slate-200">
                            🔒 Locked Opportunities
                        </span>
                    </div>
                    
                    <!-- Blurred Premium Feed Wrapper -->
                    <div class="grid grid-cols-1 gap-6 select-none pointer-events-none mb-24">
    """)

    premium_leads = leads[2:]
    for lead in premium_leads:
        agency = lead.get("agency", "Unknown Agency")
        grant_id = lead.get("grant_id", "N/A")
        close_date = lead.get("close_date", "Unspecified")
        ceiling = lead.get("funding_ceiling")
        
        # Safely format funding ceiling
        ceiling_str = f"${ceiling:,}" if isinstance(ceiling, (int, float)) else "Funding Level Unspecified"
        
        html.append(f"""
                        <!-- Locked Card -->
                        <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm relative overflow-hidden">
                            <div class="absolute top-0 left-0 w-1.5 h-full bg-slate-300"></div>
                            <div class="flex justify-between items-start gap-4 mb-3">
                                <div>
                                    <span class="px-2.5 py-0.5 text-xs font-bold text-slate-400 bg-slate-100 rounded-md uppercase tracking-wider">{grant_id}</span>
                                    <span class="ml-2 text-xs text-slate-400 font-medium">{agency}</span>
                                </div>
                            </div>
                            <h3 class="text-lg font-bold text-slate-400 leading-snug mb-3">🔒 [Premium Locked Grant Opportunity]</h3>
                            <div class="grid grid-cols-2 gap-4 border-t border-slate-100 pt-3 text-sm blur-sm select-none">
                                <div>
                                    <span class="text-slate-400 block text-xs uppercase tracking-wider font-semibold">Funding Ceiling</span>
                                    <span class="font-bold text-slate-800 text-base">{ceiling_str}</span>
                                </div>
                                <div>
                                    <span class="text-slate-400 block text-xs uppercase tracking-wider font-semibold">Close Date</span>
                                    <span class="font-medium text-slate-700">{close_date}</span>
                                </div>
                            </div>
                            <div class="mt-4 flex items-center justify-end blur-sm select-none">
                                <span class="text-sm font-semibold text-indigo-600 flex items-center gap-1">
                                    Apply Directly <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                                </span>
                            </div>
                        </div>
        """)

    # Adding the paywall CTA overlay with dynamic Stripe Link
    html.append(f"""
                    </div>

                    <!-- Beautiful Paywall Overlay -->
                    <div class="absolute inset-0 flex items-end justify-center bg-gradient-to-t from-slate-50 via-slate-50/95 to-transparent pb-12">
                        <div id="pricing" class="w-full max-w-md bg-white border border-slate-200 rounded-3xl p-8 shadow-2xl text-center relative z-10 glass-card">
                            <span class="px-3 py-1 text-xs font-semibold text-indigo-700 bg-indigo-50 rounded-full inline-block mb-4 tracking-wider uppercase">Institutional Access</span>
                            <h3 class="text-2xl font-bold text-slate-950 font-serif mb-2">Unlock All Active Grant Streams</h3>
                            <p class="text-sm text-slate-600 mb-6 leading-relaxed">
                                Get immediate access to the full premium list, real-time Slack/Telegram notifications, and automatic weekly downloadable digests formatted for your executive team.
                            </p>
                            <div class="mb-6">
                                <span class="text-4xl font-extrabold text-slate-950">$29</span>
                                <span class="text-slate-500 font-medium"> / month</span>
                            </div>
                            <a href="{stripe_link}" class="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl block transition duration-200 shadow-lg shadow-indigo-200 hover:shadow-xl">
                                Unlock Unlimited Real-Time Grant Streams
                            </a>
                            <p class="text-xs text-slate-400 mt-3 font-medium">Cancel anytime. 7-day money-back guarantee.</p>
                        </div>
                    </div>

                </div>
            </div>

            <!-- Right Sidebar Columns: Pricing & Insights -->
            <div class="space-y-8">
                
                <!-- Business Stats Widget -->
                <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                    <h3 class="font-bold text-slate-950 text-lg font-serif mb-4">Intelligence Stats</h3>
                    <div class="space-y-4">
                        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                            <span class="text-slate-500 text-sm font-medium">Total Open Grants</span>
                            <span class="font-bold text-slate-900 text-sm">1,343 Active</span>
                        </div>
                        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                            <span class="text-slate-500 text-sm font-medium">Last Feed Sync</span>
                            <span class="font-bold text-emerald-600 text-sm flex items-center gap-1">
                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> Just Now
                            </span>
                        </div>
                        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                            <span class="text-slate-500 text-sm font-medium">Primary Focus</span>
                            <span class="font-bold text-indigo-600 text-sm">501(c)(3) Nonprofits</span>
                        </div>
                        <div class="flex items-center justify-between">
                            <span class="text-slate-500 text-sm font-medium">Source Accuracy</span>
                            <span class="font-bold text-slate-900 text-sm">Official API Only</span>
                        </div>
                    </div>
                </div>

                <!-- Strategic Promotion Widget -->
                <div class="bg-gradient-to-br from-indigo-900 to-indigo-950 text-white rounded-2xl p-6 shadow-sm border border-indigo-950 relative overflow-hidden">
                    <div class="absolute -right-12 -bottom-12 w-32 h-32 bg-indigo-800 rounded-full opacity-30 blur-2xl"></div>
                    <span class="text-xs font-semibold text-indigo-300 tracking-wider uppercase block mb-1">Giles Consulting Group</span>
                    <h3 class="font-bold text-xl font-serif mb-2 text-white">Need Custom Grant Writing & Proposal Assembly?</h3>
                    <p class="text-sm text-indigo-100 leading-relaxed mb-4 opacity-90">
                        Our virtual experts assemble bulletproof application packages for qualified non-profits to secure 7-figure federal funding.
                    </p>
                    <a href="mailto:bubbagiles@icloud.com" class="text-sm font-bold text-white hover:text-indigo-200 underline flex items-center gap-1">
                        Book a Consultation <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                    </a>
                </div>

            </div>

        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 mt-16 py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-slate-500">
            <p>&copy; 2026 Giles Industries. Powered by autonomous Hermes-Agent pipelines. All rights reserved.</p>
        </div>
    </footer>

</body>
</html>
""")

    # Ensure data directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
        
    print(f"Successfully compiled storefront portal and saved to {output_path}")

if __name__ == "__main__":
    build_portal()
