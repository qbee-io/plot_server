from datetime import datetime
import decimal
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from io import IOBase
from collections import deque
import argparse
import json

hostName = None
serverPort = None
queue_length = None


renderer_html_file = open("plotly/minimal.html", "r")
renderer_html = renderer_html_file.read()


class DataObj:
    def __init__(self,unit=None):
        self.time = deque(maxlen=queue_length)
        self.vals = deque(maxlen=queue_length)
        self.__set_state__()
        self.unit = unit

    def insert(self,val,ts=None):
        #self.time.append(datetime.now().replace(microsecond=0))
        if ts is None:
            dt = datetime.now()
        else:
            dtup = decimal.Decimal(ts).as_tuple()
            ts_len = len(dtup.digits) + dtup.exponent
            ts_calc = ts if ts_len == 10 else ts/1000
            dt = datetime.fromtimestamp(ts_calc)

        self.time.append(dt)
        self.vals.append(val)
        self.__set_state__()

    def id(self):
        return self.state

    def __set_state__(self):
        self.state = int(round(datetime.now().timestamp()*1000))

    def __str__(self) -> str:
        return str(list(zip([str(t) for t in self.time],self.vals)))

    def get_time(self):
        return [str(t) for t in self.time]

    def get_value(self):
        return list(self.vals)

    def get_unit(self):
        return self.unit

class MultiDataObj:
    def __init__(self):
        self.plots={}
        self.__set_state__()

    def insert(self,tag,value,unit=None,ts=None):
        if tag not in self.plots:
            self.plots[tag] = DataObj(unit)
            self.__set_state__()

        self.plots[tag].insert(value,ts)
        # what to do on unit change? delete values or simply change unit?

    def getPlot(self,tag):
        if tag not in self.plots:
            raise ValueError()
        else:
            plot = self.plots[tag]
            plot_dict = {
                'time': plot.get_time(),
                'value': plot.get_value(),
                'tag': tag,
                'unit': plot.get_unit()
            }
            return plot_dict

    def getTagId(self,tag):
        if tag not in self.plots:
            raise ValueError()
        else:
            return self.plots[tag].id()

    def getState(self):
        return self.state

    def __set_state__(self):
        self.state = int(round(datetime.now().timestamp()*1000))

    def __str__(self) -> str:
        return_string = str("{")
        for tag,plot in self.plots.items():
            return_string += tag + ": " + str(plot) + ", "
        return_string += "}"

        return return_string

def createImageData(tag):
    return plotDat.getPlot(tag)

class MyServer(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data_input = bytes.decode(body)
        try:
            json_input = json.loads(data_input)
            print(json_input)
            val = float(json_input['value'])
            tag = json_input['tag']
            unit = json_input.get('unit')
            ts = json_input.get('ts')
            plotDat.insert(tag, val, unit, ts)
            #print(val)
            #print(plotDat)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("path: " + self.path, "utf-8"))
            self.wfile.write(bytes("received value: " + str(val), "utf-8"))
        except Exception as e:
            print(str(e))
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("ERROR: expecting json containing value, tag and unit (optional)\n", "utf-8"))
            self.wfile.write(bytes("obtained: ", "utf-8"))
            self.wfile.write(body)


    def do_GET(self):

        print("my path: ",self.path)
        parsed = urlparse(self.path)

        path = parsed.path
        query = parse_qs(parsed.query)
        print('path:',path,'query:',query)
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
        print("called delete: ", self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("path: " + self.path, "utf-8"))

    def get_plot_id(self,query):
        try:
            tag = query['tag'][0]
            plot_id = plotDat.getTagId(tag)
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
        plots = list(plotDat.plots.keys())
        self.wfile.write(bytes(json.dumps(plots), "utf-8"))

    def render_plot(self,query):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(renderer_html, "utf-8"))
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
        state = plotDat.getState()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(str(state), "utf-8"))


    def get_plot_data(self,query):
        try:
            print("entering get plot data")
            tag = query['tag'][0]
            print("obtaining tag")
            print(tag)
            data_dict = createImageData(tag)
            print("image data created")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            #self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()

            self.wfile.write(bytes(json.dumps(data_dict),"utf-8"))
        except Exception as e:
            print(str(e))
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
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


plotDat = MultiDataObj()


class LoadFromFile (argparse.Action):
    def __call__(self, parser, namespace, values: IOBase, option_string=None):
        with values as f:
            # parse arguments in the file and store them in the target namespace
            parser.parse_args(f.read().split(), namespace)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?', default='0.0.0.0', help='default 0.0.0.0')
    parser.add_argument('--port', type=int, nargs='?',default=8080, help='port to run on (default: 8080)')
    parser.add_argument('--max-points', type=int, nargs='?', default=100, help='maximum number of data points stored per measurement (default: 100)')
    parser.add_argument('--cfg', type=open, action=LoadFromFile)
    args = parser.parse_args()
    hostName = args.host
    serverPort = args.port
    queue_length = args.max_points

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
