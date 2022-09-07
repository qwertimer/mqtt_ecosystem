import time
import random
import paho.mqtt.client as mqtt
from mqtt_secrets import secrets

def get_rand(x=100):
    """
    Random number generator
    :param: x: optional item to change range of random numbers
    :returns: int: random number
    """
    rand_no = random.randint(1, x)
    return(rand_no)

def start_client(mqtt_server):
    mqtt_c = mqtt.Client()
    mqtt_c.username_pw_set(secrets["user"], password=secrets["pass"])
    mqtt_c.connect(mqtt_server, 1883, 60)
    return mqtt_c
def publish(topic, msg, client):
    msg = str(msg)
    client.publish(topic, msg)
    print(f"published {msg}")



def main():
    mqtt_server = secrets["broker"]
    mqtt_c = start_client(mqtt_server)
    mqtt_c.loop_start()
    topic = "random_num"
    while(True):
        rand_no = get_rand()
        rand_time = random.randint(1,30)
        time.sleep(rand_time)
        publish(topic, rand_no, mqtt_c)

if __name__=="__main__":
    main()
