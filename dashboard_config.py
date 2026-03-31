"""
Dashboard Configuration Integration for Synergy Store
Loads Pixie's Picks, Sales, Featured items, Bundles, and Carousels
for DaVinci & Eyce products.
"""
import json
import os
import re

SYNERGY_DIR = os.path.expanduser("~/Desktop/Synergy_Shop")
BUNDLES_PATH = os.path.join(SYNERGY_DIR, "bundles.json")
FEATURED_PATH = os.path.join(SYNERGY_DIR, "featured.json")
SALES_PATH = os.path.join(SYNERGY_DIR, "sales.json")
PICKS_PATH = os.path.join(SYNERGY_DIR, "pixies_picks.json")
CAROUSELS_PATH = os.path.join(SYNERGY_DIR, "carousels.json")


def load_json_file(path, default=None):
    """Load a JSON file safely"""
    if default is None:
        default = {}
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load {path}: {e}")
            return default
    return default


def save_json_file(path, data):
    """Save a JSON file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_picks():
    """Get list of Pixie's Pick SKUs for Synergy store"""
    data = load_json_file(PICKS_PATH, {"items": []})
    return data.get("items", [])


def get_sales():
    """Get sales data for Synergy store"""
    data = load_json_file(SALES_PATH, {"items": [], "global_discount": 10})
    return {
        "items": data.get("items", []),
        "global_discount": data.get("global_discount", 10)
    }


def get_featured():
    """Get featured items for Synergy store"""
    data = load_json_file(FEATURED_PATH, {"items": []})
    return data.get("items", [])


def get_bundles():
    """Get all active bundles for Synergy store"""
    data = load_json_file(BUNDLES_PATH, {})
    return {k: v for k, v in data.items() if isinstance(v, dict) and v.get("active", True)}


def get_carousels():
    """Get featured carousels for Synergy store"""
    data = load_json_file(CAROUSELS_PATH, {"carousels": []})
    return data.get("carousels", [])


def is_pick(sku):
    """Check if SKU is a Pixie's Pick"""
    return sku in get_picks()


def is_on_sale(sku):
    """Check if SKU is on sale"""
    return sku in get_sales()["items"]


def is_featured(sku):
    """Check if SKU is featured"""
    return sku in get_featured()


def get_sale_price(original_price, sku):
    """Calculate sale price for an item"""
    sales = get_sales()
    if sku in sales["items"]:
        discount = sales["global_discount"]
        return original_price * (1 - discount / 100)
    return original_price


def get_product_badges(sku):
    """Get all badges for a Synergy product"""
    badges = []
    if is_pick(sku):
        badges.append({
            "type": "pick",
            "label": "Pixie's Pick",
            "color": "#d4af37",
            "position": "top-left"
        })
    if is_on_sale(sku):
        badges.append({
            "type": "sale",
            "label": "On Sale",
            "color": "#e74c3c",
            "position": "top-right"
        })
    if is_featured(sku):
        badges.append({
            "type": "featured",
            "label": "Featured",
            "color": "#9b59b6",
            "position": "bottom-left"
        })
    return badges


def build_badge_html(sku):
    """Build HTML for product badges"""
    badges = get_product_badges(sku)
    html_parts = []
    
    for badge in badges:
        if badge["type"] == "pick":
            html_parts.append(f'''<div class="badge-pick" style="position:absolute;top:10px;left:10px;background:linear-gradient(135deg,#d4af37,#f4d03f);color:#111;padding:5px 12px;font-size:0.75em;font-weight:700;text-transform:uppercase;border-radius:4px;box-shadow:0 2px 8px rgba(212,175,55,0.4);">⭐ Pixie's Pick</div>''')
        elif badge["type"] == "sale":
            html_parts.append(f'''<div class="badge-sale" style="position:absolute;top:10px;right:10px;background:#e74c3c;color:#fff;padding:5px 12px;font-size:0.75em;font-weight:700;text-transform:uppercase;border-radius:4px;">🔥 On Sale</div>''')
        elif badge["type"] == "featured":
            html_parts.append(f'''<div class="badge-featured" style="position:absolute;bottom:10px;left:10px;background:#9b59b6;color:#fff;padding:5px 12px;font-size:0.75em;font-weight:700;border-radius:4px;">⭐ Featured</div>''')
    
    return "".join(html_parts)


def build_bundle_section():
    """Build HTML section for Synergy bundles"""
    bundles = get_bundles()
    if not bundles:
        return ""
    
    html_parts = ['''
<section id="synergy-bundles" class="bundles-section" style="padding:40px 20px;background:rgba(212,175,55,0.05);">
    <h2 style="text-align:center;font-size:2em;margin-bottom:30px;color:#d4af37;">📦 DaVinci & Eyce Bundles</h2>
    <div style="max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;">
''']
    
    for bundle_id, bundle in bundles.items():
        name = bundle.get("name", "Premium Bundle")
        discount = bundle.get("discount", 15)
        desc = bundle.get("description", "")
        products = bundle.get("products", [])
        
        product_cards = ""
        for sku in products[:4]:
            product_cards += f'<div style="background:#2a2a3e;padding:10px;border-radius:8px;margin:5px;">SKU: {sku}</div>'
        
        html_parts.append(f'''
        <div class="bundle-card" style="background:rgba(255,255,255,0.05);border:2px solid #d4af37;border-radius:16px;padding:20px;">
            <h3 style="color:#d4af37;margin-bottom:10px;">{name}</h3>
            <div style="background:#1a1a2e;border-radius:8px;padding:10px;margin:10px 0;">
                {product_cards}
            </div>
            <div style="color:#e74c3c;font-weight:bold;font-size:1.5em;">{discount}% OFF Bundle</div>
            <p style="color:#888;font-size:0.9em;margin-top:10px;">{desc[:150]}...</p>
            <button onclick="contactForBundle('{bundle_id}')" style="background:linear-gradient(135deg,#d4af37,#b8960c);color:#111;border:none;padding:12px 24px;border-radius:8px;font-weight:600;cursor:pointer;margin-top:15px;width:100%;">Contact for Bundle Price</button>
        </div>
''')
    
    html_parts.append('</div></section>')
    return "".join(html_parts)


def get_all_config():
    """Get all dashboard configuration for Synergy store"""
    return {
        "picks": get_picks(),
        "sales": get_sales(),
        "featured": get_featured(),
        "bundles": get_bundles(),
        "carousels": get_carousels()
    }


if __name__ == "__main__":
    print("Synergy Dashboard Configuration")
    print("=" * 40)
    print(f"Pixie's Picks: {len(get_picks())} items")
    print(f"On Sale: {len(get_sales()['items'])} items")
    print(f"Featured: {len(get_featured())} items")
    print(f"Bundles: {len(get_bundles())} active")