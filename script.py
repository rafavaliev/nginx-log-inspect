import datetime
from pathlib import Path
import src.transform as Transform
import src.extract as Extract
import src.statistics as Statistics
from time import sleep
import pprint

# Set this to True to resolve country of each ip
GET_COUNTRIES = True

# Set this to the folder with the access.log or access.log.gz files
data_dir = Path('data')


def extract_and_transform(data_dir, date_from, date_to):
    if GET_COUNTRIES:
        print("Running with ip geo resolve, might take longer!")
    else:
        print("Running...")

    log_list = Extract.get_log_list(data_dir)
    log_list = [v for v in Transform.parse_log_list(log_list)]

    for log_event in log_list:
        datetime_obj = datetime.datetime.strptime(log_event['dateandtime'], "%d/%b/%Y:%H:%M:%S %z")
        log_event['dateandtime'] = datetime_obj
    # filter by date_from and date_to
    log_list = [v for v in log_list if v['dateandtime'] > date_from and v['dateandtime'] < date_to]

    # ignore statuscake user_agent
    log_list = [v for v in log_list if v['useragent'] != 'statuscake']

    log_list = Transform.add_countries_to_messages(log_list, GET_COUNTRIES, verbose=True)
    return Transform.to_ip_log_messages_dict(log_list)


time_periods = {
    "last_week": (
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7),
        datetime.datetime.now(datetime.timezone.utc)
    ),
    "last_month": (
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30),
        datetime.datetime.now(datetime.timezone.utc)
    ),
    "last_day": (
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1),
        datetime.datetime.now(datetime.timezone.utc)
    )
}


def print_statistics(ip_log_dict, period_name):
    return {
        "period_name": period_name,
        "unique_ips": Statistics.unique_ips(ip_log_dict),
        "common_user_agent": Statistics.common_user_agent(ip_log_dict),
        "common_countries": Statistics.common_countries(ip_log_dict),
        "common_status_codes": Statistics.common_status_codes(ip_log_dict),
        "common_urls_requested": Statistics.common_urls_requested(ip_log_dict, n=10),
        "common_referrers": Statistics.common_referrers(ip_log_dict, n=10),
        "specific_urls_requested": Statistics.specific_urls_requested(ip_log_dict, []),
    }


for name, values in time_periods.items():
    ip_log_messages_dict = extract_and_transform(data_dir, values[0], values[1])

    pp = pprint.PrettyPrinter(depth=4)
    pp.pprint(print_statistics(ip_log_messages_dict, name))
    sleep(1)
