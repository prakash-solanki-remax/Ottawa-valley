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
Write a concise, punchy, and highly scannable HTML blog post about: "{selected_topic}" specifically tailored for home buyers/sellers in "{selected_town}", Ontario.

Guidelines:
1. Keep the article concise, direct, and easy to read (under 400 words total). Use short paragraphs and bullet points so it is not too long.
2. Incorporate local geographic references relevant to {selected_town} and the Ottawa Valley.
3. Structurally use <h2>, <h3>, <p>, <ul>, and <li> tags.
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
    <title>TOPIC_PLACEHOLDER in TOWN_PLACEHOLDER, ON | Blog — SolankiHomes.ca | Prakash Solanki REALTOR®</title>
    <meta name="description" content="Expert insights on TOPIC_PLACEHOLDER in TOWN_PLACEHOLDER, Ontario with Prakash Solanki, RE/MAX Pembroke Realty Ltd. Brokerage.">
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link href="[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800;900&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800;900&display=swap)" rel="stylesheet">
    <style>body { font-family: 'Plus Jakarta Sans', sans-serif; }</style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen pt-28 pb-32 px-4 sm:px-6 lg:px-8">

    <!-- STICKY NAVIGATION HEADER WITH PROFILE PICTURE, DESKTOP-ONLY RE/MAX LOGO & PHONE -->
    <header class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200/90 shadow-sm w-full">
        <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-2.5 flex items-center justify-between gap-3 w-full">
            
            <!-- LEFT: Profile Photo & Branding -->
            <div class="flex items-center gap-2.5 sm:gap-3 min-w-0">
                <a href="[https://solankihomes.ca](https://solankihomes.ca)" class="flex-shrink-0">
                    <img src="/Prakash_new_pic.PNG" alt="Prakash Solanki REALTOR" class="h-10 w-10 sm:h-12 sm:w-12 rounded-full object-cover border-2 border-red-600 shadow-sm" onerror="this.onerror=null; this.src='Prakash_new_pic.PNG';">
                </a>
                <a href="[https://solankihomes.ca](https://solankihomes.ca)" class="flex flex-col min-w-0 group">
                    <div class="flex items-center gap-1.5 leading-tight truncate">
                        <span class="text-xs sm:text-base font-extrabold tracking-tight text-slate-900 group-hover:text-red-600 transition-colors truncate">
                            Prakash Solanki
                        </span>
                        <span class="text-[9px] sm:text-xs font-black tracking-wider text-red-600 uppercase flex-shrink-0">
                            REALTOR®
                        </span>
                    </div>
                    <span class="text-[9px] sm:text-xs font-black uppercase tracking-wider text-slate-700 block leading-tight mt-0.5 truncate">
                        RE/MAX Pembroke Realty Ltd.
                    </span>
                    <span class="text-[8px] sm:text-[10px] font-bold text-slate-500 block leading-tight truncate">
                        📍 10A Canadian Forces Dr., Petawawa, ON
                    </span>
                </a>
            </div>

            <!-- CENTER: RE/MAX Logo (DESKTOP ONLY) -->
            <div class="hidden md:flex items-center justify-center flex-shrink-0 px-2">
                <a href="[https://solankihomes.ca](https://solankihomes.ca)">
                    <img src="/remax_logo.png" alt="RE/MAX Logo" class="h-10 sm:h-12 w-auto object-contain" onerror="this.onerror=null; this.src='remax_logo.png';">
                </a>
            </div>

            <!-- RIGHT: Call Button -->
            <div class="flex items-center flex-shrink-0">
                <a href="tel:16132033313" class="inline-flex items-center gap-1.5 sm:gap-2 bg-red-600 hover:bg-red-700 text-white font-black px-3 py-2 sm:px-4 sm:py-2.5 rounded-xl text-xs sm:text-sm transition shadow-md whitespace-nowrap">
                    <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-white flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/></svg>
                    <span>(613) 203-3313</span>
                </a>
            </div>
        </div>
    </header>

    <div class="max-w-3xl mx-auto bg-slate-800 p-6 sm:p-10 rounded-2xl border border-slate-700 shadow-2xl mt-2">
        
        <!-- PROMINENT BLOG BRANDING HEADER -->
        <div class="mb-6 border-b border-slate-700 pb-6">
            <div class="inline-flex items-center gap-2 bg-slate-900/90 border border-red-500/30 px-3.5 py-1.5 rounded-full mb-3">
                <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
                <span class="text-xs sm:text-sm font-extrabold text-white tracking-wide uppercase">
                    Blog — SolankiHomes.ca
                </span>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-white mt-1 leading-tight">TOPIC_PLACEHOLDER in TOWN_PLACEHOLDER, ON</h1>
            <p class="text-xs text-slate-400 mt-2.5">Published by Prakash Solanki, REALTOR® on DATE_PLACEHOLDER</p>
        </div>
        
        <div class="prose prose-invert max-w-none text-slate-300 leading-relaxed space-y-4">
