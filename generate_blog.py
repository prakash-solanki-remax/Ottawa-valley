import os
import random
import datetime
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing!")

TOWNS = [
    # Core Municipalities & Primary Hubs
    "Pembroke", "Petawawa", "Deep River", "Laurentian Hills", "Laurentian Valley", 
    "Renfrew", "Arnprior", "Whitewater Region", "Eganville",
    
    # Townships & Rural Districts
    "Admaston/Bromley", "Greater Madawaska", "Westmeath", "Calabogie", "Horton", 
    "Barry's Bay", "McNab/Braeside", "Bonnechere Valley", "North Algona Wilberforce", 
    "Madawaska Valley", "Killaloe, Hagarty and Richards",
    
    # Specific Communities & Regional Areas
    "Combermere", "Killaloe", "Round Lake", "Ottawa Valley"
]
TOPICS = [
    "Home Selling Tips to Maximize Equity",
    "First-Time Home Buyer Mistakes to Avoid",
    "Garrison Petawawa Military Relocation & House Hunting Trip (HHT) Guide",
    "Understanding Property Values and Local Market Trends",
    "Preparing Your Home for a Fast Market Sale",
    "Waterfront Property Buying Checklist",
    "Closing Costs and Financial Steps for Buying a Home in Ontario"
]

selected_town = random.choice(TOWNS)
selected_topic = random.choice(TOPICS)
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
5. Include a prominent call-to-action encouraging readers to get a Free Home Evaluation at [https://seller.solankihomes.ca](https://seller.solankihomes.ca) or request custom MLS alerts at [https://buyer.solankihomes.ca](https://buyer.solankihomes.ca).
"""

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
payload = {"contents": [{"parts": [{"text": prompt}]}]}

response = requests.post(url, json=payload)
data = response.json()

try:
    article_html = data["candidates"][0]["content"]["parts"][0]["text"]
    article_html = article_html.replace("```html", "").replace("```", "").strip()
except Exception as e:
    print("API Error Response:", data)
    raise e

full_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{selected_topic} in {selected_town}, ON | Prakash Solanki REALTOR®</title>
    <meta name="description" content="Expert insights on {selected_topic} in {selected_town}, Ontario with Prakash Solanki, RE/MAX Pembroke Realty Ltd. Brokerage.">
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link href="[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap)" rel="stylesheet">
    <style>body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}</style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto bg-slate-800 p-6 sm:p-10 rounded-2xl border border-slate-700 shadow-2xl">
        <div class="mb-8 border-b border-slate-700 pb-6">
            <a href="[https://solankihomes.ca](https://solankihomes.ca)" class="text-xs font-bold uppercase text-red-500 tracking-wider hover:underline">← Back to SolankiHomes.ca</a>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-white mt-3 leading-tight">{selected_topic} in {selected_town}, ON</h1>
            <p class="text-xs text-slate-400 mt-2">Published by Prakash Solanki, REALTOR® on {today_str}</p>
        </div>
        <div class="prose prose-invert max-w-none text-slate-300 leading-relaxed space-y-4">
            {article_html}
        </div>
        <div class="mt-12 p-6 bg-slate-900 rounded-xl border border-red-500/30 text-center space-y-3">
            <h3 class="text-xl font-bold text-white">Planning a Move in {selected_town} or the Ottawa Valley?</h3>
            <p class="text-sm text-slate-300">Contact Prakash Solanki today for a free home evaluation or personalized MLS® property alerts.</p>
            <div class="pt-2 flex justify-center gap-4">
                <a href="[https://buyer.solankihomes.ca](https://buyer.solankihomes.ca)" class="bg-blue-600 hover:bg-blue-700 text-white font-bold px-5 py-2.5 rounded-xl text-sm transition">Find Homes</a>
                <a href="[https://seller.solankihomes.ca](https://seller.solankihomes.ca)" class="bg-red-600 hover:bg-red-700 text-white font-bold px-5 py-2.5 rounded-xl text-sm transition">Free Valuation</a>
            </div>
        </div>
    </div>
</body>
</html>"""

os.makedirs("blog", exist_ok=True)
filename = f"blog/{slug_date}-{selected_town.lower().replace(' ', '-')}.html"

with open(filename, "w", encoding="utf-8") as f:
    f.write(full_page)

print(f"Successfully generated article: {filename}")
