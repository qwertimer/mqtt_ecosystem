import paho.mqtt.client as mqtt
from mqtt_secrets import secrets
import time
import datetime
import pandas as pd
from typing import Optional
from rich import box
from rich.console import Console
from rich.table import Table
from rich.live import Live
import os

TOPICS = ["mean_1", "mean_5", "mean_30"]

df_1 = pd.DataFrame(columns = ['time', 'mean_1'])
df_5 = pd.DataFrame(columns = ['time', 'mean_5'])
df_30 = pd.DataFrame(columns = ['time', 'mean_30'])
client = mqtt.Client("mean_plotter")
console = Console()

def on_message(client, userdata, message):
    """ message recieve callback :param: client: paho mqtt client :param: userdata:
    :param message: message recieved from MQTT broker

    """
    global df_1, df_5, df_30
    msg = str(message.payload.decode("utf-8"))
    msg_in = (msg)
    t = datetime.datetime.now()
    if message.topic == TOPICS[0]:
        df_1 = df_1.append(pd.Series([t, msg_in], index = ['time', 'mean_1']), ignore_index = True)

    elif message.topic == TOPICS[1]:
        df_5 = df_5.append(pd.Series([t, msg_in], index = ['time', 'mean_5']), ignore_index = True)
    if  message.topic == TOPICS[2]:
        df_30 = df_30.append(pd.Series([t, msg_in], index = ['time', 'mean_30']), ignore_index = True)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    for topic in TOPICS:
        client.subscribe(topic)
    #client.subscribe(TOPICS)

def df_to_table(
    pandas_dataframe: pd.DataFrame,
    rich_table: Table,
    show_index: bool = True,
    index_name: Optional[str] = None,
) -> Table:
    """Convert a pandas.DataFrame obj into a rich.Table obj.  
    Taken from https://gist.github.com/neelabalan/33ab34cf65b43e305c3f12ec6db05938
    Args:
        pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
        rich_table (Table): A rich Table that should be populated by the DataFrame values.
        show_index (bool): Add a column with a row count to the table. Defaults to True.
        index_name (str, optional): The column name to give to the index column. Defaults to None, showing no value.
    Returns:
        Table: The rich Table instance passed, populated with the DataFrame values."""

    if show_index:
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in pandas_dataframe.columns:
        rich_table.add_column(str(column))

    for index, value_list in enumerate(pandas_dataframe.values.tolist()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list]
        rich_table.add_row(*row)

    return rich_table

def main():
    
    mqttBroker = secrets["broker"]

    client.username_pw_set(secrets["user"], password=secrets["pass"])
    client.on_connect = on_connect
    client.on_message=on_message
    client.connect(mqttBroker,secrets["port"], 1000)
    count = 1
    global df_1, df_5, df_30 

    while(1):

        client.loop_start()
        if not df_1.empty:
            count += 1
            table = Table(show_header=True, header_style="bold magenta")
            table = df_to_table(df_1, table)
            table.row_styles = ["none", "dim"]
            table.box = box.SIMPLE_HEAD
            table1 = Table(show_header=True, header_style="bold magenta")
            table1 = df_to_table(df_5, table1)
            table1.row_styles = ["none", "dim"]
            table1.box = box.SIMPLE_HEAD
            table2 = Table(show_header=True, header_style="bold magenta")
            table2 = df_to_table(df_30, table2)
            table2.row_styles = ["none", "dim"]
            table2.box = box.SIMPLE_HEAD
       
            if count%3000 == 0:
                os.system('clear')
                console.print(table)
                console.print(table1)
                console.print(table2)
                
if __name__ == "__main__":
    main()
