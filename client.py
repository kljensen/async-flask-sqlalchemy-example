import gevent
import time
from gevent import monkey
monkey.patch_all()
import urllib2


def fetch_url(url):
    """ Fetch a URL and return the total amount of time required.
    """
    t0 = time.time()
    try:
        resp = urllib2.urlopen(url)
        resp_code = resp.code
    except urllib2.HTTPError, e:
        resp_code = e.code

    t1 = time.time()
    print("\t@ %5.2fs got response [%d]" % (t1 - t0, resp_code))
    return t1 - t0


def time_fetch_urls(url, num_jobs):
    """ Fetch a URL `num_jobs` times in parallel and return the
        total amount of time required.
    """
    print("Sending %d requests for %s..." % (num_jobs, url))
    t0 = time.time()
    jobs = [gevent.spawn(fetch_url, url) for i in range(num_jobs)]
    gevent.joinall(jobs)
    t1 = time.time()
    print("\t= %5.2fs TOTAL" % (t1 - t0))
    return t1 - t0


if __name__ == '__main__':

    num_tries = 5

    # Fetch the URL that blocks with a `time.sleep`
    t0 = time_fetch_urls("http://localhost:8000/sleep/python/", num_tries)

    # Fetch the URL that blocks with a `pg_sleep`
    t1 = time_fetch_urls("http://localhost:8000/sleep/postgres/", num_tries)

    print("------------------------------------------")
    print("SUM TOTAL = %.2fs" % (t0 + t1))
