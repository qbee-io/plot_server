from collections import deque
from datetime import datetime
import decimal
from dateutil.tz import tzlocal

class DataObj:
    def __init__(self, queue_length, unit=None):
        self.time = deque(maxlen=queue_length)
        self.vals = deque(maxlen=queue_length)
        self.__set_state__()
        self.unit = unit

    def insert(self, val, ts=None, unit=None):
        #self.time.append(datetime.now().replace(microsecond=0))
        if unit is not None:
            self.unit = unit
        if ts is None:
            dt = datetime.now(tzlocal())
        else:
            dtup = decimal.Decimal(ts).as_tuple()
            ts_len = len(dtup.digits) + dtup.exponent
            ts_calc = ts if ts_len == 10 else ts/1000
            dt = datetime.fromtimestamp(ts_calc, tzlocal())

        self.time.append(dt)
        self.vals.append(val)
        self.__set_state__()

    def id(self):
        return self.state

    def __set_state__(self):
        self.state = int(round(datetime.now().timestamp()*1000))

    def __str__(self) -> str:
        return str(list(zip([str(t) for t in self.time], self.vals)))

    def get_time(self):
        return [str(t) for t in self.time]

    def get_value(self):
        return list(self.vals)

    def get_unit(self):
        return self.unit


class MultiDataObj:
    def __init__(self,queue_length):
        self.plots = {}
        self.queue_length = queue_length
        self.__set_state__()

    def insert(self, tag, value, unit=None, ts=None):
        if tag not in self.plots:
            self.plots[tag] = DataObj(queue_length=self.queue_length,unit=unit)
            self.__set_state__()

        self.plots[tag].insert(val=value, ts=ts, unit=unit)
        # what to do on unit change? delete values or simply change unit?

    def getPlot(self, tag):
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

    def getTagId(self, tag):
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
        for tag, plot in self.plots.items():
            return_string += tag + ": " + str(plot) + ", "
        return_string += "}"

        return return_string
