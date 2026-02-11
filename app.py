import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows your website to make requests to this API

# ==========================================
# 1. THE LOGIC (Cleaned & Pure Python)
# ==========================================
def generate_caption_logic(user_input):
    # Safe extraction with defaults to prevent crashing
    brand = user_input.get('brand_name', 'Brand')
    p_name = user_input.get('product_name', 'Product')
    ingr = user_input.get('ingredients') or "premium ingredients"
    high = user_input.get('product_highlights') or "exceptional results"
    vibe = user_input.get('tone_vibe', 'fun').lower()
    platform = user_input.get('platform', 'instagram').lower()
    obj = user_input.get('campaign_objective', '').lower()

    # --- VARIATION LIBRARIES ---
    hooks = [
        f"Say hello to your best skin yet with {p_name}.",
        f"The secret is out: {brand}’s {p_name} is a game changer.",
        f"Tired of dull skin? {p_name} has entered the chat. ✨",
        f"The {ingr} your routine has been missing.",
        f"POV: You just found your new holy grail. 🧴"
    ]

    luxury_phrases = ["Exclusively crafted", "The pinnacle of skincare", "Indulge in", "Artisanally formulated"]
    science_phrases = ["Clinically proven", "Advanced formula", "Dermatological breakthrough", "pH balanced"]
    
    # --- DYNAMIC SELECTION ---
    if "luxury" in vibe:
        headline = f"{random.choice(luxury_phrases)}: {p_name}"
    elif "scientific" in vibe:
        headline = f"{random.choice(science_phrases)}: {p_name}"
    else:
        headline = random.choice(hooks)

    if "bogo" in obj:
        headline = f"🎁 LIMITED BOGO: {p_name}!"
    
    # --- BODY TEXT CONSTRUCTION ---
    templates = [
        f"Transform your ritual. {brand} combines {ingr} to ensure {high.lower()}. You won't believe the results.",
        f"Why we love it: \n✅ Infused with {ingr}\n✅ {high}\n✅ Designed for {user_input.get('target_audience', 'you')}.",
        f"It's time to treat yourself. {p_name} uses {ingr} to give you that {vibe} glow you've been searching for. {high} never felt so good.",
        f"The wait is over. {p_name} is officially here to {high.lower()}. Formulated specifically with {ingr} for maximum impact."
    ]
    
    body = random.choice(templates)
    
    if "tiktok" in platform or "instagram" in platform:
        body += " ✨ Tap the link in bio to grab yours! 🛍️"

    # Dynamic Hashtags
    base_tags = [f"#{brand.replace(' ', '')}", f"#{p_name.replace(' ', '')}", "#Skincare", "#BeautyTips"]
    random.shuffle(base_tags)
    final_tags = " ".join(base_tags[:4])

    return {
        "headline": headline,
        "body_text": body,
        "call_to_action": f"Shop {brand} at the link below.",
        "hashtags": final_tags
    }

# ==========================================
# 2. THE API ROUTE
# ==========================================
@app.route('/', methods=['GET'])
def home():
    return "Skintellect API is running! Send a POST request to /generate"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get JSON data sent from your website
        data = request.get_json()
        
        # Run the logic
        result = generate_caption_logic(data)
        
        # Return the result as JSON
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
