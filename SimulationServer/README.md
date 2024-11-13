# Simulation Server

## Running the server
This is on Linux. If you are using Windows, click [here](https://learn.microsoft.com/en-us/linux/install).

### Activate venv
```bash
source venv/bin/activate
```
### Start the valkey container
```bash
docker compose up -d
```

### Start Flask server
```bash
python3 app.py
```

### Open UFW
```bash
sudo ufw allow 5000/tcp
```


## Websocket formats

### Output to visualisation

<table>
    <thead>
        <tr>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=10>10 Bit Car ID (0-1023)</td>
            <td colspan=4>4 Bit Other stuff</td>
            <td colspan=1>HW2 Select</td>
            <td colspan=1>HW1 Select</td>
            <td colspan=16>First 16 bits are for position, as an int (0-65535), meassured in dm</td>
        </tr>
    </tbody>
</table>

### Output to hardware
<table>
    <thead>
        <tr>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=8>8 Bit warning data</td>
            <td colspan=12>12 Bit for recommended speed (0-4095) in dm/s</td>
            <td colspan=12>First 12 bits are for current speed, as an int (0-4095), measured in dm/s</td>
        </tr>
    </tbody>
</table>

### Input from hardware
<table>
    <thead>
        <tr>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
            <th>0</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=1>Incr Car ID</td>
            <td colspan=1>Decr Car ID</td>
            <td colspan=6>6 Bit Other Stuff</td>
            <td colspan=8>8 Bit Current Brake Pressure (0-255)</td>
        </tr>
    </tbody>
</table>
