#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
from mqtt_secrets import secrets
from copy import copy
import datetime
import pandas as pd
import numpy as np
topic = "random_num"
msg_in = ""
df = pd.DataFrame(columns = ['time', 'msg'])
client = mqtt.Client("sys")
mean_1 = 0
mean_5 = 0
mean_30 = 0

def on_message(client, userdata, message):
    """
    message recieve callback
    :param: client: paho mqtt client
    :param: userdata:
    :param message: message recieved from MQTT broker

    """
    global df
    msg = str(message.payload.decode("utf-8"))
    msg_in = int(msg)
    t = datetime.datetime.now()
    df = df.append(pd.Series([t, msg_in], index = ['time', 'msg']), ignore_index = True)



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def pub_freq_stats(time_int, df):
    t = datetime.datetime.now()
    dt = t - datetime.timedelta(minutes=time_int)
    data_mean = run_stats(df, dt, t, time_int)
    return data_mean
   


def run_stats(df, dt, t, time_int):
    #print(df)
    filtereddf = df[(df['time'] > dt) & (df['time'] < t)]
    res = filtereddf["msg"].mean()
    #print(f"{time_int = }, {res = }")
    return res
   
def pub(topic, msg):
    topic = f"mean_{topic}"
    msg = str(msg)
    print(f"Publishing -- {topic = }, {msg = }")
    client.publish(topic, msg)

def pub_stats(df):
    global mean_1, mean_5, mean_30
    time_intervals = [1, 5, 30]
    for time_int in time_intervals:
        #print(time_int)
        data_mean = pub_freq_stats(time_int, df)
        if time_int == 1:
            if data_mean == mean_1:
               continue 
            else:
               mean_1 = data_mean
        if time_int == 5:
            if data_mean == mean_5:
                continue
            else:
               mean_5 = data_mean
        if time_int == 30:
            if data_mean == mean_30:
                continue
            else:
               mean_30 = data_mean
        pub(time_int, data_mean)


def main():
    
    mqttBroker = secrets["broker"]

    client.username_pw_set(secrets["user"], password=secrets["pass"])
    client.on_connect = on_connect
    client.on_message=on_message
    client.connect(mqttBroker,secrets["port"], 1000)
    

    while(1):

        client.loop_start()
        if not df.empty:
            pub_stats(df)



if __name__=="__main__":
    main()
