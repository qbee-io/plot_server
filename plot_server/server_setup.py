from http.server import HTTPServer
import logging
import os

from plot_server.data_handlers import MultiDataObj
from plot_server.request_handler import PlotRequestHandler
from plot_server.utils import *


def init_request_handler(queue_length, resource_file):
    PlotRequestHandler.plotDat = MultiDataObj(queue_length)

    with open(resource_file, "r") as renderer_html_file:
        PlotRequestHandler.renderer_html = renderer_html_file.read()

def run_server(hostName,serverPort):
    webServer = HTTPServer((hostName, serverPort), PlotRequestHandler)
    logging.info("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    logging.info("Server stopped.")

def main():
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

    parser = create_parser()
    args = parser.parse_args()

    abs_path = os.path.dirname(os.path.realpath(__file__))
    resource_file = os.path.join(abs_path,"plotly/minimal.html")

    init_request_handler(queue_length=args.max_points, resource_file=resource_file)
    run_server(hostName=args.host, serverPort=args.port)

#if __name__ == "__main__":
#    main()
