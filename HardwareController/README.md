# project
Model: ESP32-C3-DevkitC-02

# Intro til ESP32
## Introduktion 
I dette projekt bruger vi ESP-IDF framework som eer HAL layer for esp32r et software development environment for ESP32. ESP32 er et overordet for en serie af mikrokontroller med forskellige specs. 

### Forskellige versioner af ESP32

Her er en tabel der viser de forskellige chips af ESP32 til at give en ide hvad forskellen er

| ESP32 Model      | CPU Kerner | RAM      | Flash    | Wi-Fi | Bluetooth | Specielle Funktioner                   |
|------------------|------------|----------|----------|-------|-----------|----------------------------------------|
| ESP32-WROOM-32   | 2 (Xtensa) | 520 KB   | Op til 4 MB | Ja   | Ja        | Standardmodellen, bredt understøttet    |
| ESP32-WROOM-32D  | 2 (Xtensa) | 520 KB   | Op til 4 MB | Ja   | Ja        | Antenne på modul, robust forbindelse    |
| ESP32-WROOM-32U  | 2 (Xtensa) | 520 KB   | Op til 4 MB | Ja   | Ja        | UFL-konnektor til ekstern antenne       |
| ESP32-WROVER     | 2 (Xtensa) | 520 KB   | Op til 16 MB | Ja | Ja       | Ekstra RAM, PSRAM                       |
| ESP32-WROVER-B   | 2 (Xtensa) | 520 KB + 4 MB PSRAM | Op til 16 MB | Ja | Ja | Støtter PSRAM til hukommelseskrævende applikationer |
| ESP32-WROVER-E   | 2 (Xtensa) | 520 KB + 8 MB PSRAM | Op til 16 MB | Ja | Ja | Øget PSRAM, egnet til komplekse applikationer |
| ESP32-S2         | 1 (Xtensa) | 320 KB   | Op til 4 MB | Ja   | Nej       | USB OTG-understøttelse, ingen BT        |
| ESP32-S3        | 2 (Xtensa) | 512 KB   | Op til 16 MB | Ja | Ja       | AI-funktioner, TensorFlow Lite support  |
| **ESP32-C3**         | 1 (RISC-V) | 400 KB   | Op til 4 MB | Ja   | Ja        | Lavt strømforbrug, RISC-V arkitektur    |
| ESP32-H2         | 1 (RISC-V) | 320 KB   | Op til 4 MB | Nej  | BLE & Zigbee | BLE og Zigbee-protokol support          |
| ESP32-PICO-D4    | 2 (Xtensa) | 520 KB   | Op til 4 MB | Ja   | Ja        | Integreret Flash & Crystal              |

Vi bruger lige nu ESP32-C3 hvilket er fint til vores projekt

### ESP-C3

![](https://docs.espressif.com/projects/esp-idf/en/v5.0/esp32c3/_images/esp32-c3-devkitc-02-v1-pinout.png)

Her er et billed af ESP32-C3-DevkitC-02 som er det board vi bruger i projektet.

**GPIO**

Dette er pins man kan bruges i koden til input og output af signaler

**ADC**

Dette er Analog Digitial converter dette er porte der kan tage input af 0-3.3v og output 0-3.3v hvor andre porte normalt er 0 eller 3.3v

**Interrupts pins**

Dette er pins som interrupts i koden så når denne pin er høj hopper koden til et bestemt sted tror det er dem der hedder TOUCH?:)

## installation 

### ESP-IDF
følg installation på esp-idf: [docs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/index.html#)

eller

Archlinux:

```bash
sudo pacman -S --needed gcc git make flex bison gperf python cmake ninja ccache dfu-util libusb
yay -S esp-idf
```
I projekt så esp-idf tools kan findes
```bash
. /opt/esp-idf/export.sh
```


---
Ubuntu
```bash

// installation af packages som skal bruges
sudo apt-get install git wget flex bison gperf python3 python3-pip python3-venv cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0

// installation 
mkdir -p ~/esp
cd ~/esp
git clone --recursive https://github.com/espressif/esp-idf.git
cd ~/esp/esp-idf
./install.sh esp32
. ./export.sh

// hvis usb ikke virker
sudo usermod -a -G dialout $USER

```

---

Windows:


download link: [download](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/windows-setup.html)


---

Vscode:

hvis man bruger vscode er der en extension som kan hjælpe. 

Exension: ESP-IDF

---


## ESP-IDF

### esp-idf tools

der et python tool som er i ESP-IDF. idf.py som bliver brugt til at configure, build, flash og monitor
̣

**set-target**
```bash
idf.py set-target esp32c3
```

bruges til at fortælle hvilken chip version der bruges

**configure**
```bash
idf.py menuconfig
```
bruges til at configuration af forskellige variabler som bruges af compiler og drivers

**build**
```bash
idf.py build
```
dette compiler alt koden outputtet af dette kan findes i /build


**flash**
```bash
idf.py -p (usb port her) flash
```

dette bruges til at få det compiled kode over på mikrokontrolleren



**monitor**
```bash
idf.py -p (usb port her) monitor 
```

dette er til at se hvad der sker over UART som er usb protocol. Dette kan bruges til at debug ved at printe variabler til UART

**help**
```bash
idf.py help
```

Der er mange flere som kommandoer som kan findes ved hjælp af denne kommando

### Standard Libs
dette er libs som er i ESP-IDF frameworks

**driver/gpio.h**
Hvis


```c
gpio_set_direction(13, GPIO_MODE_OUTPUT);
```

Dette sætte GPIO13 pin til output

```c
gpio_set_level(13, 1);
```
Dette sætte pin højt hvilket giver 3.3v

### Managede Libs
Dette er libs som ikke er i standard lib.
man kan se dem på https://components.espressif.com/

```bash
idf.py add-dependency (navnet på lib/component)
```
man kan installere dem til ens project sådan. man skal så full build igen få man kan bruge dem
