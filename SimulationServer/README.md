# Simulation Server

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
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=10>10 Bit Car ID (0-1023)</td>
            <td colspan=6>6 Bit Other stuff</td>
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
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=10>10 Bit Currently Selected Car ID (0-1023)</td>
            <td colspan=10>10 Bit for warning data</td>
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
            <td colspan=10>10 Bit Currently Selected Car ID (0-1023)</td>
            <td colspan=6>6 Bit Current Brake Pressure (0-63)</td>
        </tr>
    </tbody>
</table>
