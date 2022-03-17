import sys
import json
import argparse
import requests


def handle_get_request(URL, output, **kwargs):
    print("GET request")
    r = requests.get(URL, stream=True)

    if output:
        with open(output, 'w') as f:
            f.write(r.text)

    return r


def handle_post_request(URL, payload, **kwargs):
    print("POST request")
    return requests.post(URL, json=payload)


REQUEST_TYPES = {'GET': handle_get_request, 'POST': handle_post_request}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="URL to send request to")
    parser.add_argument("-X", "--request", default="GET", choices=REQUEST_TYPES.keys(),
                        help="Specifies a custom request method to use when communicating with the HTTP server (defaults to GET).")
    parser.add_argument(
        "-d", "--data", type=json.loads, help="Sends the specified data in a POST request to the HTTP server")
    parser.add_argument(
        "-o", "--output", help="Write output to <file> instead of stdout")
    args = parser.parse_args()

    if args.request not in REQUEST_TYPES:
        sys.exit('Request type can only be GET or POST')

    URL = args.URL
    payload = args.data
    output = args.output if args.output else None
    try:
        res = REQUEST_TYPES[args.request](URL, output=output, payload=payload)
    except:
        sys.exit('Error processing request')

    print(res.text)
