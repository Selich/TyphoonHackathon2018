"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir


def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py

    load_one = True
    load_two = True
    load_three = True
    power_reference = 0.0
    pv_mode = PVMode.ON
    predicted_consumption = 1.1 
    max_charging = 5.0

    

    if msg.grid_status:
        if msg.bessSOC < 1 and msg.buying_price == msg.selling_price and msg.id < 7000:
            power_reference = -max_charging
            msg.mainGridPower = msg.current_load + max_charging - msg.solar_production
        elif (msg.bessSOC * 20) > (predicted_consumption * 1.5) and msg.buying_price == 8.0:
            power_reference = max_charging
            msg.mainGridPower = msg.current_load - max_charging - msg.solar_production

        
        if msg.solar_production > msg.current_load and msg.buying_price == 3.0:
            msg.mainGridPower = msg.current_load - msg.solar_production
        elif msg.solar_production > msg.current_load:
            power_reference = msg.current_load - msg.solar_production
        
    else:
        pv_mode = PVMode.OFF
        if msg.current_load < msg.solar_production and msg.bessSOC == 1:
            power_reference = max_charging
        
        if msg.current_load > (max_charging + msg.solar_production):
            load_three = False
            if msg.current_load > (max_charging + msg.solar_production):
                load_two = False

    return ResultsMessage(data_msg=msg,
                          load_one=load_one,
                          load_two=load_two,
                          load_three=load_three,
                          power_reference=power_reference,
                          pv_mode=pv_mode)


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
