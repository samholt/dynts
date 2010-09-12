from datetime import datetime, date

from dynts.utils.anyjson import json

EPOCH = 1970
_EPOCH_ORD = date(EPOCH, 1, 1).toordinal()


class JsonPlotBase(object):
    
    def tojson(self):
        raise NotImplementedError('Cannot serialize object to JSON string')
    

class MultiPlot(object):
    
    def __init__(self, flot = None):
        self.plots = []
        self.add(flot)
        
    def add(self, flot):
        if isinstance(flot,Flot):
            self.plots.append(flot)
        
    def todict(self):
        return {'type': 'multiplot',
                'plots': [plot.todict() for plot in self.plots]}
    
    def tojson(self):
        return json.dumps(self.todict())
    

class Flot(object):
    
    def __init__(self, name = '', type = 'timeseries'):
        self.name   = name
        self.type   = type
        self.series = []
        
    def add(self, serie):
        if isinstance(serie,Serie):
            self.series.append(serie)
        
    def todict(self):
        od = self.__dict__.copy()
        od['series'] = [serie.todict() for serie in self.series]
        return od
    
    def tojson(self):
        m = MultiPlot(flot = self)
        return m.tojson()    


class Serie(object):
    
    def __init__(self, label = '', data = None):
        self.label = label
        if data is None:
            data = []
        self.data = data
        
    def todict(self):
        od = self.__dict__.copy()
        return od


def pydate2flot(dte):
    year, month, day, hour, minute, second = dte.timetuple()[:6]
    days = date(year, month, 1).toordinal() - _EPOCH_ORD + day - 1
    hours = days*24 + hour
    minutes = hours*60 + minute
    seconds = minutes*60 + second
    if isinstance(dte,datetime):
        return 1000*seconds + 0.001*dte.microsecond
    else:
        return 1000*seconds
