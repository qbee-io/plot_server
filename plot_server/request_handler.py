from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import logging
import json

from plot_server.data_handlers import MultiDataObj

class PlotRequestHandler(BaseHTTPRequestHandler):

    plotDat = MultiDataObj(0)
    renderer_html = str()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data_input = bytes.decode(body)
        try:
            json_input = json.loads(data_input)
            logging.info(json_input)
            val = float(json_input['value'])
            tag = json_input['tag']
            unit = json_input.get('unit')
            ts = json_input.get('ts')
            __class__.plotDat.insert(tag, val, unit, ts)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("path: " + self.path, "utf-8"))
            self.wfile.write(bytes("received value: " + str(val), "utf-8"))
        except Exception as e:
            logging.exception("ERROR")
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(
                "ERROR: expecting json containing value, tag, unit (optional) and ts (optional)\n", "utf-8"))
            self.wfile.write(bytes("obtained: ", "utf-8"))
            self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)

        path = parsed.path
        query = parse_qs(parsed.query)
        logging.info('path:' +  path + ' query:' + str(query))
        if(path == "/current_data"):
            self.get_plot_data(query)
        elif(path == "/plot_id"):
            self.get_plot_id(query)
        elif(path == "/"):
            self.render_plot(query)
        elif(path == "/available_plots"):
            self.get_available_plots()
        elif(path == "/state"):
            self.get_tag_state()
        else:
            self.default_response()

    def do_DELETE(self):
        logging.info("called delete: ", self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("path: " + self.path, "utf-8"))

    def get_plot_id(self, query):
        try:
            tag = query['tag'][0]
            plot_id = __class__.plotDat.getTagId(tag)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(str(plot_id), "utf-8"))
        except:
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("tag not provided or invalid", "utf-8"))

    def get_available_plots(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        plots = list(__class__.plotDat.plots.keys())
        self.wfile.write(bytes(json.dumps(plots), "utf-8"))

    def render_plot(self, query):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(__class__.renderer_html, "utf-8"))
        '''
        if query is not None:
            print("adding query")
            tag = query['tag'][0]
            self.wfile.write(bytes("<html>", "utf-8"))
            self.wfile.write(bytes("<script>", "utf-8"))
            self.wfile.write(bytes("document.getElementById(\"plotSelector\").value = \'" + tag + "\'", "utf-8"))
            self.wfile.write(bytes("</script>", "utf-8"))
            self.wfile.write(bytes("</html>", "utf-8"))
        '''

    def get_tag_state(self):
        state = __class__.plotDat.getState()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(str(state), "utf-8"))

    def get_plot_data(self, query):
        try:
            tag = query['tag'][0]
            data_dict = __class__.plotDat.getPlot(tag)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            #self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()

            self.wfile.write(bytes(json.dumps(data_dict), "utf-8"))
        except Exception as e:
            logging.exception("ERROR")
            #print(str(e))
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("tag not provided or invalid", "utf-8"))

    def default_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(
            bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
