# -*- encoding: utf-8 -*-


from datetime import datetime
from collections import Counter
import re


def gen_reqexp(ignore_files=False,
               request_type=None,
               ignore_www=False,
               slow_queries=False):
    data = '\[(?P<datetime>\d+/\w+/\d+ \d+:\d+:\d+)\]'
    req_type = '\w+' if request_type is None else '(?:{})'.format("|".join(request_type))
    url_1 = r'\w+://{}(?P<url>[\w.]+[^ \t\n\r\f\v]*)'
    url_2 = r'\w+://{}(?P<url>[\w.]+[^ \t\n\r\f\v.]*)'
    url = url_2 if ignore_files else url_1
    url = url.format("(?:www\.)?" if ignore_files else "")
    p_time = '(?P<p_time>\d+)' if slow_queries else '\d+'
    fields = {'data': data,
              'req_type': req_type,
              'url': url,
              'p_time': p_time}
    
    regexp = '{date} "{req_type} {url} \S+" \d+ {p_time}'
    
    regexp = regexp.format(**fields)
   
    return regexp


def parse(ignore_files=False,
          ignore_urls=[],
          start_at=None,
          stop_at=None,
          request_type=None,
          ignore_www=False,
          slow_queries=False,
          file_name = "log.log"):
    with open(file_name) as f:
        reqexp = gen_reqexp(ignore_files, request_type, ignore_www, slow_queries)
        reqexp = re.compile(reqexp)
        ignore_urls_set = set(ignore_urls)
        count = Counter()

        if slow_queries:
            p_time = Counter()
        if start_at:
            start_at = datetime.strptime(start_at, '%d%b%Y %H:%M:%S')
        if stop_at:
            stop_at = datetime.strptime(stop_at, '%d%b%Y %H:%M:%S')
        for line in line:
            m = reqexp.match(line)
            if m:
                m = m.groupdict()
                if start_at or stop_at:
                    lod_date = datetime.strptime(m['datetime'], '%d%b%Y %H:%M:%S')
                if start_at:
                    if lod_date < start_at:
                        continue
                if stop_at:
                    if lod_date > stop_at:
                        break
                if ignore_urls:
                    if m['url'] in ignore_urls_set:
                        continue
                if slow_queries:
                    p_time[m['url']] += int(m['p_time'])
                count[m['url']] += 1
        if slow_queries:
            for k in count:
                count[k] = p_time[k] // count[k]
    return [v[1] for v in count.most_common(5)]


if __name__ == '__main__':
    parse()
    

    

a=[1,3,4,2,0,2]