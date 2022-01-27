"""
simulate.py for simulating BT trilateration data
Wilson McDade
"""

from models import ESP,UE
import time
import json
from paho.mqtt import client as mqtt_client
from argparse import ArgumentParser

def connect_mqtt(broker,port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected")
        else:
            print("Error connecting to mqtt broker")

    client = mqtt_client.Client("yeet")
    client.on_connect = on_connect
    client.connect(broker,port)
    return client

def publish(client,data,outputmode):
    result = client.publish(outputmode[3],data)
    return result

def main(espnum,outputmode,uenum,timestep,simlen):
    uelist = []
    esplist = []
    
    for ue in range(1,uenum):
        uelist.append(UE("UE"+str(ue)))

    for esp in range(1,espnum):
        esplist.append(ESP("ESP"+str(esp),outputmode,espnum))

    input("Start?")

    if outputmode[0] == "json":
        jsondata = dict()
        defaulttime = 1643054030
    elif outputmode[0] == "mqtt":
        mqttclient = connect_mqtt(outputmode[1],outputmode[2])
    else:
        print("Beginning live simulation")

    elapsed = 0
    while elapsed < simlen:

        if outputmode[0] == "mqtt":
            pass
        elif outputmode[0] == "json":
            jsondata[defaulttime+elapsed] = {}
        else:
            print("\n\n Time\t\t| ID\t| UE\t| MacAddr\t\t| RSSI\t\t| Distance \t| Position")

        for ue in uelist:
            ue.update()

        for esp in esplist:
            data = esp.sniff() # espname:[{"uename", "macaddr", "rssi", "dist"}, ...]
        
            if outputmode[0] == "mqtt":
                
                result = publish(mqttclient,esp.name+": "+str(data),outputmode)
                if result[0] != 0:
                    print("Error sending data")
                else:
                    print("Sent data")

            elif outputmode[0] == "json":

                jsondata[defaulttime+elapsed][esp.name] = data

            else:

                if len(data)>0:
                    print(" {}\t| {}\t| {}\t| {}\t| {}\t| {}\t| {}".format(
                                    round(time.time(),0),
                                    esp.name,
                                    data[0]["uename"],
                                    data[0]["macaddr"],
                                    data[0]["rssi"],
                                    data[0]["dist"],
                                    data[0]["pos"]))

                    for ue in range(1,len(data)):
                        print(" \t \t \t| {}\t| {}\t| {}\t| {}\t| {}".format(
                                    data[ue]["uename"],
                                    data[ue]["macaddr"],
                                    data[ue]["rssi"],
                                    data[ue]["dist"],
                                    data[ue]["pos"]))
                else: 
                    print(" {}\t| {}\t".format(round(time.time(),0),esp.name))

        elapsed += timestep
        if outputmode[0] != "json":
            time.sleep(timestep)
            print("Live simulation ...")

    if outputmode[0] == "json":
        with open(outputmode[1],"w") as outfile:
            json.dump({
                "esps": {e.name: e.pos for e in esplist},
                "data": jsondata
            },outfile)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--esp", type=int, default=5, help="Number of sniffers")
    parser.add_argument("--ue", type=int, default=50, help="Number of user devices")
    parser.add_argument("--step", type=int, default=5, help="Time per step (secs)")
    parser.add_argument("--len", type=int, default=600, help="Number of seconds to simulate")
    parser.add_argument("--mode", type=str, default="json", help="Mode to output data in (any of json, mqtt, print)")
    parser.add_argument("--jsonpath", type=str, default="test.json", help="File path for JSON mode")
    parser.add_argument("--mqttbroker", type=str, default="localhost", help="IP for MQTT broker")
    parser.add_argument("--mqttport", type=int, default=1883, help="Port for MQTT broker")
    parser.add_argument("--mqtttopic", type=str, default="imaginerit", help="Topic for MQTT broker")
    args = parser.parse_args()

    espnum = args.esp
    uenum = args.ue
    timestep = args.step
    simlen = args.len
    if args.mode == "print":
        omode = ("print")
    elif args.mode == "json":
        omode = ("json", args.jsonpath)
    else:
        omode = ("mqtt", args.mqttbroker, args.mqttport, args.mqtttopic)

    main(espnum,omode,uenum,timestep,simlen)
