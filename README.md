# imaginerit22-testdata
Fake data generator for imagine rit backend/frontend teams

## How to use

```
usage: simulate.py [-h] [--esp ESP] [--ue UE] [--step STEP] [--len LEN] [--mode MODE] [--jsonpath JSONPATH]
                   [--mqttbroker MQTTBROKER] [--mqttport MQTTPORT] [--mqtttopic MQTTTOPIC]

optional arguments:
  -h, --help            show this help message and exit
  --esp ESP             Number of sniffers
  --ue UE               Number of user devices
  --step STEP           Time per step (secs)
  --len LEN             Number of seconds to simulate
  --mode MODE           Mode to output data in (any of json, mqtt, print)
  --jsonpath JSONPATH   File path for JSON mode
  --mqttbroker MQTTBROKER
                        IP for MQTT broker
  --mqttport MQTTPORT   Port for MQTT broker
  --mqtttopic MQTTTOPIC
                        Topic for MQTT broker
```

1. Clone
```
git clone git@github.com:wilsonmcdade/imaginerit22-testdata.git
```

2. Create venv
```
python3 -m venv venv/
```

3. Enter venv
```
source venv/bin/activate
```

4. Install python requiremnts
```
pip3 install -r requirements.txt
```

5. Run simulate.py (with defaults)
```
python3 simulate.py
```

Run simulation sending to local mqtt broker
```
python3 simulate.py --mode mqtt --mqttbroker localhost --mqtttopic footsniffer
```
