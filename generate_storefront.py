import json
import os
import re

JSON_PATH = os.path.expanduser("~/Desktop/Synergy_Scraper/synergy_products.json")
OUTPUT_DIR = os.path.expanduser("~/Desktop/Synergy_Shop")

def slugify(text):
    text = str(text).lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text

def ensure_dirs():
    os.makedirs(os.path.join(OUTPUT_DIR, "css"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "js"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "categories"), exist_ok=True)

def generate_site():
    ensure_dirs()
    if not os.path.exists(JSON_PATH):
        print(f"File not found: {JSON_PATH}")
        return
        
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    products = data.get("products", [])
    
    # Organize products
    brands = {"DaVinci": [], "Eyce": []}
    categories = {}
    
    for p in products:
        b = p.get("brand")
        if b in brands:
            brands[b].append(p)
            
        ptype = p.get("product_type") or "Accessories"
        if b not in categories:
            categories[b] = {}
        if ptype not in categories[b]:
            categories[b][ptype] = []
        categories[b][ptype].append(p)
        
    print(f"Loaded {len(products)} products.")
    
    # CSS
    css_content = """
    :root { --primary: #111; --gold: #d4af37; --bg: #fff; --muted: #888; --border: #eaeaea; --sidebar-w: 260px; }
    body { font-family: 'Helvetica Neue', Arial, sans-serif; background: var(--bg); color: var(--primary); margin: 0; padding: 0; }
    .sidebar { position: fixed; width: var(--sidebar-w); left: 0; top: 0; bottom: 0; background: #fafafa; border-right: 1px solid var(--border); overflow-y: auto; padding: 30px 20px; box-sizing: border-box; }
    .sidebar-logo { font-size: 22px; font-weight: 800; text-decoration: none; color: #000; display: block; margin-bottom: 5px; }
    .sidebar-tagline { font-size: 11px; text-transform: uppercase; color: var(--muted); letter-spacing: 1px; margin-bottom: 30px; }
    .sidebar-section { font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin: 20px 0 10px; color: var(--muted); }
    .sidebar-link { display: block; padding: 6px 0; color: #333; text-decoration: none; font-size: 14px; font-weight: 500; }
    .sidebar-link:hover, .sidebar-link.active { color: var(--gold); }
    .sidebar-link.child { padding-left: 15px; font-size: 13px; color: #555; }
    .sidebar-footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--border); }
    
    .main-wrapper { margin-left: var(--sidebar-w); min-height: 100vh; display: flex; flex-direction: column; }
    .main-content { padding: 40px 50px; flex: 1; }
    
    .page-title { font-size: 32px; font-weight: 800; margin: 0 0 10px; }
    .page-subtitle { color: var(--muted); margin-bottom: 40px; }
    
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 30px; }
    .card { border: 1px solid var(--border); border-radius: 12px; overflow: hidden; background: #fff; transition: transform 0.2s, box-shadow 0.2s; display: flex; flex-direction: column; cursor: pointer; }
    .card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); border-color: #ddd; }
    .card-img { width: 100%; height: 280px; object-fit: contain; padding: 20px; box-sizing: border-box; background: #fdfdfd; border-bottom: 1px solid var(--border); }
    .card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; }
    .card-brand { font-size: 11px; text-transform: uppercase; color: var(--muted); letter-spacing: 1px; margin-bottom: 5px; }
    .card-title { font-size: 16px; font-weight: 600; margin: 0 0 10px; flex: 1; line-height: 1.4; }
    .card-price { font-size: 18px; font-weight: 700; color: var(--gold); margin-bottom: 15px; }
    .btn { display: inline-block; background: #000; color: #fff; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 700; text-transform: uppercase; text-align: center; border: none; cursor: pointer; transition: background 0.2s; }
    .btn:hover { background: var(--gold); }
    .btn-outline { background: transparent; color: #000; border: 1px solid #000; }
    .btn-outline:hover { background: #000; color: #fff; }
    
    /* Modal */
    .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1000; display: none; align-items: center; justify-content: center; backdrop-filter: blur(4px); }
    .modal-overlay.active { display: flex; }
    .modal { background: #fff; width: 90%; max-width: 1000px; max-height: 90vh; border-radius: 16px; display: flex; overflow: hidden; position: relative; box-shadow: 0 20px 50px rgba(0,0,0,0.2); }
    .modal-close { position: absolute; top: 20px; right: 20px; background: #f0f0f0; border: none; width: 36px; height: 36px; border-radius: 50%; font-size: 20px; cursor: pointer; z-index: 10; display: flex; align-items: center; justify-content: center; }
    .modal-close:hover { background: #e0e0e0; }
    .modal-left { width: 50%; background: #fdfdfd; padding: 40px; border-right: 1px solid var(--border); position: relative; }
    .modal-main-img { width: 100%; height: 400px; object-fit: contain; margin-bottom: 20px; }
    .modal-right { width: 50%; padding: 40px; overflow-y: auto; max-height: 90vh; }
    .modal-brand { font-size: 12px; text-transform: uppercase; color: var(--muted); letter-spacing: 1px; margin-bottom: 5px; }
    .modal-title { font-size: 28px; font-weight: 800; margin: 0 0 15px; }
    .modal-price { font-size: 24px; font-weight: 700; color: var(--gold); margin-bottom: 25px; }
    .modal-desc { font-size: 15px; line-height: 1.6; color: #444; margin-bottom: 30px; }
    .modal-desc p { margin-top: 0; }
    .variant-label { font-size: 12px; font-weight: 800; text-transform: uppercase; margin-bottom: 10px; display: block; }
    .swatch-group { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 30px; }
    .swatch { border: 1px solid #ddd; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; background: #fff; transition: all 0.2s; }
    .swatch:hover { border-color: #aaa; }
    .swatch.selected { border-color: #000; background: #000; color: #fff; }
    .modal-buy-btn { width: 100%; padding: 15px; font-size: 15px; border-radius: 8px; }
    
    @media (max-width: 900px) {
        .sidebar { transform: translateX(-100%); z-index: 100; transition: transform 0.3s; }
        .main-wrapper { margin-left: 0; }
        .modal { flex-direction: column; overflow-y: auto; }
        .modal-left, .modal-right { width: 100%; }
        .modal-left { border-right: none; border-bottom: 1px solid var(--border); padding: 20px; }
        .modal-main-img { height: 300px; }
        .modal-right { max-height: none; padding: 20px; }
    }
    """
    with open(os.path.join(OUTPUT_DIR, "css", "style.css"), "w") as f:
        f.write(css_content)
        
    # JS
    js_content = """
    document.addEventListener('DOMContentLoaded', () => {
        const modalOverlay = document.getElementById('modal-overlay');
        const modalClose = document.getElementById('modal-close');
        
        // Elements to update
        const mBrand = document.getElementById('m-brand');
        const mTitle = document.getElementById('m-title');
        const mPrice = document.getElementById('m-price');
        const mDesc = document.getElementById('m-desc');
        const mImg = document.getElementById('m-img');
        const swatchesContainer = document.getElementById('swatches');
        const vLabel = document.getElementById('v-label');
        
        // Products data injected
        window.openModal = function(handle) {
            const p = window.productsData[handle];
            if(!p) return;
            
            mBrand.textContent = p.brand;
            mTitle.textContent = p.title;
            mPrice.textContent = '$' + p.min_price.toFixed(2);
            mDesc.innerHTML = p.body_html || 'No description available.';
            
            const firstVariant = p.in_stock_variants[0];
            mImg.src = firstVariant.variant_image || p.featured_image;
            
            // Build variants
            swatchesContainer.innerHTML = '';
            vLabel.textContent = p.options[0] ? p.options[0].name : 'Options';
            
            if(p.in_stock_variants.length > 0) {
                p.in_stock_variants.forEach((v, idx) => {
                    const btn = document.createElement('button');
                    btn.className = 'swatch' + (idx === 0 ? ' selected' : '');
                    btn.textContent = v.option1_value || 'Default';
                    btn.onclick = () => {
                        document.querySelectorAll('.swatch').forEach(s => s.classList.remove('selected'));
                        btn.classList.add('selected');
                        if(v.variant_image) mImg.src = v.variant_image;
                        mPrice.textContent = '$' + parseFloat(v.price).toFixed(2);
                    };
                    swatchesContainer.appendChild(btn);
                });
            } else {
                swatchesContainer.innerHTML = '<span class="muted">Out of stock</span>';
            }
            
            modalOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        };
        
        modalClose.onclick = () => {
            modalOverlay.classList.remove('active');
            document.body.style.overflow = '';
        };
        
        modalOverlay.onclick = (e) => {
            if(e.target === modalOverlay) {
                modalClose.onclick();
            }
        };
    });
    """
    with open(os.path.join(OUTPUT_DIR, "js", "main.js"), "w") as f:
        f.write(js_content)

    def get_sidebar_html(depth=""):
        html = f"""
        <aside class="sidebar">
            <a href="{depth}index.html" class="sidebar-logo">Pixie's Pantry</a>
            <div class="sidebar-tagline">DaVinci & Eyce</div>
            
            <a href="{depth}index.html" class="sidebar-link">All Products</a>
        """
        
        for brand in ["DaVinci", "Eyce"]:
            html += f"""
            <div class="sidebar-section">{brand}</div>
            <a href="{depth}{brand.lower()}.html" class="sidebar-link">Shop All {brand}</a>
            """
            for cat in sorted(categories.get(brand, {}).keys()):
                if not cat: continue
                html += f'<a href="{depth}categories/{slugify(brand)}-{slugify(cat)}.html" class="sidebar-link child">{cat}</a>'
                
        html += f"""
            <div class="sidebar-footer">
                <a href="{depth}login.html" class="sidebar-link">Log In</a>
                <a href="{depth}signup.html" class="sidebar-link">Sign Up</a>
            </div>
        </aside>
        """
        return html

    def get_modal_html():
        return """
        <div class="modal-overlay" id="modal-overlay">
            <div class="modal">
                <button class="modal-close" id="modal-close">&times;</button>
                <div class="modal-left">
                    <img src="" alt="Product" class="modal-main-img" id="m-img">
                </div>
                <div class="modal-right">
                    <div class="modal-brand" id="m-brand">Brand</div>
                    <h2 class="modal-title" id="m-title">Product Name</h2>
                    <div class="modal-price" id="m-price">$0.00</div>
                    <div class="modal-desc" id="m-desc"></div>
                    
                    <div class="variant-label" id="v-label">Options</div>
                    <div class="swatch-group" id="swatches"></div>
                    
                    <button class="btn modal-buy-btn" onclick="alert('Checkout integration pending')">Add to Cart</button>
                </div>
            </div>
        </div>
        """

    def render_page(filename, title, subtitle, product_list, depth=""):
        sidebar = get_sidebar_html(depth)
        modal = get_modal_html()
        
        # Inject data for JS
        products_dict = {p["handle"]: p for p in product_list}
        json_data = json.dumps(products_dict)
        
        grid_html = '<div class="grid">'
        for p in product_list:
            img = p.get("featured_image") or (p.get("all_images")[0] if p.get("all_images") else "")
            price = p.get("min_price", 0)
            handle = p["handle"]
            grid_html += f"""
            <div class="card" onclick="openModal('{handle}')">
                <img src="{img}" alt="{p['title']}" class="card-img" loading="lazy">
                <div class="card-body">
                    <div class="card-brand">{p['brand']}</div>
                    <h3 class="card-title">{p['title']}</h3>
                    <div class="card-price">${price:.2f}</div>
                    <span class="btn btn-outline" style="width:100%;box-sizing:border-box;">View Details</span>
                </div>
            </div>
            """
        grid_html += '</div>'
        if not product_list:
            grid_html = '<p>No products found in this category.</p>'
            
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} | Pixie's Pantry</title>
    <link rel="stylesheet" href="{depth}css/style.css">
