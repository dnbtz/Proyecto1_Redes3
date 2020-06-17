import rrdtool


def create(nombre_rrd):
    try:
        ret = rrdtool.create("RRD/" + nombre_rrd + str(".rrd"),
                             "--start", 'N',
                             "--step", '1',
                             "DS:VALUES1:COUNTER:600:U:U",
                             "RRA:AVERAGE:0.5:1:1000",
                             #RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra - num]
                             "RRA:HWPREDICT:30000:0.1:0.0035:60:3",
                             #RRA:SEASONAL:seasonal period:gamma:rra-num
                             "RRA:SEASONAL:60:0.1:2",
                             "RRA:DEVSEASONAL:60:0.1:2",
                             "RRA:DEVPREDICT:30000:4",
                             "RRA:FAILURES:30000:7:9:4")

        if ret:
            print(rrdtool.error())
        return True

    except ValueError:
        return False
