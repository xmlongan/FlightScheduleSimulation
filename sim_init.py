# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 18:34:41 2018

@author: xmlon
"""
import numpy as np
import pandas as pd
from data_prep import get_flight_seq

## define the simulation system's state 
# i.e., (state_flights, state_airplanes) 
# state_flights: (flight_id, flight_state, real_dep, real_arr)
# state_airplanes: (airplane_id, airplane_state, waiting_airport,
#                   flying_flight)
# the possible values of flight_state: 'to_fly','flying','finished','cancelled'
# the possible values of airplane_state: 'waiting', 'flying', 'maintaining'
#
# flights_ID: the ID for each flight, which is determined uniquely
# and jointly by flights.航班日期 + flights.航班号 + flights.起飞场

def state_init(flights):
    flights_ID = flights.航班日期 + flights.航班号 + flights.起飞场
    N_flights = len(flights)
    #
    state_flights = pd.DataFrame({'flight_ID' : flights_ID,
                                 'flight_state' : 'to_fly',
                                 'real_dep' : '',
                                 'real_arr' : ''
                                 },index=np.arange(N_flights))
    # Notes: 某一航班可能迫降到其他机场！所以，状态后续应该扩展
    #
    airplanes_info = get_flight_seq(flights)
    airplanes_ID = airplanes_info['airplanes_ID']
    start_idx = airplanes_info['start_idx']
    N_airplanes = len(airplanes_ID)
    
    state_airplanes = pd.DataFrame({'airplane_ID' : airplanes_ID,
                                   'airplane_state' : 'waiting',
                                   'waiting_airport' : 'PVG',
                                   'flying_flight' : ''
                                    },index=np.arange(N_airplanes))
    #
    #populate the initial state_airplanes
    init_airport = [flights.起飞场[start_idx[i]] for i in range(N_airplanes)]
    state_airplanes.waiting_airport = init_airport
    
    return((state_flights,state_airplanes))

def get_eventclocktime(flights):
    # prepare the events clock time
    flights_ID = flights.航班日期 + flights.航班号 + flights.起飞场
    dep = flights.计飞
    dep_clock_time = pd.DataFrame({'flights_ID': flights_ID,
                                   'dep/arr': 'd',
                                   'event_time': dep})
    arr = flights.计到
    arr_clock_time = pd.DataFrame({'flights_ID': flights_ID,
                                   'dep/arr': 'a',
                                   'event_time': arr})
    
    event_clock_time = pd.concat([dep_clock_time,arr_clock_time])
    N_events = len(event_clock_time)
    event_clock_time.index=np.arange(N_events) # 0:N_events(N_events not included)
    # sort the event_clock_time
    event_clock_time = event_clock_time.sort_values(by='event_time',
                                                    ascending  = True)
    event_clock_time.index=np.arange(N_events)
    # rearange the index
    return(event_clock_time)

def get_col_table(flights):
    # get the column index of html table, which is used for presenting the state
    # bt: base time, the time in the first column in the presenting html table
    # dt: delta time, comparing with bt
    N_flights = len(flights)
    bt = pd.Timestamp(2018,1,16,0,0,0)
    dt = [flights.计飞[i] - bt for i in range(N_flights) ]
    col_table = [ 24*dt[i].components.days + dt[i].components.hours for i in range(N_flights)]
    col_table = pd.Series(col_table, index=np.arange(N_flights))
    
    return(col_table)