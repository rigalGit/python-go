from go_req import req
from sample import add

def test():
    url = "https://postman-echo.com/post"
    headers = {'Content-Type': 'application/json', 'X-Content-Type': 'X-application/json'}
    user_ids = ['Toby1', 'Toby2', 'Toby3', 'Toby4', 'Toby5']
    p1 = "{'name':'Toby1','email':'Toby1@example.com'}"
    p2 = "{'name':'Toby2','email':'Toby2@example.com'}"
    p3 = "{'name':'Toby3','email':'Toby3@example.com'}"
    p4 = "{'name':'Toby4','email':'Toby4@example.com'}"
    p5 = "{'name':'Toby5','email':'Toby5@example.com'}"

    payloads = [p1, p2, p3, p4, p5]
    results = req.make_request(url,headers,payloads,user_ids)

    import json
    print (" =======================output=============================== ")
    print (json.dumps(results))

p = add.addNumers(10,20)
print p
test()
