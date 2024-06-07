@echo off

rd /Q /S .\EqualizingNodeBurden\analysis\UNIFORM\
rd /Q /S .\EqualizingNodeBurden\analysis\EXPONENTIAL_DECAYING\
rd /Q /S .\EqualizingNodeBurden_Hierachically\analysis\UNIFORM\
rd /Q /S .\EqualizingNodeBurden_Hierachically\analysis\EXPONENTIAL_DECAYING\
rd /Q /S .\KademliaXOR\analysis\UNIFORM\
rd /Q /S .\KademliaXOR\analysis\EXPONENTIAL_DECAYING\

py run_simulator.py
