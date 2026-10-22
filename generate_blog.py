import os
import random
import datetime
import time
import re
import requests
# -*- coding: utf-8 -*-
# Ensure API Key is available
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing!")

# Core / Primary Markets (Weighted higher for frequent posting)
CORE_TOWNS = [
    "Petawawa",
    "Pembroke and Laurentian Valley",
    "Renfrew, Arnprior, and Carleton Place",
    "Deep River, Chalk River, and Laurentian Hills"
]

# Secondary Regional Clusters
OTHER_TOWNS = [
    "Horton, Admaston/Bromley, Greater Madawaska, and Calabogie",
    "McNab/Braeside",
    "Eganville, Bonnechere Valley, and North Algona Wilberforce",
    "Madawaska Valley, Barry's Bay, and Combermere",
    "Killaloe, Hagarty, Richards, and Round Lake"
]

# --- Topic Pools by Regional Tracks ---
MILITARY_HUB_TOPICS = [
    "Garrison Petawawa Military Relocation & House Hunting Trip (HHT) Guide",
    "IRP & SIRVA Relocation Breakdown: Navigating Canadian Forces Relocations",
    "Renting vs. Buying: Should Military Families Buy or Rent in Petawawa?",
    "Selling on a Posting: How to Quickly List and Sell Your Petawawa Home",
    "Moving for CNL: Housing Options in Deep River, Chalk River, and Laurentian Hills",
    "Living Off-Base: The Best Neighborhoods in Petawawa for DND Civilian Contractors",
    "Pembroke Regional Hospital Relocation: Where Healthcare Professionals Buy Homes",
    "Investing in the Valley: Capitalizing on the Petawawa & Pembroke Rental Market",
    "First-Time Home Buyer Mistakes to Avoid in Petawawa & Pembroke",
    "Home Selling Tips for Maximizing Equity in the Local Housing Market",
    "Family-Friendly Neighborhoods: Finding the Right Property in Pembroke & Petawawa",
    "Preparing Your Home for a Fast Market Sale: Staging & Curb Appeal Tips",
    "Downsizing or Upgrading: Navigating Property Transitions Locally",
    "Maintenance-Free Living: The Rise of Modern Townhomes and Condos in Pembroke"
]

COMMUTER_TOPICS = [
    "Commuting from Carleton Place or Arnprior to Ottawa: What to Expect",
    "First-Time Home Buyer Mistakes to Avoid in High-Demand Suburbs",
    "Home Selling Tips for Maximizing Equity in Fast-Moving Markets",
    "Downsizing Locally: Transitioning from Rural Property to an Arnprior Townhome",
    "Arnprior & Carleton Place Market Update: Suburban Demand vs. Ottawa Pricing"
]

RURAL_WATERFRONT_TOPICS = [
    "Septic & Well Inspections: What Buyers Must Know About Rural Ontario Infrastructure",
    "Shoreline Allowances: Understanding Crown Reserves When Buying Waterfront",
    "Cottage as a Primary Residence: Living Year-Round in Recreational Properties",
    "Ottawa Valley Acreage & Waterfront Report: Pricing Trends for Rural Properties"
]

GENERAL_MARKET_TOPICS = [
    "Renfrew County Housing Overview: Inventory and Average Days on Market",
    "Preparing Your Home for a Fast Market Sale in the Ottawa Valley",
    "Understanding Property Values and Local Market Trends"
]

# Create a weighted pool: Core towns appear 3x more often than other towns
weighted_town_pool = (CORE_TOWNS * 3) + OTHER_TOWNS

# Select a town for this run
selected_town = random.choice(weighted_town_pool)
print(f"Selected town for this post: {selected_town}")

# Intelligent Topic Routing
if selected_town in ["Petawawa", "Pembroke and Laurentian Valley"]:
    selected_topic = random.choice(MILITARY_HUB_TOPICS)
elif selected_town == "Deep River, Chalk River, and Laurentian Hills":
    selected_topic = random.choice(MILITARY_HUB_TOPICS + RURAL_WATERFRONT_TOPICS)
elif selected_town in ["Renfrew, Arnprior, and Carleton Place", "McNab/Braeside"]:
    selected_topic = random.choice(COMMUTER_TOPICS + GENERAL_MARKET_TOPICS)
else:
    selected_topic = random.choice(RURAL_WATERFRONT_TOPICS + GENERAL_MARKET_TOPICS)

