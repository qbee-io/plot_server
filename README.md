# plot_server
an http plot server written in python to visualize data locally

## How to run
Adapt the settings in param.cfg to your needs and run

```
python3 plot_server.py --cfg=param.cfg
```

You can also leave out the cfg flag and default values will be used. To run the server in background use `start_service.sh` and `stop_service.sh`. This is not (yet) a system service.