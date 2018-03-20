# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 15:25:51 2018

@author: xmlon
"""

import json
from data_prep import get_flights, get_flight_seq
from sim_init import state_init, get_eventclocktime, get_col_table

## load and prepare data
# Get prepared flights from csv or txt data file
# set file_path to the data file location in your computer
file_path = 'C:/Users/xmlon/Documents/ceair_simulation/flights3.txt'
flights = get_flights(file_path)

flights_ID = flights.航班日期 + flights.航班号 + flights.起飞场

airplanes_info = get_flight_seq(flights)
airplanes_ID = airplanes_info['airplanes_ID']
del airplanes_info # delete airplanes_info

## Simulation (X,E,f,Gamma,x_0,V)
#
# X: state
# (state_flights, state_airplanes)
#
# E: event
# (event_ID, event_Type)
# from_flights: depart/arrive,
# from_airplanes: maintenance, mechanical problems,
# from_weather: heavy rain, frog, heavy snow,...
# from_air_control: 
# from_airport_control:
# from_other:
#
# f: state transition rules
# according to flights sequence plan 
# according to schedule policies which will be proposed by us
#
# Gamma: available events under current state (situation)
#
# x_0: initial state
#
# V: EventClockTime
# 

# initialize the state, (state_flights,state_airplanes)
state_flights, state_airplanes = state_init(flights)

# Set event_clock_time which is sorted in ascending order
event_clock_time = get_eventclocktime(flights)
N_events = len(event_clock_time)

# Calculate the col_table of html table
col_table =get_col_table(flights)


for i in range(N_events):
    flight_id = event_clock_time.flights_ID[i]
    eventType = event_clock_time['dep/arr'][i]
    eventTime = event_clock_time.event_time[i]
    # updating state_flights & state_airplanes
    indx1 = (flights_ID == flight_id)
    airplane_id = flights.原机号[indx1]# airplane_id is a Series
    airplane_id = airplane_id.iloc[0]# now it is a string
    indx2 = (airplanes_ID == airplane_id)
    if eventType == 'd':
        state_flights.flight_state[indx1] = 'flying'
        state_flights.real_dep[indx1] = eventTime
        
        state_airplanes.airplane_state[indx2] = 'flying'
        state_airplanes.flying_flight[indx2] = flight_id
        state_airplanes.waiting_airport[indx2] = ''
    else:
        state_flights.flight_state[indx1] = 'finished'
        state_flights.real_arr[indx1] = eventTime
        
        state_airplanes.airplane_state[indx2] = 'waiting'
        state_airplanes.flying_flight[indx2] = ''
        landing_airport = flights.落地场[indx1]
        landing_airport = landing_airport.iloc[0]
        state_airplanes.waiting_airport[indx2] = landing_airport

    # to be double-checked
    airplane_idx = airplanes_ID.index[indx2]
    # td_col_idx: the column index of the presenting html table
    td_col_idx = col_table[indx1]
    txt_json = {'row': str(airplane_idx[0]),
                 'col': str(td_col_idx.iloc[0]),
                 'flight_state': state_flights.flight_state[indx1].iloc[0]}
    txt_json = json.dumps(txt_json)
    print(txt_json)
    
