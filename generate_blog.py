import os
import random
import datetime
import time
import re
import requests
from google import genai
from google.genai.errors import ServerError

# -*- coding: utf-8 -*-
# Ensure API Key is available
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing!")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)
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
You are an expert real estate SEO copywriter for Prakash Solanki, an individual REALTOR® with RE/MAX Pembroke Realty Ltd., Brokerage, serving Pembroke, Petawawa, Deep River, Renfrew, Whitewater Region, and the Ottawa Valley.
Write a complete, highly engaging HTML blog post about: "{selected_topic}" specifically tailored for home buyers/sellers in "{selected_town}", Ontario.

Guidelines:
1. Write in a professional, authoritative, yet warm and approachable tone.
2. Incorporate local geographic references relevant to {selected_town} and the Ottawa Valley.
3. Include practical, actionable real estate advice.
4. Structurally use <h2>, <h3>, <p>, <ul>, and <li> tags with clean styling class names like Tailwind CSS.
5. Include a prominent call-to-action encouraging readers to get a Free Home Evaluation at solankihomes.ca or request custom MLS alerts.
Return ONLY valid HTML content for the article body inside the <div>. Do not include markdown code blocks like ```html.
"""


max_retries = 3
for attempt in range(max_retries):
  try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )
    break
  except ServerError as e:
    if e.code == 503 and attempt < max_retries - 1:
      wait_time = (attempt + 1) * 15
      print(f"503 High Demand. Retrying in {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
      time.sleep(wait_time)
    else:
      raise e

article_html = response.text.strip()

if article_html.startswith("```html"):
    article_html = article_html[7:]
if article_html.endswith("```"):
    article_html = article_html[:-3]
article_html = article_html.strip()

head_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TOPIC_PLACEHOLDER in TOWN_PLACEHOLDER, ON | Prakash Solanki REALTOR</title>
    <meta name="description" content="Expert insights on TOPIC_PLACEHOLDER in TOWN_PLACEHOLDER, Ontario with Prakash Solanki, RE/MAX Pembroke Realty Ltd. Brokerage.">
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link href="[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap)" rel="stylesheet">
    <style>body { font-family: 'Plus Jakarta Sans', sans-serif; }</style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto bg-slate-800 p-6 sm:p-10 rounded-2xl border border-slate-700 shadow-2xl">
        <div class="mb-8 border-b border-slate-700 pb-6">
            
            <h1 class="text-3xl sm:text-4xl font-extrabold text-white mt-3 leading-tight">TOPIC_PLACEHOLDER in TOWN_PLACEHOLDER, ON</h1>
            <p class="text-xs text-slate-400 mt-2">Published by Prakash Solanki, REALTOR on DATE_PLACEHOLDER</p>
        </div>
        <div class="prose prose-invert max-w-none text-slate-300 leading-relaxed space-y-4">
"""

head_html = head_html.replace("TOPIC_PLACEHOLDER", selected_topic)
head_html = head_html.replace("TOWN_PLACEHOLDER", selected_town)
head_html = head_html.replace("DATE_PLACEHOLDER", today_str)

tail_html = """
        </div>
        <div class="mt-12 p-6 bg-slate-900 rounded-xl border border-red-500/30 text-center space-y-3">
            <h3 class="text-xl font-bold text-white">Planning a Move in TOWN_PLACEHOLDER or the Ottawa Valley?</h3>
            <p class="text-sm text-slate-300">Contact Prakash Solanki today for a free home evaluation or personalized MLS property alerts.</p>
            <div class="pt-2 flex justify-center gap-4">
                 <a href="[https://seller.solankihomes.ca](https://seller.solankihomes.ca)" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2.5 px-5 rounded-lg text-sm transition shadow-md">Free Home Evaluation</a>
                 <a href="[https://buyer.solankihomes.ca](https://buyer.solankihomes.ca)" class="bg-slate-700 hover:bg-slate-600 text-white font-bold py-2.5 px-5 rounded-lg text-sm transition shadow-md">Custom MLS Alerts</a>
            </div>
        </div>
    </div>

<!-- Sticky Bottom CTA Bar -->
    <div class="fixed bottom-0 left-0 right-0 bg-slate-900/95 backdrop-blur-md border-t border-slate-700 py-2.5 px-4 z-50 shadow-2xl">
      <div class="max-w-3xl mx-auto flex items-center justify-between gap-3">
        <div class="hidden sm:block">
          <p class="text-xs sm:text-sm font-semibold text-slate-200">
            Planning a move in TOWN_PLACEHOLDER?
          </p>
          <p class="text-[10px] text-slate-400 uppercase tracking-wider font-medium">
            100% Free & No Obligation
          </p>
        </div>
        <div class="flex items-center gap-2 w-full sm:w-auto justify-center">
          <a href="https://seller.solankihomes.ca" target="_blank" rel="noopener noreferrer" class="flex-1 sm:flex-none text-center px-4 py-1.5 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg shadow transition leading-tight">
            <span class="block text-xs sm:text-sm">Free Evaluation</span>
            <span class="block text-[10px] sm:text-xs font-normal opacity-90">Sell High</span>
          </a>
          <a href="https://buyer.solankihomes.ca" target="_blank" rel="noopener noreferrer" class="flex-1 sm:flex-none text-center px-4 py-1.5 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-lg border border-slate-600 transition leading-tight">
            <span class="block text-xs sm:text-sm">Buy Smart</span>
            <span class="block text-[10px] sm:text-xs font-normal opacity-90">Free & No-Obligation</span>
          </a>
        </div>
      </div>
    </div>


</body>
</html>
"""

tail_html = tail_html.replace("TOWN_PLACEHOLDER", selected_town)

full_page = head_html + article_html + tail_html

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
