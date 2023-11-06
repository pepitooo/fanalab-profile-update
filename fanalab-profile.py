import argparse
import glob
import os
import sys
import xml.etree.ElementTree as ET

BASE_DD1PS4_TYPE = {'BaseType': '7', 'WheelType': '14'}
BASE_DD1_TYPE = {'BaseType': '7', 'WheelType': '14'}
BASE_DD2_TYPE = {'BaseType': '8', 'WheelType': '15'}


# BME : Podium Button Module Endurance
# APM : Advance paddle module
WHEEL_GT3_TYPE = {'SWType': '11', 'BME': 'False', 'APM': 'False'}
WHEEL_F1_V2_TYPE = {'SWType': '10', 'BME': 'False', 'APM': 'True'} 
PODIUM_HUB_TYPE = {'SWType': '12', 'BME': 'False', 'APM': 'False'} 

PEDAL_CS_V3_TYPE = {'PedalType': '3'}


def get_base_type(base: str):
    if base.lower() == 'dd1':
        return BASE_DD1_TYPE
    elif base.lower() == 'dd2':
        return BASE_DD2_TYPE
    elif base.lower() == 'dd1ps4':
        return BASE_DD1PS4_TYPE
    return BASE_DD2_TYPE


def get_wheel_type(wheel: str):
    if wheel.lower() == 'f1v2':
        return WHEEL_F1_V2_TYPE
    elif wheel.lower() == 'gt3':
        return WHEEL_GT3_TYPE
    return WHEEL_F1_V2_TYPE


def get_pedal_type(pedal):
    if pedal.lower() == 'csv3':
        return PEDAL_CS_V3_TYPE
    return PEDAL_CS_V3_TYPE


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base', dest='base_type', help='Choose your base type', type=str, 
        choices=['DD1', 'DD1PS4','DD2'], required=False, default='DD2')
        
    parser.add_argument('-w', '--wheel', dest='wheel_type', help='Choose your wheel type', type=str, 
        choices=['GT3', 'F1v2'], required=False, default='F1v2')
        
    parser.add_argument('-p', '--pedal', dest='pedal_type', help='Choose your pedal type', type=str, 
        choices=['CSV3'], required=False, default='CSV3')

    parser.add_argument('-s', '--sensibility', dest='sensibility', help='Choose your sensibility', type=int, default=1080)
    parser.add_argument('--mps', dest='mps', help='Choose multi position switch type', type=int, default=2)

    parser.add_argument('--brf', dest='brf', help='Choose your brake force', type=int, default=60)
    parser.add_argument('--bli', dest='bli', help='Choose your brake level indicator ', type=int, default=101)
    parser.add_argument('--sho', dest='sho', help='Wheel vibration motor', type=int, default=1)
    parser.add_argument("--rev_limiter", action="store_true", help='Pedal vibrate when rev too high')

    parser.add_argument("--led_race", action="store_true", help='Leds for race, fuel, lap, position')
    parser.add_argument("--led_practice", action="store_true", help='Leds for practice')

    return parser.parse_args(args)


def main(args):
    args_parsed = parse_args(args)
    base_type = get_base_type(args_parsed.base_type)    
    wheel_type = get_wheel_type(args_parsed.wheel_type)
    pedal_type = get_pedal_type(args_parsed.pedal_type)

    print(f"Base : {args_parsed.base_type}, pedal : {args_parsed.pedal_type}, wheel : {args_parsed.wheel_type}")

    dir_path = r'./profiles/original/*/*.pws'
    res = glob.glob(dir_path)
    for profile_path in res:
        try:
            profile_xml = ET.parse(profile_path)
        except ET.ParseError:
            print(f'file not valid {profile_path}')
            continue
        settings = profile_xml.getroot()

        settings.find('./Device').attrib = base_type | wheel_type | pedal_type

        settings.find('./TuningMenu/SEN').text = str(args_parsed.sensibility)
        if base_type == BASE_DD1_TYPE or base_type == BASE_DD1PS4_TYPE:
            settings.find('./TuningMenu/FF').text = str(int((int(profile_xml.find('./TuningMenu/FF').text) * 1.25)))

        settings.find('./TuningMenu/MPS').text = str(args_parsed.mps)
        settings.find('./TuningMenu/BRF').text = str(args_parsed.brf)
        settings.find('./TuningMenu/SHO').text = str(args_parsed.sho)
        settings.find('./TuningMenu/ABS').text = str(args_parsed.bli)  # BLI

        if args_parsed.sho:
            settings.find('./Vibration/SteeringWheel/RevEnabled').text = 'False'
            settings.find('./Vibration/SteeringWheel/TractionControlEnabled').text = 'True'
            settings.find('./Vibration/SteeringWheel/TractionControl').text = '10'
            settings.find('./Vibration/SteeringWheel/TractionControlThreshold').text = '250'

        if args_parsed.rev_limiter:
            settings.find('./Vibration/Throttle/RevLimiter').text = 'True'

        if args_parsed.led_practice:
            settings.find('./ThreeDigitLed/Fuel_I').text = '4'
            settings.find('./ThreeDigitLed/Position').text = '4'
            settings.find('./ThreeDigitLed/TCGraphics').text = '3'
            settings.find('./ThreeDigitLed/ABSGraphics').text = '3'
            settings.find('./ThreeDigitLed/EngineMap').text = '3'
            settings.find('./ThreeDigitLed/iBrakeBias').text = '1'

        updated_profile_path = profile_path.replace('/original', '/updated')
        os.makedirs(os.path.dirname(updated_profile_path), exist_ok=True)
        profile_xml.write(updated_profile_path)


if __name__ == '__main__':
    main(sys.argv[1:])

    