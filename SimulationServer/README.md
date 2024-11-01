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
            <td colspan=8>8 Bit Car ID (0-255)</td>
            <td colspan=8>8 Bit Other stuff</td>
            <td colspan=16>First 16 bits are for position, as an int (0-65535)</td>
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
            <td colspan=8>8 Bit Currently Selected Car ID (0-255)</td>
            <td colspan=12>12 Bit for warning data</td>
            <td colspan=12>First 12 bits are for current speed, as an int (0-4095)</td>
        </tr>
    </tbody>
</table>
