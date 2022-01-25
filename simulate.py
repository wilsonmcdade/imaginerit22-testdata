"""
simulate.py for simulating BT trilateration data
Wilson McDade
"""

from models import ESP,UE
import time
import json
from paho.mqtt import client as mqtt_client

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
                    print(" {}\t| {}\t".format(time.time(),esp.name))

        elapsed += timestep
        if outputmode[0] != "json":
            time.sleep(timestep)
            print("Live simulation ...")

    if outputmode[0] == "json":
        with open(outputmode[1],"w") as outfile:
            json.dump(jsondata,outfile)

if __name__ == "__main__":

    espnum = 5   # number of sniffers
    uenum = 50   # number of user devices
    timestep = 5 # sec
    simlen = 600 # sec
    outputmode = "print"#("mqtt","localhost",1883,"imaginerit") # (print), (mqtt,broker,port,topic), (json,filename)

    main(espnum,outputmode,uenum,timestep,simlen)
