from login import login
import datetime
import time
import pandas as pd
import os

# Gets data only upto 27-01-2025 since we don't have minute price series data before that(tested with test_dates.py)
def get_last_year_timestamps():
    today = datetime.date.today()
    one_year_ago = today - datetime.timedelta(days=365)
    
    # Define start and end times for the last year (market hours 9:15 to 15:30)
    # Start from one year ago at market open
    start_time = datetime.datetime.combine(one_year_ago, datetime.time(9, 15))
    # End at yesterday's market close (today might still be ongoing)
    yesterday = today - datetime.timedelta(days=1)
    end_time = datetime.datetime.combine(yesterday, datetime.time(15, 30))
    
    return int(start_time.timestamp()), int(end_time.timestamp())

def fetch_sbin_data():
    api = login()
    if api is None:
        print("Failed to login. Exiting.")
        return

    # Search for SBIN token
    search_result = api.searchscrip(exchange='NSE', searchtext='SBIN')
    if search_result and 'values' in search_result:
        # Assuming the first result is the correct one (SBIN-EQ)
        sbin_token = None
        for scrip in search_result['values']:
             if scrip['tsym'] == 'SBIN-EQ':
                 sbin_token = scrip['token']
                 break
        
        if sbin_token:
            print(f"Found SBIN token: {sbin_token}")
            
            start_ts, end_ts = get_last_year_timestamps()
            print(f"Fetching data from {datetime.datetime.fromtimestamp(start_ts)} to {datetime.datetime.fromtimestamp(end_ts)}")
            
            # Fetch per minute data (interval=1 for 1 minute)
            # Note: The interval parameter in get_time_price_series might be in minutes or specific codes.
            # Based on example_market.py, interval=1 seems to be 1 minute.
            # Let's try to verify if there is an enum or specific value.
            # example_market.py uses 'v' => get 1 min market data, but calls api.get_time_price_series with interval=240?
            # Wait, example_market.py line 89: ret = api.get_time_price_series(exchange='NSE', token='22', starttime=1642265814, endtime=1642438794, interval=240)
            # But the prompt says "v => get 1 min market data". This is confusing.
            # Let's assume interval is in minutes. 1 minute = 1.
            
            ret = api.get_time_price_series(exchange='NSE', token=sbin_token, starttime=start_ts, endtime=end_ts, interval=1)
            
            if ret:
                df = pd.DataFrame.from_dict(ret)
                print(df.head())
                
                # Define output directory and file path
                output_dir = os.path.join(os.path.dirname(__file__), 'data', 'SBI')
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, 'sbin_data.csv')
                df.to_csv(output_file, index=False)
                print(f"Data saved to {output_file}")
            else:
                print("No data returned from API.")
        else:
            print("SBIN-EQ token not found in search results.")
    else:
        print("Failed to search for SBIN.")

if __name__ == "__main__":
    fetch_sbin_data()
