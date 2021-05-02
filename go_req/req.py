from ctypes import *
ROOT_PATH = "/Users/jitendra/moengage/python-go/go_http/"
FILE_NAME = "go_http_req.so"
http_lib = cdll.LoadLibrary(ROOT_PATH+FILE_NAME)

# define class GoSlice to map to:
# C type struct { void *data; GoInt len; GoInt cap; }
class GoSlice(Structure):
    _fields_ = [("data", POINTER(c_void_p)), ("len", c_longlong), ("cap", c_longlong)]


# define class GoString to map:
# C type struct { const char *p; GoInt n; }
class GoString(Structure):
    _fields_ = [("p", c_char_p), ("m", c_longlong)]


class GoStringSlice(Structure):
    _fields_ = [("data", POINTER(GoString)), ("len", c_longlong), ("cap", c_longlong)]


def _make_post_request_via_go(url, headers, request_payloads):
    n = len(request_payloads)
    go_url = GoString(url,len(url))
    payloads = GoStringSlice((GoString * n)(), n, n)
    for i in range(n):
        payloads.data[i] = GoString(request_payloads[i], len(request_payloads[i]))
    responses = GoStringSlice((GoString * n)(), n, n)
    status_codes = GoSlice((c_void_p * n)(), n, n)
    header_length = len(headers)
    header_keys = GoStringSlice((GoString * header_length)(), header_length, header_length)
    header_values = GoStringSlice((GoString * header_length)(), header_length, header_length)
    i = 0
    for key, value in headers.items():
        header_keys.data[i] = GoString(key, len(key))
        header_values.data[i] = GoString(value, len(value))
        i = i + 1
    print("==== making http request to go module ")
    http_lib.PostRequests.argtypes = [GoString, GoStringSlice, GoStringSlice, GoStringSlice, GoStringSlice, GoSlice]
    http_lib.PostRequests(go_url, payloads, header_keys, header_values, responses, status_codes)
    resp = []
    for i in range(responses.len):
        print("----------------- req start  -------------", i)
        print("status code  ", status_codes.data[i])
        print("response body  ", responses.data[i].p)
        print("---------------- req done  -------------", i)
        resp.append((status_codes.data[i], responses.data[i].p))
    return resp


def make_request(url, headers, payloads, user_ids):
    bulk_resp = _make_post_request_via_go(url, headers, payloads)
    results = []
    for i in range(len(bulk_resp)):
        status_code = bulk_resp[i][0]
        resp_body = bulk_resp[i][1]
        single_res = {'status': 'success'}

        if status_code < 0:
            single_res['status'] = 'failure'
        single_res['unique_key'] = user_ids[i]
        single_res['kwargs'] = {'data': payloads[i]}
        single_res['resp'] = resp_body
        results.append(single_res)
    return results


def test_python_make_req():
    url = "https://postman-echo.com/post"
    headers = {'Content-Type': 'application/json', 'X-Content-Type': 'X-application/json'}
    user_ids = ['Toby1', 'Toby2', 'Toby3', 'Toby4', 'Toby5']
    p1 = "{'name':'Toby1','email':'Toby1@example.com'}"
    p2 = "{'name':'Toby2','email':'Toby2@example.com'}"
    p3 = "{'name':'Toby3','email':'Toby3@example.com'}"
    p4 = "{'name':'Toby4','email':'Toby4@example.com'}"
    p5 = "{'name':'Toby5','email':'Toby5@example.com'}"

    payloads = [p1, p2, p3, p4, p5]
    results = make_request(url,headers,payloads,user_ids)

    import json
    print (" =======================output=============================== ")
    print (json.dumps(results))


test_python_make_req()