print(f"Selected topic: {selected_topic}")

today_str = datetime.date.today().strftime("%B %d, %Y")
slug_date = datetime.date.today().strftime("%Y-%m-%d")

prompt = f"""
You are an expert real estate SEO copywriter for Prakash Solanki, REALTOR® at RE/MAX Pembroke Realty Ltd., Brokerage in Petawawa, Ontario.

Write a complete, highly engaging HTML blog post on the topic: "{selected_topic} in {selected_town}, Ontario".

Strict Guidelines:
1. Return ONLY pure HTML content inside an <article> tag. Do not include markdown backticks like ```html.
2. Naturally mention Prakash Solanki, REALTOR®, RE/MAX Pembroke Realty Ltd., Brokerage, and phone number (613) 203-3313.
3. Address specific buyer and seller intent for {selected_town} and the Ottawa Valley region.
4. Structurally use <h2>, <h3>, <p>, <ul>, and <li> tags with clean styling class names like Tailwind CSS.
5. 5. Include a prominent call-to-action encouraging readers to get a Free Home Evaluation at https://seller.solankihomes.ca or request custom MLS alerts at https://buyer.solankihomes.ca.


# Clean API Endpoint (No markdown brackets)
base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key="
url = base_url + GEMINI_API_KEY
payload = {"contents": [{"parts": [{"text": prompt}]}]}



# Automatic Retry Loop for handling temporary 503 errors
max_retries = 3
article_html = ""
data = {}

for attempt in range(max_retries):
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        # Safe response payload schema parsing mapping
        article_html = data["candidates"][0]["content"]["parts"][0]["text"]
        article_html = article_html.replace("```html", "").replace("```", "").strip()
        break  # Success! Exit retry loop
    except Exception as e:
        if attempt < max_retries - 1:
            print(f"API busy or error encountered ({e}). Retrying in 15 seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(15)
        else:
            print("API Error Response:", data)
            raise e

# Build full web page template wrapper with static links
full_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{selected_topic} in {selected_town}, ON | Prakash Solanki REALTOR</title>
    <meta name="description" content="Expert insights on {selected_topic} in {selected_town}, Ontario with Prakash Solanki, RE/MAX Pembroke Realty Ltd. Brokerage.">
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link href="[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap)" rel="stylesheet">
    <style>body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}</style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto bg-slate-800 p-6 sm:p-10 rounded-2xl border border-slate-700 shadow-2xl">
        <div class="mb-8 border-b border-slate-700 pb-6">
            <a href="https://solankihomes.ca" class="text-xs font-bold uppercase text-red-500 tracking-wider hover:underline">&larr; Back to SolankiHomes.ca</a>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-white mt-3 leading-tight">{selected_topic} in {selected_town}, ON</h1>
            <p class="text-xs text-slate-400 mt-2">Published by Prakash Solanki, REALTOR on {today_str}</p>
        </div>
        <div class="prose prose-invert max-w-none text-slate-300 leading-relaxed space-y-4">
            {article_html}
        </div>
        <div class="mt-12 p-6 bg-slate-900 rounded-xl border border-red-500/30 text-center space-y-3">
            <h3 class="text-xl font-bold text-white">Planning a Move in {selected_town} or the Ottawa Valley?</h3>
            <p class="text-sm text-slate-300">Contact Prakash Solanki today for a free home evaluation or personalized MLS property alerts.</p>
            <div class="pt-2 flex justify-center gap-4">
                 <a href="https://seller.solankihomes.ca" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2.5 px-5 rounded-lg text-sm transition shadow-md">Free Home Evaluation</a>
                 <a href="https://buyer.solankihomes.ca" class="bg-slate-700 hover:bg-slate-600 text-white font-bold py-2.5 px-5 rounded-lg text-sm transition shadow-md">Custom MLS Alerts</a>
            </div>
        </div>
    </div>
</body>
</html>"""

# --- File System Local Disk Output ---
clean_topic = re.sub(r'[^a-zA-Z0-9\s-]', '', selected_topic.lower())
clean_town = re.sub(r'[^a-zA-Z0-9\s-]', '', selected_town.lower())
combined_text = f"{clean_topic} in {clean_town}"
slug = re.sub(r'[\s_]+', '-', combined_text.strip())
filename = f"{slug_date}-{slug}.html"

output_dir = "blog"
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, filename)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(full_page)

print(f"File successfully compiled and written to disk at: {file_path}")
