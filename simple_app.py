from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

def application(environ, start_response):
    method = environ.get("REQUEST_METHOD")
    if method == "GET":
        query_string = environ.get("QUERY_STRING", "")
        params = parse_qs(query_string)
        response = f"GET parameters: {params}"
    elif method == "POST":
        try:
            request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        except:
            request_body_size = 0
        
        request_body = environ["wsgi.input"].read(request_body_size)
        params = parse_qs(request_body.decode("utf-8"))
        response = f"POST parameters: {params}"
    else:
        response = f"Only GET and POST"
    
    status = "200 OK"
    response_headers = [("Content-type", "text/plain; charset=utf-8")]
    start_response(status, response_headers)
    
    return [response.encode("utf-8")]

if __name__ == "__main__":
    server = make_server("localhost", 8001, application)
    server.serve_forever()
    
# curl -X POST -d "param1=value1&param2=value2" http://localhost:8001