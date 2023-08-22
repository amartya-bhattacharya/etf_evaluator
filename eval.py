from concurrent.futures import ThreadPoolExecutor

from scrape import scrape_data
import cProfile
import pstats
from io import StringIO


def process_ticker(ticker):
    data, benchmark_data = fetch_data(ticker.strip())
    premium_discount, valuation = analyze_etf(data, benchmark_data)

    analysis = (
        f"\n{ticker.strip()}:",
        f"Trading at a {premium_discount} to its NAV.",
        f"It is {valuation} compared to the benchmark."
    )

    return analysis


def fetch_data(ticker):
    # print(f"Fetching data for {ticker.strip()}...")
    data, benchmark_data = scrape_data(ticker)
    # print(f"{ticker} ETF Data: {data}")
    # print(f"Benchmark Data: {benchmark_data}")
    return data, benchmark_data


def analyze_etf(data, benchmark_data):
    if data["market_price"] is None or data["NAV"] is None:
        premium_discount = "N/A"
    elif data["market_price"] > data["NAV"]:
        premium_discount = "premium"
    elif data["market_price"] < data["NAV"]:
        premium_discount = "discount"
    else:
        premium_discount = "fair value"

    if None in [data["PE_ratio"], benchmark_data["PE_ratio"], data["PB_ratio"], benchmark_data["PB_ratio"]]:
        valuation = "N/A"
    elif data["PE_ratio"] > benchmark_data["PE_ratio"] or data["PB_ratio"] > benchmark_data["PB_ratio"]:
        valuation = "overvalued"
    elif data["PE_ratio"] < benchmark_data["PE_ratio"] or data["PB_ratio"] < benchmark_data["PB_ratio"]:
        valuation = "undervalued"
    else:
        valuation = "fairly valued"

    return premium_discount, valuation


def main():
    tickers = input("Enter the ETF tickers separated by commas: ").split(",")

    profiler = cProfile.Profile()
    s = StringIO()

    profiler.enable()  # Start profiling

    print("Fetching data...")
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_ticker, tickers))

    for result in results:
        print(*result)

    profiler.disable()  # Stop profiling

    stats = pstats.Stats(profiler, stream=s).sort_stats("time")
    stats.print_stats(0)
    print(s.getvalue())  # Print the contents of the StringIO object


if __name__ == "__main__":
    main()
