from scrape import scrape_data


def fetch_data(ticker):
    # Using the scrape_data function from scrape.py to fetch real data for the given ticker
    base_url = "https://investor.vanguard.com/investment-products/etfs/profile/"
    url = base_url + ticker.strip()
    data, benchmark_data = scrape_data(url)
    print(f"Data for {ticker.strip()} fetched successfully!")
    print(f"ETF Data: {data}")
    print(f"Benchmark Data: {benchmark_data}")
    return data, benchmark_data


def analyze_etf(data, benchmark_data):
    # Compare market price to NAV
    if data["market_price"] > data["NAV"]:
        premium_discount = "premium"
    elif data["market_price"] < data["NAV"]:
        premium_discount = "discount"
    else:
        premium_discount = "fair value"

    # Compare P/E and P/B to benchmark
    valuation = "fairly valued"
    if data["PE_ratio"] > benchmark_data["PE_ratio"] or data["PB_ratio"] > benchmark_data["PB_ratio"]:
        valuation = "overvalued"
    elif data["PE_ratio"] < benchmark_data["PE_ratio"] or data["PB_ratio"] < benchmark_data["PB_ratio"]:
        valuation = "undervalued"

    return premium_discount, valuation


def main():
    tickers = input("Enter the ETF tickers separated by commas: ").split(",")

    for ticker in tickers:
        data, benchmark_data = fetch_data(ticker.strip())
        premium_discount, valuation = analyze_etf(data, benchmark_data)

        print(f"\nETF {ticker.strip()} Analysis:")
        print(f"Trading at a {premium_discount} to its NAV.")
        print(f"It is {valuation} based on its P/E and P/B ratios compared to the benchmark.\n")


if __name__ == "__main__":
    main()
