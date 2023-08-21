from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_data(target_url):
    driver = webdriver.Chrome()  # Make sure ChromeDriver is installed and in PATH
    driver.get(target_url)
    # driver.implicitly_wait(0.5)

    # Extracting Current Market Price (IIV), Closing Market Price, and Closing NAV Price
    iiv = float(
        driver.find_element(
            by=By.CSS_SELECTOR, value='h2[data-rpa-tag-id="priceMarket"]').text.replace('$', ''))
    market_price = float(
        driver.find_element(
            by=By.CSS_SELECTOR, value='h4[data-rpa-tag-id="priceMarket"]').text.replace('$', ''))
    nav_price = float(driver.find_element(
        by=By.CSS_SELECTOR, value='h4[data-rpa-tag-id="priceNAV"]').text.replace('$', ''))

    # Extracting P/E Ratio for data and benchmark_data
    pe_ratio_data = float(
        driver.find_element(
            by=By.CSS_SELECTOR, value='.equity-characteristics:nth-child(6) td:nth-child(2)').text.replace(
            'x', ''))
    pe_ratio_benchmark = float(
        driver.find_element(
            by=By.CSS_SELECTOR, value='.equity-characteristics:nth-child(6) td:nth-child(3)').text.replace(
            'x', ''))

    # Extracting P/B Ratio for data and benchmark_data
    pb_ratio_data = float(
        driver.find_element(
            by=By.CSS_SELECTOR, value='.equity-characteristics:nth-child(7) td:nth-child(2)').text.replace('x', ''))
    pb_ratio_benchmark = float(
        driver.find_element(
            by=By.CSS_SELECTOR, value='.equity-characteristics:nth-child(7) td:nth-child(3)').text.replace('x', ''))

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
