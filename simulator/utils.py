import time
import requests
from deepdiff import DeepDiff


def request_dump(req):
    try:
        # Module requests
        url = req.url
    except AttributeError:
        # Django
        url = req.build_absolute_uri()
    return ('HTTP/1.1 {method} {url}\n{headers}\n\n{body}'.format(
        method=req.method,
        url=url,
        headers='\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        body=req.body,
    ))


def response_dump(res):
    return ('HTTP/1.1 {status_code}\n{headers}\n\n{body}'.format(
        status_code=res.status_code,
        headers='\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
        body=res.text if res.text else res.content,
    ))


def do_request(method, url, payload=None, headers=None, data=None, debug=False, raw_result=False):
    verify = False
    timeout = 30
    req = requests.Request(method, url, params=payload, headers=headers, json=data)
    prepared = req.prepare()
    if debug:
        request_src = request_dump(prepared)
        print("\nREQUEST:\n{}\n".format(request_src))
    session = requests.Session()

    response = session.send(prepared, verify=verify, timeout=timeout)

    if debug:
        response_src = response_dump(response)
        print("\nRESPONSE:\n{}\n".format(response_src))

    if raw_result:
        return response.status_code, response.content

    try:
        response_json = response.json()
    except Exception:
        response_json = {}

    return response.status_code, response_json


def do_post(url, payload=None, headers=None, data=None):
    return do_request(url, payload, headers, data)


def do_get(url, payload=None, headers=None):
    return do_request(url, payload, headers)


def get_unix_time_stamp():
    return int(time.time())


def compare_dict(dict1, dict2, debug=False):
    if not (isinstance(dict1, dict) and isinstance(dict2, dict)):

        return False

    result = DeepDiff(dict1, dict2)
    if debug or result:
        print(">>>> DIFF", result)

    return False if result else True
