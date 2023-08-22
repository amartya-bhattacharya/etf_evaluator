from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def scrape_data(target_ticker):
    target_url = build_url(target_ticker)
    options = Options()
    # options.page_load_strategy = 'eager'  # not working
    options.add_argument("--headless=new")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Disable sandbox mode

    driver = webdriver.Chrome(options=options)  # Make sure ChromeDriver is installed and in PATH
    driver.get(target_url)

    # Explicit waits for each element
    wait = WebDriverWait(driver, timeout=10)

    # Extracting Current Market Price (IIV), Closing Market Price, and Closing NAV Price
    try:
        # Wait until the IIV value is not '—'
        iiv_element = wait.until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'h2[data-rpa-tag-id="priceMarket"]')))

        # Additional wait for the text to be different from '—'
        wait.until(lambda driver: iiv_element.text != '—')

        # Extracting the updated IIV
        iiv = float(iiv_element.text.replace('$', ''))
    except Exception as e:
        print(f"{target_ticker} Error scraping IIV: {str(e)}")
        iiv = None

    try:
        market_price_element = wait.until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'h4[data-rpa-tag-id="priceMarket"]')))
        market_price = float(market_price_element.text.replace('$', ''))
    except Exception as e:
        print(f"{target_ticker} Error scraping market price: {str(e)}")
        market_price = None

    try:
        nav_price_element = wait.until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'h4[data-rpa-tag-id="priceNAV"]')))
        nav_price = float(nav_price_element.text.replace('$', ''))
    except Exception as e:
        print(f"{target_ticker} Error scraping NAV price: {str(e)}")
        nav_price = None

    # Extracting P/E Ratio for etf data and benchmark_data
    try:
        pe_ratio_data_element = wait.until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, '.equity-characteristics:nth-child(6) td:nth-child(2)')))
        pe_ratio_data = float(pe_ratio_data_element.text.replace('x', ''))
    except Exception as e:
        print(f"{target_ticker} Error scraping PE ratio data: {str(e)}")
        pe_ratio_data = None

    try:
        pe_ratio_benchmark_element = wait.until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, '.equity-characteristics:nth-child(6) td:nth-child(3)')))
        pe_ratio_benchmark = float(pe_ratio_benchmark_element.text.replace('x', ''))
    except Exception as e:
        print(f"{target_ticker} Error scraping PE ratio benchmark: {str(e)}")
        pe_ratio_benchmark = None

    # Extracting P/B Ratio for etf data and benchmark_data
    try:
        pb_ratio_data_element = wait.until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, '.equity-characteristics:nth-child(7) td:nth-child(2)')))
        pb_ratio_data = float(pb_ratio_data_element.text.replace('x', ''))
    except Exception as e:
        print(f"{target_ticker} Error scraping PB ratio data: {str(e)}")
        pb_ratio_data = None

    try:
        pb_ratio_benchmark_element = wait.until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, '.equity-characteristics:nth-child(7) td:nth-child(3)')))
        pb_ratio_benchmark = float(pb_ratio_benchmark_element.text.replace('x', ''))
    except Exception as e:
        print(f"{target_ticker} Error scraping PB ratio benchmark: {str(e)}")
        pb_ratio_benchmark = None

    etf_data = {
        "NAV": nav_price,
        "market_price": market_price,
        "IIV": iiv,
        "PE_ratio": pe_ratio_data,
        "PB_ratio": pb_ratio_data
    }

    benchmark_data = {
        "PE_ratio": pe_ratio_benchmark,
        "PB_ratio": pb_ratio_benchmark
    }

    driver.quit()

    return etf_data, benchmark_data


def build_url(ticker):
    base_url = "https://investor.vanguard.com/investment-products/etfs/profile/"
    return base_url + ticker.strip()
