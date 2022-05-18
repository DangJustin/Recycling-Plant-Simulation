import random

from rcplant import *


def user_sorting_function(sensors_output):
    spectrum_IR = sensors_output[1]['spectrum'] # FTIR Spectrum
    spectrum_Ra = sensors_output[2]['spectrum'] # Raman spectroscopy spectrum
    id_max_i = spectrum_IR.idxmax() # Wavelength that gives max value on IR Spectrum
    ir_max = spectrum_IR.max() # Max value on IR spectrum
    ir_mean = spectrum_IR.mean() # Mean of IR spectrum
    raman_max = spectrum_Ra.max() # Max of Raman Spectroscopy Spectrum
    higher_sum_i = spectrum_IR.loc[3600:2400].sum() # Sum of first half of IR spectrum
    lower_sum_i = spectrum_IR.loc[2400:1200].sum() # Sum of second half of IR spectrum

    if (ir_max == 0): # No Object Detected
        return {1: Plastic.Blank}

    # Group 1 HDPE, LDPE, PP
    if higher_sum_i > lower_sum_i or id_max_i in range(2800, 3600):

        if 4 * lower_sum_i > higher_sum_i:
            decision = {1: Plastic.PP}
        else:
            if raman_max > 20000:
                decision = {1: Plastic.LDPE}
            else:
                if 1.5 * spectrum_IR.loc[1400:1300].max() > ir_mean:
                    decision = {1: Plastic.LDPE}
                else:
                    decision = {1: Plastic.HDPE}


    else: # Group 2 PC, PVC, PS, PU, PET, Polyester


        if id_max_i in range(1250, 1300): # Subgroup PVC, PET, PC

            if 1.1 * spectrum_IR.loc[1800:1700].max() > ir_max:
                decision = {1: Plastic.PET}
            elif 2 * spectrum_IR.loc[1800:1700].max() > ir_max:
                decision = {1: Plastic.PC}
            else:
                decision = {1: Plastic.PVC}

        elif id_max_i in range(1430, 1600): # PS
            decision = {1: Plastic.PS}
        elif id_max_i in range(1770, 1800): # PC
            decision = {1: Plastic.PC}

        else: # Subgroup Polyester, PET, PU

            if 15 * spectrum_Ra.loc[2000:2500].max() > raman_max:
                decision = {1: Plastic.PU}
            else:
                if 6 * spectrum_Ra.loc[3000:3200].max() > raman_max:
                    decision = {1: Plastic.PET}
                else:
                    decision = {1: Plastic.Polyester}

    return decision


def main(speed, containers, sampling_frequency):
    # simulation parameters
    conveyor_length = 1000  # cm
    conveyor_width = 100  # cm
    conveyor_speed = speed  # cm per second
    num_containers = containers
    sensing_zone_location_1 = 500  # cm
    sensors_sampling_frequency = sampling_frequency  # Hz
    simulation_mode = 'testing'

    sensors = [
        Sensor.create(SpectrumType.FTIR, sensing_zone_location_1),
        Sensor.create(SpectrumType.Raman, sensing_zone_location_1)
    ]

    conveyor = Conveyor.create(conveyor_speed, conveyor_length, conveyor_width)

    simulator = RPSimulation(
        sorting_function=user_sorting_function,
        num_containers=num_containers,
        sensors=sensors,
        sampling_frequency=sensors_sampling_frequency,
        conveyor=conveyor,
        mode=simulation_mode
    )


    return simulator.total_classified


if __name__ == '__main__':
    main(10,100,1)
