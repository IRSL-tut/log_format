# log_plotter

### Install

```
python3 -m pip install -r requirements.txt
```


### under any ROS workspace

```
git clone https://github.com/kindsenior/log_plotter.git
catkin build log_plotter
```

### check install

```
which datalogger_plotter_with_pyqtgraph.py
```

```
datalogger_plotter_with_pyqtgraph.py --start 8700 --length 3300 -f mc-control-BaselineWalkingController-2024-03-13-18-36-53 --plot config/mc_rtc_plot.yaml --layout config/chidori_zmp_layout.yaml
```

# Convert mc-rtc log to hrpsys log

```
python3 mc_rtc_log_conv.py -f path-to-log.bin
```
