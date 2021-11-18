from sec_edgar_downloader import Downloader
import sys

# Initialize a downloader instance. If no argument is passed
# to the constructor, the package will download filings to
# the current working directory.

def download_report(ticker, type="10-Q"):
    dl = Downloader("./raw")
    dl.get(type, ticker, after="2016-01-01")

if __name__ == "__main__":
    company = sys.argv[1]    
    print(f"starting program with {company}")
    download_report(company, "10-Q")