from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path.startswith('/api/dl/'):
            body = Path('.github/shellpanel-legacy-compat-tool.sh').read_bytes()
            self.send_response(200)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length)
        with open('/tmp/shellpanel_legacy_compat_requests.log', 'ab') as output:
            output.write(self.path.encode() + b' ' + body + b'\n')
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')

HTTPServer(('127.0.0.1', 18080), Handler).serve_forever()
