from login import login
import datetime

# Test specific dates
api = login()

if api:
    # Search for SBIN token
    search_result = api.searchscrip(exchange='NSE', searchtext='SBIN')
    sbin_token = None
    for scrip in search_result['values']:
        if scrip['tsym'] == 'SBIN-EQ':
            sbin_token = scrip['token']
            break
    
    if sbin_token:
        print(f"SBIN Token: {sbin_token}\n")
        
        # Test dates - including weekdays
        test_dates = [
            (datetime.date(2025, 1, 27), "Monday"),
            (datetime.date(2025, 1, 26), "Sunday"),
            (datetime.date(2025, 1, 25), "Saturday"),
            (datetime.date(2025, 1, 24), "Friday"),
            (datetime.date(2025, 1, 23), "Thursday"),
        ]
        
        for test_date, day_name in test_dates:
            start_time = datetime.datetime.combine(test_date, datetime.time(9, 15))
            end_time = datetime.datetime.combine(test_date, datetime.time(15, 30))
            
            start_ts = int(start_time.timestamp())
            end_ts = int(end_time.timestamp())
            
            print(f"Testing {test_date.strftime('%d-%m-%Y')} ({day_name}):")
            print(f"  Start: {start_time} (timestamp: {start_ts})")
            print(f"  End:   {end_time} (timestamp: {end_ts})")
            
            ret = api.get_time_price_series(
                exchange='NSE',
                token=sbin_token,
                starttime=start_ts,
                endtime=end_ts,
                interval=1
            )
            
            if ret:
                print(f"  Result: SUCCESS - {len(ret)} records returned")
                if len(ret) > 0:
                    print(f"  First: {ret[0]['time']}")
                    print(f"  Last:  {ret[-1]['time']}")
            else:
                print(f"  Result: FAILED - No data returned (ret = {ret})")
            print()
