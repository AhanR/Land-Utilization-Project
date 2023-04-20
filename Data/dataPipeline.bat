python dataMaker.py Vandalur_LST linear [0,211,127] [60,239,175] [200,174,120]
@REM python dataMaker.py Vandalur_LULC mapped {this:that}
python dataMaker.py Vandalur_NDVI linear [0,255,127] [60,255,127] [112,255,48]
@REM D:\College Work\Land utilization project\visualization\public\data
robocopy "D:\College Work\LandUtilizationProject\Data\Data Generated" "D:\College Work\LandUtilizationProject\visualization\public\data\ProcessedData" *.csv /mt