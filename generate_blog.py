import os
import random
import datetime
import time
import re
from google import genai
from google.genai.errors import ServerError

# -*- coding: utf-8 -*-
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing!")

client = genai.Client(api_key=GEMINI_API_KEY)

CORE_TOWNS = [
    "Petawawa",
    "Pembroke and Laurentian Valley",
    "Renfrew, Arnprior, and Carleton Place",
    "Deep River, Chalk River, and Laurentian Hills"
]

OTHER_TOWNS = [
    "Horton, Admaston/Bromley, Greater Madawaska, and Calabogie",
    "McNab/Braeside",
    "Eganville, Bonnechere Valley, and North Algona Wilberforce",
    "Madawaska Valley, Barry's Bay, and Combermere",
    "Killaloe, Hagarty, Richards, and Round Lake"
]

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
    "Preparing Your Home for a Fast Market Sale: Staging & Curb Appeal Tips"
]

COMMUTER_TOPICS = [
    "Commuting from Carleton Place or Arnprior to Ottawa: What to Expect",
    "First-Time Home Buyer Mistakes to Avoid in High-Demand Suburbs",
    "Home Selling Tips for Maximizing Equity in Fast-Moving Markets"
]

RURAL_WATERFRONT_TOPICS = [
    "Septic & Well Inspections: What Buyers Must Know About Rural Ontario Infrastructure",
    "Shoreline Allowances: Understanding Crown Reserves When Buying Waterfront",
    "Cottage as a Primary Residence: Living Year-Round in Recreational Properties"
]

GENERAL_MARKET_TOPICS = [
    "Renfrew County Housing Overview: Inventory and Average Days on Market",
    "Preparing Your Home for a Fast Market Sale in the Ottawa Valley"
]

weighted_town_pool = (CORE_TOWNS * 3) + OTHER_TOWNS
selected_town = random.choice(weighted_town_pool)

if selected_town in ["Petawawa", "Pembroke and Laurentian Valley"]:
    selected_topic = random.choice(MILITARY_HUB_TOPICS)
elif selected_town == "Deep River, Chalk River, and Laurentian Hills":
    selected_topic = random.choice(MILITARY_HUB_TOPICS + RURAL_WATERFRONT_TOPICS)
elif selected_town in ["Renfrew, Arnprior, and Carleton Place", "McNab/Braeside"]:
    selected_topic = random.choice(COMMUTER_TOPICS + GENERAL_MARKET_TOPICS)
else:
    selected_topic = random.choice(RURAL_WATERFRONT_TOPICS + GENERAL_MARKET_TOPICS)

today_str = datetime.date.today().strftime("%B %d, %Y")
slug_date = datetime.date.today().strftime("%Y-%m-%d")

