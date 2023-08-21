def fetch_data(ticker):
    # Make an API call to a stock market data provider.
    # For now, we will simulate this with placeholder data.
    data = {
        "NAV": 82.24,
        "market_price": 82.26,
        "IIV": 81.86,
        "PE_ratio": 13.8,
        "PB_ratio": 1.8
    }
    return data


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

    # Simulated benchmark data (e.g., VFH)
    benchmark_data = {
        "PE_ratio": 15.9,
        "PB_ratio": 1.8
    }

    for ticker in tickers:
        data = fetch_data(ticker.strip())
        premium_discount, valuation = analyze_etf(data, benchmark_data)

        print(f"\nETF {ticker.strip()} Analysis:")
        print(f"Trading at a {premium_discount} to its NAV.")
        print(f"It is {valuation} based on its P/E and P/B ratios compared to the benchmark.")


if __name__ == "__main__":
    main()
