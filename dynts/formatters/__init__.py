# -*- coding: utf-8 -*-
import cStringIO
import csv

from dynts.exceptions import FormattingException

default_converter = lambda x : x.isoformat()

def tsiterator(ts, dateconverter = None):
    dateconverter = dateconverter or default_converter
    yield ['Date']+ts.names()
    for dt,value in ts.items():
        dt = dateconverter(dt)
        yield [dt]+list(value)

def tocsv(ts, filename = None, **kwargs):
    '''Returns CSV representation of a :class:`dynts.TimeSeries`.'''
    stream = cStringIO.StringIO()
    _csv = csv.writer(stream)

    for row in tsiterator(ts):
        _csv.writerow(row)

    return stream.getvalue()


def toflot(ts, **kwargs):
    pass


def toxls(ts, filename = None, title = None, raw = False, **kwargs):
    '''Dump the timeseries to an xls representation.
This function requires the python xlwt__ package.

__ http://pypi.python.org/pypi/xlwt'''
    try:
        import xlwt
    except ImportError:
        raise FormattingException('To save the timeseries as a spreadsheet, the xlwt python library is required.')
    
    
    if isinstance(filename,xlwt.Workbook):
        wb = filename
    else:
        wb = xlwt.Workbook()
    title = title or ts.name
    stream = cStringIO.StringIO()
    sheet = wb.add_sheet(title)
    for i,row in enumerate(tsiterator(ts)):
        for j,col in enumerate(row):
            sheet.write(i,j,str(col))
    
    if raw:
        return wb
    else:
        stream = cStringIO.StringIO()
        wb.save(stream)
        return stream.getvalue()
    
     