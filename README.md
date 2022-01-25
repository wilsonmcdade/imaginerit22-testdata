# imaginerit22-testdata
Fake data generator for imagine rit backend/frontend teams

## How to use

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

5. Edit simulate.py to your preferred output method

This can be one of the following:

Live print
```
"print"
```

Live MQTT Stream
```
("mqtt","broker","port","topic")
```

Quicksim json output
```
("json",filename)
```

6. Run simulate.py
```
python3 simulate.py
```
