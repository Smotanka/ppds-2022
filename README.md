# 4. Assignment - dinning philosophers, nuclear power plant

_Whole assignment in slovak ([link](https://uim.fei.stuba.sk/i-ppds/4-cvicenie-vecerajuci-filozofi-atomova-elektraren-%f0%9f%8d%bd%ef%b8%8f/))_

In this assignment we continue to exploring the lightswitch synchronization events.

---
### 1. Task - dinning philosophers
Implement a solution to the synchronization problem of dinning philosophers using right-handers and left-handers so 
that the following conditions are met:

1. Only one philosopher can hold a fork at a time,
2. there must be no entrapment (i.e. any philosopher hadn't eaten ),
3. it must not happen that one of the philosophers does not eat,
4. finally, the solution must allow several philosophers to eat at the same time.


#### Solution

This synchronization problem was solved by professor Jókay at the 4th seminar (source code: [dinnigPhilosphers.py](dinningPhilosophers.py)), so we think
there is no need for deep explanation. The solution is easy to understand: there are philosophers 
that need to think, then eat. To eat they need pick up fork which they only do if the footman is watching.
We created an infinite loop, where we have on central synchronization object (footman) and for each philosopher there is 
one unique semaphore synchronization (fork). When footman signals, then the philosopher can take the fork and do eating (simulating 
code execution). When the fork is taken, others philosophers are waiting for a fork to be free. When philosopher is done 
eating he puts down the fork and waiter signals that fork is free to grab for another philosopher.

---
### 2. Task - nuclear power plant

The nuclear power plant has 11 sensors:

* two primary circuit coolant flow sensors,
* two secondary circuit coolant flow sensors,
* two primary circuit coolant temperature sensors,
* two secondary circuit coolant temperature sensors,
* three control rod insertion depth sensors.

These sensors try to update the measured values in the common data store in a constant cycle. 
In this storage, each sensor has its own space, where it updates the value that belongs to it (take into account when synchronizing). 
It takes 10 to 15 ms for each sensor to update the data (base the model of each sensor only on this feature).

In addition to the sensors, they also have two operators in that power plant, who are constantly looking at each of their monitors, 
where the measured values of the sensors are projected. However, this data must somehow get from the common sensor data storage to the monitor. 
This is done by each monitor sending a request for updated data 
in a continuous cycle every 500 ms since the last update was completed (or 500 ms since the monitor was activated). 
When the monitor requests an update of the data, this must be guaranteed within 200 ms.

However, the monitors can only start (activate) if at least one sensor has supplied data to the storage.

#### Solution

Solution to this task (source [code](nuclearPowerPlant.py) ) is deeply explained at this [link](https://uim.fei.stuba.sk/i-ppds/4-cvicenie-vecerajuci-filozofi-atomova-elektraren-%f0%9f%8d%bd%ef%b8%8f/)
We show the pseudocode that is also solution to this problem
```
def init():
    accessData = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    validData = Event()

    for monitor_id in &amp;lt;0,1&amp;gt;:
        create_and_run_thread(monitor, monitor_id)
    for cidlo_id in &amp;lt;0,10&amp;gt;:
        create_and_run_thread(cidlo, cidlo_id)

def monitor(monitor_id):
    // wait for data to be stored
    validData.wait()

    while True:
        // wait 500 ms for next actualization
        sleep(500 ms)

        // block the sensors from co-routine
        turnstile.wait()
            // get acces to storage
            monitors_read = ls_monitor(accessData).lock()
        turnstile.signal()

        // print the actualization
        print('monit "%02d": monitors_read=%02d\n')
        // data actualized, we exit the storage
        ls_monitor(accessData).unlock()

def sensor(sensor_id):
    while True:
        // Sensor are collecting data until the monitor stops them
        turnstile.wait()
        turnstile.signal()

        // get acces to storage
        sensors_read = ls_cidlo(accessData).lock()
            // accesing the storage is simulated by waiting 10 - 15 ms
            write_time = rand(10 to 15 ms)
            print('sensor "%02d":  sensors_read=%02d, write_time=%03d\n')
            sleep(write_time)
            // signalize that data are correct
            validData.signal()
        // data stored, we exit the storage
        ls_cidlo(accessData).unlock()

```
---
### 3. Task - nuclear power plant #2
_This is modification from a previous task._


The nuclear power plant has 3 sensors:

* one primary circuit coolant flow sensor (sensor P)
* one primary circuit coolant temperature sensor (T sensor)
* one control rod insertion depth sensor (sensor H)

These sensors are constantly trying to update the measured values. They store the data in a common data repository. 
Each sensor has its own dedicated space in the storage, where it stores data (take into account when synchronizing).

The sensors update every 50-60 ms. The data update itself takes 10-20 ms for the sensor P and T for the sensor T, but it takes 20-25 ms for the sensor H.

In addition to the sensors, there are eight operators in that power plant, who are constantly looking at eight monitors to see where the measured values of the sensors are displayed. 
The data update request is sent by the monitor continuously in a cycle. One update takes 40-50 ms.

Monitors can only start working if all sensors have already delivered valid data to the repository.

#### Solution
Firstly lets look at the pseudocod:

```
def init():
    accessData = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    validDataP = Event()
    validDataT = Event()
    validDataH = Event()

    for monitor_id in &amp;lt;0,1&amp;gt;:
        create_and_run_thread(monitor, monitor_id)
    for cidlo_id in &amp;lt;0,10&amp;gt;:
        create_and_run_thread(cidlo, cidlo_id)

def monitor(monitor_id):

    // wait for data to be stored
    validDataH.wait()
    validDataT.wait()
    validDataP.wait()
    
    while True:
        // wait 40-50 ms for actualization
        sleep(40-50 ms)

        // block the sensors from co-routine
        turnstile.wait()
            // get acces to storage
            monitors_read = ls_monitor(accessData).lock()
        turnstile.signal()

        // print the actualization
        print('monit "%02d": monitors_read=%02d\n')
        // data actualized, we exit the storage
        ls_monitor(accessData).unlock()

def sensor(sensor_id, sensor_type):

    while True:
        // Sensor are collecting data until the monitor stops them
        turnstile.wait()
        turnstile.signal()
        
        // Collect data every 60 seconds
        sleep(50 - 60 ms)   
        
        // get acces to storage
        sensors_read = ls_sensor(accessData).lock()
            // accesing the storage is simulated by waiting
            // Different sensor types have different wait times
            if sensor_type is SensorType.H
                write_time = randint(20, 25)
            else:
                write_time = randint(10, 20)
            print('sensor "%02d":  sensors_read=%02d, write_time=%03d\n')
            sleep(write_time)
            
            // Signalize that data are correct
            // For monitor function, that waits for all three sensor to collect data
            if sensor_type is SensorType.P:
                system_control.validDataP.signal()
            elif sensor_type is SensorType.T:
                system_control.validDataT.signal()
            else:
                system_control.validDataH.signal()
                
        // data stored, we exit the storage
        ls_sensor(accessData).unlock()

```
The source code can be found at [advancedPowerPlant](advancedPowerPlant.py), where we created Enum class for different 
sensor types, also we created a unique event for each sensor type. We added this because we needed to halt the monitoring
until all the sensor types collected data. We also added the if else clause to determine how long the sensor should 
perform the actualizing and storing the data. 

The code execution is simple: we have one central synchronization object - turnstile, which is called by the monitor 
function to block sensor from accessing the storage. Then we lock the monitors to get information on how many monitors
are in the lock method of PowerPlant class. We print the actualized info and continue in code execution. The principe
is similar with the sensors. The main think to remember is that the storage can be access only for reading or for writing.
Not both at the same time.
