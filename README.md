# Prerequisites

Windows, linux, or mac with python > 3.9 installed

Have a look to this [link](https://learn.microsoft.com/en-us/windows/python/beginners) for windows

# fanalab profile update

This simple script will update fanalab profile to match your preference and hardware

From fanatec forum, it's easy to get a profile for fanalab. Usually it's done for DD2 wheelbase.
If you want to use it on a DD1, you have to calculate a ration of 1.25 for each profile. 
This script is doing it automatically.

1. Download a profile zip file (from Maurice B) usually first comment after new fanalab release
2. Extract in the folder orginal inside profiles like this :
   ```   
   profiles
   ├── original
   │   ├── ACC
   │   ├── AMS2
   │   ├── F1 2021
   │   ├── F1 22
   │   ├── iRacing
   │   └── rF2
   create_my_own_profiles.bat
   fanalab-profile.py
   README.md
    ```
3. Modify .bat file to match your needs
4. Execute .bat file
5. The sripts will have created a new folder called updated
   ```   
   profiles
   ├── original
   │   ├── ACC
   │   ├── AMS2
   │   ├── F1 2021
   │   ├── F1 22
   │   ├── iRacing
   │   └── rF2
   ├── updated
   │   ├── ACC
   │   ├── AMS2
   │   ├── F1 2021
   │   ├── F1 22
   │   ├── iRacing
   │   └── rF2
   create_my_own_profiles.bat
   fanalab-profile.py
   README.md
    ```
6. import in fanalab the profiles you want

## Tested Version

- FanaLab 1.66
- FanaLab 2.01.12 <- don't work properly 
- FanaLab 2.01.21

Make sure you download the profiles archive from the same forum thread as the FanaLab version.

## Script options

### Wheel base 

```shell
python fanalab-profile.py --base XXX
```

- Fanatec DD1 `DD1`
- Fanatec DD2 `DD2` _*default_
- Fanatec DD1 for PS4 `DD1PS4`

### Wheel base 

```shell
python fanalab-profile.py --wheel XXX
```

- Fanatec F1 v2 `F1V2` _*default_
- Fanatec McLaren GT3 `GT3`

### Pedal 

```shell
python fanalab-profile.py --pedal XXX
```

- Fanatec ClubSport V3 `CSV3` _*default_

### Sensibility

```shell
python fanalab-profile.py --sensibility XXX
```

Sensibility as integer value, ex: 640, 720, 1080

_*default_ = 1080

### Brake force (load cell configuration)

```shell
python fanalab-profile.py --bfr XXX
```

BFR as integer value, ex: 50, 60, 90

_*default_ = 60

### Brake Level Indicator (Brake pedal vibration when reach this value)

```shell
python fanalab-profile.py --bfr XXX
```

BLI as integer value, ex: 50, 60, 90

_*default_ = 101 : Disabled

### Rev limiter (Gaz pedal vibration when reach rev limit)

```shell
python fanalab-profile.py --rev_limiter
```

Activate rev limiter when defined

_*default_ : Disabled

### Wheel LED

```shell
python fanalab-profile.py --led_race
python fanalab-profile.py --led_practice
```

Activate led for race or led practice

Led practice : 

default LED + this change
      
- Disable Fuel
- Disable Position
- Enable TC change
- Enable ABS change
- Enable Engine Map change
- Enable Brake Bias change

_*default_ : led_race

# My personal preference

Here the command I run to match my preferences.
```shell
python fanalab-profile.py --base DD1PS4 --wheel GT3 --pedal CSV3 --sensibility 720 --brf 90 --bli 90 --rev_limiter --led_practice
```