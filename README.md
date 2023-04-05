# g36-boiler-plant-faults

[![Build Status](https://app.travis-ci.com/bbartling/g36-ahu-faults.svg?branch=develop)](https://app.travis-ci.com/bbartling/g36-boiler-plant-faults)

## This project is under development to eventually be a Pypi package for Fault Detection Diagnostics (FDD) on HVAC system datasets with the Pandas computing library. 
See also (in development) for other HVAC system types:
* [g36-ahu-faults](https://github.com/bbartling/g36-ahu-faults)
* [g36-chiller-plant-faults](https://github.com/bbartling/g36-chiller-plant-faults)

###### Note - Fault equations expect a float between 0.0 and 1.0 for a control system analog output that is typically expressed in industry HVAC controls as a percentage between 0 and 100% of command. 
Examples of a analog output could a heating valve, air damper, or fan VFD speed. For sensor input data these can be either float or integer based. Boolean on or off data for control system 
binary commands the fault equation expects an integer of 0 for Off and 1 for On.

## Reference AHU fault equations here defined by ASHRAE Guideline 36:
https://github.com/bbartling/open-fdd/tree/master/air_handling_unit/images


## License
g36-boiler-plant-faults is made available under the MIT license. Enjoy! 

## Development
You can follow the development of g36-ahu-faults on [GitHub](https://github.com/bbartling/open-fdd) via the `open-fdd` project for ASHRAE G36 Fault Detection Diagnostics.

## Contributing
To contribute to g36-boiler-plant-faults please open an issue on the [GitHub issue tracker](https://github.com/bbartling/g36-boiler-plant-faults/issues) and/or leave a Pull Request. Thanks!

## FDD Dataset Contributing
Any good anonymous HVAC FDD datasets in CSV format where lots of faults are found please contribute in a community effort:
https://github.com/bbartling/Data