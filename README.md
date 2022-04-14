# plot_server
A lightweight http plot server written in python to visualize data locally. Storing only a fixed number of data points (100 per default) per measurement to keep the resources low.

Empty plot                 |  Selectable data
:-------------------------:|:-------------------------:
![](https://raw.githubusercontent.com/qbee-io/plot_server/main/img/empty_plot.png)  | ![](https://raw.githubusercontent.com/qbee-io/plot_server/main/img/two_plots.png)

## Quickstart
Install the package via pip
```
pip3 install http-plot-server
```

Adapt the settings in param.cfg to your needs and run

```
plot_server --cfg=param.cfg
```
or run the module as
```
python3 -m plot_server --cfg=param.cfg
```
and open your browser with the specified port, per default:
```
http://localhost:8080
```

You can also leave out the cfg flag and default values will be used.

## Command line options
* `--host`: specifies the host (default: 0.0.0.0), can be `localhost` to avoid access from outside
* `--port`: specifies the port the server runs on (default: 8080)
* `--max-points`: specifies the maximum number of data points the plot server stores per measurement (default: 100)
* `--cfg`: specifies the path to a config file containing the above command line arguments (see `misc/param.cfg`)

## How to feed data to the plot_server
You can add data points to the plot_server by a simple http POST request including the json payload

``` json
{
    "tag": "Measurement Name",
    "value": 1234,
    "unit": "W",
    "ts": 1649859909
}
```

Where `unit` and `ts` are optional. If `ts` is not provided, then the time is used at which the post request is made. If `unit` is not provided, then the plot_server simply displays "Value" on the y-axis.

An example program feeding the plot_server is included in this repository and named `misc/data_injector.py`.

A short python snippet would look like this
``` python
import requests
data = {
    "tag": "Measurement Name",
    "value": 1234,
    "unit": "W",
    "ts": 1649859909
}
url = "http://localhost:8080"
requests.post(url,json=data)

```