"""

head_html = head_html.replace("TOPIC_PLACEHOLDER", selected_topic)
head_html = head_html.replace("TOWN_PLACEHOLDER", selected_town)
head_html = head_html.replace("DATE_PLACEHOLDER", today_str)

tail_html = """
        </div>

        <!-- BOTTOM CONVERSION BOX (MATCHING LANDING PAGE BUTTONS) -->
        <div class="mt-12 p-8 bg-slate-900 rounded-2xl border border-red-500/30 text-center space-y-4 shadow-xl">
            <h3 class="text-2xl sm:text-3xl font-extrabold text-white">Planning a Move to or from TOWN_PLACEHOLDER?</h3>
            <p class="text-sm sm:text-base text-slate-300 max-w-xl mx-auto">Get clarity on your home's current market value or receive immediate notifications when properties hit the MLS in TOWN_PLACEHOLDER and the Ottawa Valley.</p>
            <div class="pt-4 flex flex-col sm:flex-row justify-center gap-4">
                 <a href="[https://seller.solankihomes.ca](https://seller.solankihomes.ca)" target="_blank" rel="noopener noreferrer" class="bg-red-600 hover:bg-red-700 text-white font-bold py-3.5 px-8 rounded-xl text-sm sm:text-base transition shadow-md">Get a Free Home Evaluation</a>
                 <a href="[https://buyer.solankihomes.ca](https://buyer.solankihomes.ca)" target="_blank" rel="noopener noreferrer" class="bg-slate-700 hover:bg-slate-600 text-white font-bold py-3.5 px-8 rounded-xl text-sm sm:text-base transition shadow-md border border-slate-600">Request Custom MLS Alerts</a>
            </div>
            <div class="pt-2 text-xs text-slate-400 font-medium">
                Prakash Solanki, REALTOR® | RE/MAX Pembroke Realty Ltd., Brokerage<br>
                Dedicated service throughout TOWN_PLACEHOLDER and across the Ottawa Valley.
            </div>
        </div>
    </div>

    <!-- STICKY BOTTOM MOBILE CTA BAR -->
    <div class="fixed bottom-2 sm:bottom-0 left-0 right-0 bg-slate-900/95 backdrop-blur-md border-t border-slate-700 py-3 px-4 z-50 shadow-[0_-8px_20px_rgba(0,0,0,0.4)]">
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
          <a href="[https://seller.solankihomes.ca](https://seller.solankihomes.ca)" target="_blank" rel="noopener noreferrer" class="flex-1 sm:flex-none text-center px-4 py-2.5 bg-red-600 hover:bg-red-700 text-white font-bold text-xs sm:text-sm rounded-lg shadow transition">
            Get Free Evaluation
          </a>
          <a href="[https://buyer.solankihomes.ca](https://buyer.solankihomes.ca)" target="_blank" rel="noopener noreferrer" class="flex-1 sm:flex-none text-center px-4 py-2.5 bg-slate-700 hover:bg-slate-600 text-white font-semibold text-xs sm:text-sm rounded-lg border border-slate-600 transition">
            Request MLS Alerts
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