</head>
<body>
    {sidebar}
    <div class="main-wrapper">
        <main class="main-content">
            <h1 class="page-title">{title}</h1>
            <div class="page-subtitle">{subtitle}</div>
            {grid_html}
        </main>
    </div>
    {modal}
    <script>window.productsData = {json_data};</script>
    <script src="{depth}js/main.js"></script>
</body>
</html>"""
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html)
            
    # Write pages
    print("Generating pages...")
    render_page("index.html", "Shop All", "Discover premium devices from DaVinci and Eyce.", products)
    render_page("davinci.html", "DaVinci", "Advanced vaporizers and accessories.", brands.get("DaVinci", []))
    render_page("eyce.html", "Eyce", "Silicone pipes and rigs.", brands.get("Eyce", []))
    
    for brand, cats in categories.items():
        for cat, prods in cats.items():
            if not cat: continue
            render_page(f"categories/{slugify(brand)}-{slugify(cat)}.html", 
                        f"{brand} {cat}", f"Shop all {brand} {cat}.", prods, depth="../")
                        
    # Login / Signup stubs
    auth_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Account | Pixie's Pantry</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        .auth-container { max-width: 400px; margin: 80px auto; text-align: center; }
        .input-box { margin-bottom: 20px; text-align: left; }
        .input-box label { display: block; font-size: 11px; font-weight: 800; text-transform: uppercase; margin-bottom: 8px; }
        .input-box input { width: 100%; border: 1px solid var(--border); padding: 12px; border-radius: 8px; box-sizing: border-box; }
    </style>
</head>
<body>
    {sidebar}
    <div class="main-wrapper">
        <main class="main-content">
            <div class="auth-container">
                <h1 class="page-title">{title}</h1>
                <p class="page-subtitle">FormPress Backend Required</p>
                <div class="input-box"><label>Email</label><input type="email"></div>
                <div class="input-box"><label>Password</label><input type="password"></div>
                <button class="btn" style="width:100%">{title}</button>
            </div>
        </main>
    </div>
</body>
</html>"""
    with open(os.path.join(OUTPUT_DIR, "login.html"), "w") as f:
        f.write(auth_html.replace("{sidebar}", get_sidebar_html()).replace("{title}", "Log In"))
    with open(os.path.join(OUTPUT_DIR, "signup.html"), "w") as f:
        f.write(auth_html.replace("{sidebar}", get_sidebar_html()).replace("{title}", "Sign Up"))
        
    print("Storefront generated successfully!")

if __name__ == "__main__":
    generate_site()
