from subprocess import PIPE
import subprocess
import sys
import numpy as np
from math import atan2 as arctan
from math import fabs

pos_pt = [[100, 100], [100, 700]]


def cal_deg(pt_x, pt_y, x_trace, y_trace, flag):
    deg = flag*arctan(abs(pt_y - y_trace), abs(pt_x - x_trace))
    return deg


def read_pt(output_str):
    return np.array(output_str[1:-1].split(b', ')).astype(np.float)


def ctrl_pt(p_values, t_values, x_trace, y_trace):
    url_pre = "/CP_Update.xml?"
    pcmd = [0]*len(pos_pt)
    tcmd = [0]*len(pos_pt)
    for coordinate in pos_pt:
        flag = 0
        index = 0
        if coordinate[0] < x_trace:
            flag = 1
        if coordinate[0] > x_trace:
            flag = -1
        degree = cal_deg(pos_pt[index][0], pos_pt[index][1], x_trace, y_trace, flag)
        p_degree = p_values[index] + degree
        pcmd[index] = flag * 30
        url = url_pre + "PCmd=" + str(pcmd[index]) + "&" + "TCmd=" + str(tcmd[index])
        conn_proc.stdin.write(bytes(url, 'utf-8'))
        print(url)


print('Python %s on %s' % (sys.version, sys.platform))

conn_proc = subprocess.Popen(["py", "-3.4", "httpClient.py"],
                             stdin=PIPE,
                             stdout=PIPE,
                             stderr=PIPE)

trace_proc = subprocess.Popen(["py", "-3.4", "mouseTracer.py"],
                              stdout=PIPE,
                              stderr=PIPE)

while True:
    output_pt = conn_proc.stdout.readline().rstrip()
    output_trace = trace_proc.stdout.readline().rstrip()
    tmp_pt = output_pt.rstrip().split(b" ++ ")
    # The default range of x is [0, 799] and which is [0, 601] for y
    tmp_trace = output_trace.rstrip().split()
    trace_x = float(tmp_trace[0])
    trace_y = float(tmp_trace[1])
    pv = read_pt(tmp_pt[0])
    tv = read_pt(tmp_pt[1])
    print(pv, tv, trace_x, trace_y)
    ctrl_pt(pv, tv, trace_x, trace_y)
   # str2ctrl = output_pt + b'++' + output_trace
#    ctrl_proc.stdin.write(pv. tv, trace_x, trace_y)







