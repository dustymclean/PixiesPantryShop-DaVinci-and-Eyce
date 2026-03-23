# Pixie's Pantry - DaVinci & Eyce Storefront Guide

## 1. Overview
This project is an automated static HTML storefront generator. It takes wholesale product data (from `Synergy_Scraper`) and turns it into a fully functional, mobile-responsive e-commerce website with interactive product variants.

## 2. Prerequisites
- Python 3 installed on your Mac
- `requests` library for the scraper
- A GitHub account for hosting

## 3. How to Re-Scrape
When new products arrive or prices change, run the scraper to get fresh data:
1. Open Terminal.
2. `cd ~/Desktop/Synergy_Scraper`
3. `source venv/bin/activate` (starts the Python virtual environment)
4. `python3 scrape_synergy.py`
5. The script will log in, pull the latest data, and update `synergy_products.json` and `synergy_products.csv`.

## 4. How to Regenerate the Storefront
Once you have fresh scraped data, rebuild the website:
1. Open Terminal.
2. `cd ~/Desktop/Synergy_Shop`
3. `python3 generate_storefront.py`
4. The script will instantly build all new HTML pages in the folder.

## 5. How to Update Products (Full Workflow)
To completely update your live site:
1. Re-scrape data (Step 3).
2. Regenerate storefront (Step 4).
3. Push to GitHub (Step 6).

## 6. GitHub Pages Deployment
To put the site live on the internet:
1. `cd ~/Desktop/Synergy_Shop`
2. `git add -A`
3. `git commit -m "Update products"`
4. `git push origin main`
5. Go to your GitHub Repository Settings -> Pages. Ensure the source is set to `Deploy from a branch` and select `main` (or whichever branch you pushed).
6. To add a custom domain (like `vapes.pixiespantryshop.com`), add the domain in the GitHub Pages settings and configure your DNS provider.

## 7. File Structure
- `generate_storefront.py`: The Python brain that builds the website.
- `index.html`: The homepage.
- `davinci.html` / `eyce.html`: Brand-specific pages.
- `css/style.css`: The visual design and layout.
- `js/main.js`: The interactivity (clicking variants to change images).
- `categories/`: Folder containing all the individual category pages.

## 8. Customization Guide
- **Change Colors:** Open `generate_storefront.py`, find the CSS block (`css_content = ...`), and change the HEX codes for `--gold`, `--primary`, or `--bg`.
- **Change Logo/Name:** Open `generate_storefront.py`, find the `get_sidebar_html()` function, and edit the text.

## 9. Troubleshooting
- **"File not found: synergy_products.json"**: Make sure you ran the scraper first. The generator needs the scraper's output file to exist.
- **Images broken**: Ensure the JSON contains valid Shopify CDN URLs. The script uses exactly what Synergy provides.
- **Storefront looks weird after editing Python**: You likely broke the HTML formatting in `generate_storefront.py`. Check your quotes and tags.

## 10. Glossary
- **JSON**: A data file format that computers use to talk to each other.
- **CSV**: A spreadsheet format.
- **Variant**: A specific color, size, or style of a base product.
- **Handle**: The URL-friendly name of a product (e.g., `davinci-iq3`).
- **GitHub Pages**: A free service from GitHub that hosts static HTML websites on the internet.
