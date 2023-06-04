import re
from collections import Counter

from src.etc import status_code_to_text

from itertools import islice


def unique_ips(ip_request_dict):
    country_set = set()
    for ip in ip_request_dict:
        country_set.add(ip_request_dict[ip][0]["country"])
    return len(ip_request_dict.keys())


def common_countries(ip_request_dict):
    c = Counter([ip_request_dict[ip][0]["country"] for ip in ip_request_dict])

    n = 10
    res = {}
    for agent in c.most_common(n):
        res[agent[1]] = agent[0]
    return sorted(res.items(), key=lambda x: x[1], reverse=True)


def common_user_agent(ip_request_dict):
    agents = []
    for ip in ip_request_dict:
        for message in ip_request_dict[ip]:
            agents.append(message["useragent"])

    c = Counter(agents)

    n = 10
    res = {}
    for agent in c.most_common(n):
        res[agent[0]] = agent[1]
    return sorted(res.items(), key=lambda x: x[1], reverse=True)


def common_status_codes(ip_request_dict):
    agents = []
    for ip in ip_request_dict:
        for message in ip_request_dict[ip]:
            agents.append(message["statuscode"])

    c = Counter(agents)

    n = 10
    res = {}
    for agent in c.most_common(n):
        res[status_code_to_text(int(agent[0]))] = agent[1]
    return sorted(res.items(), key=lambda x: x[1], reverse=True)


def common_ip_adresses(ip_request_dict):
    n = 10
    res = {}
    for ip in islice(ip_request_dict, n):
        res[ip] = len(ip_request_dict[ip])
    return res


def common_urls_requested(ip_request_dict, ip=None, n=10):
    urls = []
    for ip_entry in ip_request_dict.items():
        # log only specific ip
        if ip != None and ip_entry[0] != ip:
            continue
        urls += [message["url"] for message in ip_entry[1]]

    c = Counter(urls)
    res = {}
    for value in c.most_common(n):
        res[value[0]] = value[1]
    return sorted(res.items(), key=lambda x: x[1], reverse=True)


def unique_url_counts(ip_request_dict, n=50):
    urls = []

    for ip in ip_request_dict:
        for message in ip_request_dict[ip]:
            urls.append(message["url"])

    c = Counter(urls)
    res = {}
    for value in c.most_common(n):
        res[value[0]] = value[1]
    return res


def ip_by_countries(ip_request_dict):
    country_dict = {}

    for ip in ip_request_dict:
        country = ip_request_dict[ip][0]["country"]
        if country in country_dict:
            country_dict[country].append(ip_request_dict[ip])
        else:
            country_dict[country] = [ip_request_dict[ip]]
    return country_dict


def specific_urls_requested(ip_request_dict, specific_urls):
    n = 100
    urls = []

    # count all urls that are in the specific_urls list
    for ip in ip_request_dict:
        for message in ip_request_dict[ip]:
            # trim url from space
            message["url"] = message["url"].strip()

            if message["url"] in specific_urls:
                urls.append(message["url"])

            # if specific url is a regex
            for specific_url in specific_urls:
                if not specific_url.startswith("regex:"):
                    continue
                # remove regex prefix
                specific_url = specific_url[6:]
                if re.match(specific_url, message["url"]):
                    urls.append(specific_url)
                    break

    c = Counter(urls)
    res = {}
    for value in c.most_common(n):
        res[value[0]] = value[1]
    return sorted(res.items(), key=lambda x: x[1], reverse=True)


def common_referrers(ip_log_messages_dict, n):
    # Find top 10 refferers
    refferer = []
    for ip in ip_log_messages_dict:
        for message in ip_log_messages_dict[ip]:
            refferer.append(message['refferer'])

    c = Counter(refferer)
    res = {}
    for value in c.most_common(n):
        res[value[0]] = value[1]
    return sorted(res.items(), key=lambda x: x[1], reverse=True)

