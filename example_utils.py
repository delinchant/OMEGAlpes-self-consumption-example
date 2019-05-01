#! usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
..
    Copyright 2018 G2ELab / MAGE
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
         http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import os

from omegalpes.energy.energy_nodes import EnergyNode
from omegalpes.energy.units.consumption_units import VariableConsumptionUnit, \
    FixedConsumptionUnit, \
    ShiftableConsumptionUnit
from omegalpes.energy.units.conversion_units import ElectricalToHeatConversionUnit
from omegalpes.energy.units.production_units import FixedProductionUnit, \
    VariableProductionUnit
from omegalpes.energy.units.storage_units import StorageUnit
from omegalpes.general.optimisation.elements import DynamicConstraint, ExtDynConstraint
from omegalpes.general.optimisation.model import OptimisationModel
from omegalpes.general.plots import plt, plot_node_energetic_flows
from omegalpes.general.utils import save_energy_flows
from omegalpes.general.time import TimeUnit
import pandas as pd


def convert_min_data_into_5min(data_list):
    """

    :param data_list:
    :return:
    """
    new_data_list = []
    sum_data = 0

    for i, data in enumerate(data_list):
        sum_data += data
        if (i + 1) % 5 == 0:
            mean_value = sum_data / 5
            new_data_list.append(mean_value)
            sum_data = 0

    return new_data_list


def import_PV_profile_5_min():
    """
        Import an example of PV production profile with a time step of 5 minutes

    :return: PV production profile for a 5-minutes time step [W]
    """
    PV_prod = pd.read_csv('data/PV_production.csv', sep=';')
    PV_prod_profile_5min = (1000 * PV_prod['Power(kW)']).tolist()

    return PV_prod_profile_5min


def import_clothes_washer_and_dryer_load_profiles():
    """
        Import examples of clothes washer and dryer consumption profile :
            * 1-minute time step
            * in kW

        Delete NaN values

    :return: Clothes washer and clothes dryer consumption profiles [W]
    """
    # Import data
    appliances_load = pd.read_csv('data/household_appliances_consumption.csv',
                                  sep=';')

    # Convert kW into W
    cl_wash_s = 1000 * appliances_load['Clothes washer - Regular (kW)']
    cl_dry_s = 1000 * appliances_load['Clothes dryer - Regular (kW)']

    cl_wash_load = convert_min_data_into_5min(cl_wash_s[~cl_wash_s.isnull()]
                                              .tolist())
    cl_dry_load = convert_min_data_into_5min(cl_dry_s[~cl_dry_s.isnull()]
                                             .tolist())

    return cl_wash_load, cl_dry_load


def import_domestic_hot_water_load_profile():
    """

    :return:
    """
    domestic_hot_water = pd.read_csv('data/DHW.csv', sep=';')
    dhw_load = convert_min_data_into_5min(domestic_hot_water['DHW (W)']
                                          .tolist())
    return dhw_load
