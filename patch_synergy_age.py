import os

FILE = os.path.expanduser("~/Desktop/Synergy_Shop/generate_storefront.py")
with open(FILE, "r") as f:
    content = f.read()

# Replace banner injection with age gate + banner injection
if '<div class="banner">' in content and 'age-gate-overlay' not in content:
    html = """
    <!-- Age Gate -->
    <div class="age-gate-overlay" id="age-gate-overlay">
        <div class="age-gate-box">
            <div class="age-gate-logo">Pixie's <span>Pantry</span></div>
            <div class="age-gate-tagline">Premium Hardware — Members Only</div>
            <div class="age-gate-heading">Age Verification Required</div>
            <h2 class="age-gate-title">Are you 21 or older?</h2>
            <p class="age-gate-subtitle">This website contains products intended for adults 21 years of age or older. You must verify your age to enter.</p>
            <div class="age-gate-buttons">
                <button class="age-gate-yes" onclick="ageGateEnter()">Yes, I'm 21+</button>
                <button class="age-gate-no" onclick="ageGateDeny()">No, Exit</button>
            </div>
            <p class="age-gate-disclaimer">By entering this site you are agreeing to our Terms of Service and Privacy Policy. This site uses cookies to remember your age verification.</p>
        </div>
    </div>
    <div class="banner">"""
    
    content = content.replace('<div class="banner">', html)
    
    # Inject CSS
    css = """
    /* Age Gate */
    .age-gate-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: #000; z-index: 99999; display: flex; align-items: center; justify-content: center; padding: 20px; }
    .age-gate-box { max-width: 480px; width: 100%; text-align: center; }
    .age-gate-logo { font-size: 28px; font-weight: 900; color: #fff; letter-spacing: -1px; margin-bottom: 8px; }
    .age-gate-logo span { color: var(--gold); }
    .age-gate-tagline { font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: #888; margin-bottom: 50px; }
    .age-gate-heading { font-size: 13px; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; color: #888; margin-bottom: 15px; }
    .age-gate-title { font-size: 38px; font-weight: 900; color: #fff; margin: 0 0 20px; line-height: 1.1; }
    .age-gate-subtitle { font-size: 15px; color: #888; line-height: 1.6; margin-bottom: 40px; }
    .age-gate-buttons { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; }
    .age-gate-yes { background: var(--gold); color: #000; border: none; padding: 16px 40px; font-size: 14px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; border-radius: 8px; cursor: pointer; transition: 0.2s; }
    .age-gate-yes:hover { background: #fff; }
    .age-gate-no { background: transparent; color: #555; border: 1px solid #333; padding: 16px 40px; font-size: 14px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; border-radius: 8px; cursor: pointer; transition: 0.2s; }
    .age-gate-no:hover { border-color: #555; color: #888; }
    .age-gate-disclaimer { font-size: 11px; color: #444; margin-top: 30px; line-height: 1.6; }
    /* Banner */"""
    
    content = content.replace("/* Banner */", css)
    
    # Inject JS
    js = """
        // -- AGE GATE --
        (function() {
            const overlay = document.getElementById('age-gate-overlay');
            if (!overlay) return;
            if (localStorage.getItem('pixies_age_verified') === 'true') {
                overlay.style.display = 'none';
            }
        })();
        window.ageGateEnter = function() {
            localStorage.setItem('pixies_age_verified', 'true');
            document.getElementById('age-gate-overlay').style.display = 'none';
        };
        window.ageGateDeny = function() {
            window.location.href = 'https://www.google.com';
        };
        // Setup initial UI"""
        
    content = content.replace("// Setup initial UI", js)
    
    with open(FILE, "w") as f:
        f.write(content)
        print("Patched synergy age gate")

