
    document.addEventListener('DOMContentLoaded', () => {
        const modalOverlay = document.getElementById('modal-overlay');
        const modalClose = document.getElementById('modal-close');
        
        // Checkout elements
        const checkoutOverlay = document.getElementById('checkout-overlay');
        const checkoutClose = document.getElementById('checkout-close');
        const checkoutBtn = document.getElementById('checkout-btn');
        const checkoutForm = document.getElementById('checkout-form');
        const checkoutItemDesc = document.getElementById('checkout-item-desc');
        const checkoutFeedback = document.getElementById('checkout-feedback');
        const cSubmit = document.getElementById('c_submit');
        
        let currentCheckoutItem = null;
        
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
            
            currentCheckoutItem = {
                title: p.title,
                brand: p.brand,
                variant: firstVariant.option1_value || 'Default',
                price: parseFloat(firstVariant.price).toFixed(2)
            };
            
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
                        const vPrice = parseFloat(v.price).toFixed(2);
                        mPrice.textContent = '$' + vPrice;
                        currentCheckoutItem.variant = v.option1_value || 'Default';
                        currentCheckoutItem.price = vPrice;
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
        
        // Checkout Logic
        checkoutBtn.onclick = () => {
            if(!currentCheckoutItem) return;
            modalOverlay.classList.remove('active');
            checkoutItemDesc.textContent = `Ordering: ${currentCheckoutItem.title} - ${currentCheckoutItem.variant} ($${currentCheckoutItem.price})`;
            checkoutOverlay.classList.add('active');
        };
        
        checkoutClose.onclick = () => {
            checkoutOverlay.classList.remove('active');
            document.body.style.overflow = '';
        };
        
        checkoutForm.onsubmit = async (e) => {
            e.preventDefault();
            cSubmit.disabled = true;
            cSubmit.textContent = "Processing...";
            checkoutFeedback.style.display = "block";
            checkoutFeedback.style.color = "#333";
            checkoutFeedback.textContent = "Securing order...";
            
            // Generate unique Order ID PX-[YYMMDD]-[RANDOM4]
            const dateStr = new Date().toISOString().slice(2,10).replace(/-/g,'');
            const rand4 = Math.floor(1000 + Math.random() * 9000);
            const orderId = `PX-${dateStr}-${rand4}`;
            
            const name = document.getElementById('c_name').value;
            const email = document.getElementById('c_email').value;
            const phone = document.getElementById('c_phone').value;
            const discordUser = document.getElementById('c_discord').value || "Not provided";
            const address = `${document.getElementById('c_address').value}, ${document.getElementById('c_city').value}, ${document.getElementById('c_state').value} ${document.getElementById('c_zip').value}`;
            
            const payload = {
                username: "Pixie's Pantry Store",
                embeds: [{
                    title: `🚨 New Order: ${orderId}`,
                    color: 13938487, // Gold-ish
                    fields: [
                        { name: "Item", value: `${currentCheckoutItem.title} (${currentCheckoutItem.variant})`, inline: false },
                        { name: "Price", value: `$${currentCheckoutItem.price}`, inline: true },
                        { name: "Brand", value: currentCheckoutItem.brand, inline: true },
                        { name: "Customer Name", value: name, inline: false },
                        { name: "Phone Number", value: phone, inline: true },
                        { name: "Discord", value: discordUser, inline: true },
                        { name: "Email", value: email, inline: false },
                        { name: "Shipping Address", value: address, inline: false }
                    ],
                    footer: { text: "Pixie's Pantry Automated Checkout" },
                    timestamp: new Date().toISOString()
                }]
            };
            
            try {
                const res = await fetch("https://discord.com/api/webhooks/1485760760939417811/p9gAtkJd3-Rw64TlaQK0FjbDrFHPRWq32pcEcl_ZghQ7qa17vnFZsJr3thAjO__xRosE", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                
                if(res.ok || res.status === 204) {
                    checkoutFeedback.style.color = "green";
                    checkoutFeedback.textContent = `Success! Order ID: ${orderId}. We will contact you for payment.`;
                    checkoutForm.reset();
                    setTimeout(() => {
                        checkoutOverlay.classList.remove('active');
                        cSubmit.disabled = false;
                        cSubmit.textContent = "Submit Order";
                        checkoutFeedback.style.display = "none";
                        document.body.style.overflow = '';
                    }, 4000);
                } else {
                    throw new Error("Webhook failed");
                }
            } catch(err) {
                checkoutFeedback.style.color = "red";
                checkoutFeedback.textContent = "Error submitting order. Please try again or contact support.";
                cSubmit.disabled = false;
                cSubmit.textContent = "Submit Order";
            }
        };
    });
    