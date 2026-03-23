
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
    