prompt = f"""
You are an expert real estate SEO copywriter for Prakash Solanki, an individual REALTOR® with RE/MAX Pembroke Realty Ltd., Brokerage, serving Pembroke, Petawawa, Deep River, Renfrew, Whitewater Region, and the Ottawa Valley.
Write a concise, punchy, and highly scannable HTML blog post about: "{selected_topic}" specifically tailored for home buyers/sellers in "{selected_town}", Ontario.

Guidelines:
1. Keep the article concise, direct, and easy to read (under 400 words total). Use short paragraphs and bullet points.
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
      time.sleep((attempt + 1) * 15)
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
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link href="[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800;900&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800;900&display=swap)" rel="stylesheet">
    <style>body { font-family: 'Plus Jakarta Sans', sans-serif; }</style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen pt-28 pb-32 px-4 sm:px-6 lg:px-8">

    <header class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200/90 shadow-sm w-full">
        <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-2.5 flex items-center justify-between gap-3 w-full">
            <div class="flex items-center gap-2.5 sm:gap-3 min-w-0">
                <a href="[https://solankihomes.ca](https://solankihomes.ca)" class="flex-shrink-0">
                    <img src="/Prakash_new_pic.PNG" alt="Prakash Solanki REALTOR" class="h-10 w-10 sm:h-12 sm:w-12 rounded-full object-cover border-2 border-red-600 shadow-sm" onerror="this.onerror=null; this.src='Prakash_new_pic.PNG';">
                </a>
                <a href="[https://solankihomes.ca](https://solankihomes.ca)" class="flex flex-col min-w-0 group">
                    <div class="flex items-center gap-1.5 leading-tight truncate">
                        <span class="text-xs sm:text-base font-extrabold tracking-tight text-slate-900 group-hover:text-red-600 transition-colors truncate">Prakash Solanki</span>
                        <span class="text-[9px] sm:text-xs font-black tracking-wider text-red-600 uppercase flex-shrink-0">REALTOR®</span>
                    </div>
                    <span class="text-[9px] sm:text-xs font-black uppercase tracking-wider text-slate-700 block leading-tight mt-0.5 truncate">RE/MAX Pembroke Realty Ltd.</span>
                    <span class="text-[8px] sm:text-[10px] font-bold text-slate-500 block leading-tight truncate">📍 10A Canadian Forces Dr., Petawawa, ON</span>
                </a>
            </div>

            <div class="hidden md:flex items-center justify-center flex-shrink-0 px-2">
                <a href="[https://solankihomes.ca](https://solankihomes.ca)">
                    <img src="/remax_logo.png" alt="RE/MAX Logo" class="h-10 sm:h-12 w-auto object-contain" onerror="this.onerror=null; this.src='remax_logo.png';">
                </a>
            </div>

            <div class="flex items-center flex-shrink-0">
                <a href="tel:16132033313" class="inline-flex items-center gap-1.5 sm:gap-2 bg-red-600 hover:bg-red-700 text-white font-black px-3 py-2 sm:px-4 sm:py-2.5 rounded-xl text-xs sm:text-sm transition shadow-md whitespace-nowrap">
                    <span>(613) 203-3313</span>
                </a>
            </div>
        </div>
    </header>

    <div class="max-w-3xl mx-auto bg-slate-800 p-6 sm:p-10 rounded-2xl border border-slate-700 shadow-2xl mt-2">
        <div class="mb-6 border-b border-slate-700 pb-6">
            <div class="inline-flex items-center gap-2 bg-slate-900/90 border border-red-500/30 px-3.5 py-1.5 rounded-full mb-3">
                <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
                <span class="text-xs sm:text-sm font-extrabold text-white tracking-wide uppercase">Blog — SolankiHomes.ca</span>
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

        <div class="mt-12 p-8 bg-slate-900 rounded-2xl border border-red-500/30 text-center space-y-4 shadow-xl">
            <h3 class="text-2xl sm:text-3xl font-extrabold text-white">Planning a Move to or from TOWN_PLACEHOLDER?</h3>
            <p class="text-sm sm:text-base text-slate-300 max-w-xl mx-auto">Get clarity on your home's current market value or receive immediate notifications when properties hit the MLS in TOWN_PLACEHOLDER and the Ottawa Valley.</p>
            <div class="pt-4 flex flex-col sm:flex-row justify-center gap-4">
                 <a href="[https://seller.solankihomes.ca](https://seller.solankihomes.ca)" target="_blank" rel="noopener noreferrer" class="bg-red-600 hover:bg-red-700 text-white font-bold py-3.5 px-8 rounded-xl text-sm sm:text-base transition shadow-md">Get a Free Home Evaluation</a>
                 <a href="[https://buyer.solankihomes.ca](https://buyer.solankihomes.ca)" target="_blank" rel="noopener noreferrer" class="bg-slate-700 hover:bg-slate-600 text-white font-bold py-3.5 px-8 rounded-xl text-sm sm:text-base transition shadow-md border border-slate-600">Request Custom MLS Alerts</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

tail_html = tail_html.replace("TOWN_PLACEHOLDER", selected_town)
full_page = head_html + article_html + tail_html

clean_topic = re.sub(r'[^a-zA-Z0-9\s-]', '', selected_topic.lower())
clean_town = re.sub(r'[^a-zA-Z0-9\s-]', '', selected_town.lower())
slug = re.sub(r'[\s_]+', '-', f"{clean_topic} in {clean_town}".strip())
filename = f"{slug_date}-{slug}.html"

output_dir = "blog"
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, filename)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(full_page)

# Automatically update index.html with the new post
index_path = "index.html"
if os.path.exists(index_path):
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    # 1. Update default iframe src to the new article
    iframe_pattern = r'id="sh-frame"\s+src="[^"]*"'
    new_iframe_src = f'id="sh-frame" src="/blog/{filename}"'
    if re.search(iframe_pattern, index_content):
        index_content = re.sub(iframe_pattern, new_iframe_src, index_content)

    # 2. Insert new post into date-sorted blog list
    new_link_html = f'''          <a href="#" onclick="loadArticle('/blog/{filename}', this); return false;" class="sh-post-item block p-3 rounded-xl bg-slate-800/80 hover:bg-slate-700 border border-slate-700/80 transition group">
            <span class="text-[10px] font-extrabold text-remax-gold block mb-1">{today_str}</span>
            <span class="text-xs font-bold text-white group-hover:text-sky-400 transition leading-snug block">{selected_topic} in {selected_town}, ON</span>
          </a>'''

    start_marker = "<!-- BLOG_LIST_START -->"
    end_marker = "<!-- BLOG_LIST_END -->"
    
    if start_marker in index_content and end_marker in index_content:
        parts = index_content.split(start_marker)
        header_part = parts[0]
        rest = parts[1].split(end_marker)
        list_content = rest[0]
        footer_part = rest[1]

        updated_list_content = list_content.replace('<div class="space-y-2">', f'<div class="space-y-2">\n{new_link_html}')
        index_content = header_part + start_marker + updated_list_content + end_marker + footer_part

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    print("Successfully updated index.html with the new blog post!")
