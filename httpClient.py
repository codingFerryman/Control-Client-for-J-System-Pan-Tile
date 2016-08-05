import http.client
import xml.etree.ElementTree as Etree
from time import sleep
import sys

table = [209, 213]
prefix = "10.1.203."
ip = [prefix+str(ip) for ip in table]

index = []
for i in range(len(ip)):
    index.append(i)

p_initial_value = 180
t_initial_value = -12
initial_value = 0
ppv = [p_initial_value]*len(ip)
ptv = [t_initial_value]*len(ip)
conn = [initial_value]*len(ip)


j = 0
for ip in ip:
    conn[j] = http.client.HTTPConnection(ip)
    j += 1

for i in index:
    conn[i].request("GET", "/PresetsList.xml?Action=G&Row=0")
    r = conn[i].getresponse()
sleep(3)


j = 0
while True:
    for ip in ip:
        try:
            while True:
                next_line = sys.stdin.readline()
                if not next_line:
                    break
                print(next_line)
            conn[j].request("GET", "/CP_Update.xml" + next_line)
            r = conn[j].getresponse()
            data = r.read()
            treeRoot = Etree.fromstring(data)
            ppv[j] = float(treeRoot.find('PanPos').text)
            ptv[j] = float(treeRoot.find('TiltPos').text)
        except Etree.ParseError as ParseError:
            sys.stderr.write("Parse Error Occured! Please wait...\r\n")
            sys.stderr.flush()
            sleep(2)
            pass
        except:
            sys.stderr.write("Unexpected error:", sys.exc_info()[0])
            sys.stderr.flush()
            raise
        if j < len(ip):
            j += 1
        else:
            j = 0
    print(ppv, "++", ptv)
    sys.stdout.flush()
#    sleep(0.05)




    


