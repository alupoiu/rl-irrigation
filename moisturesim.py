# flow = float(input('Flow rate (L/s): '))
# time = float(input('Time (hr): '))
# K = 1.01
# area = float(input('Area (m^2): '))
#
# ir_eff = float(input('Irrigation efficiency (%): '))
#
# depth = 2.54 * (flow / 28.3168 * time) / (K * area / 4046.86) * (ir_eff / 100)
# soil_moisture = (flow * 3600 * 0.001) * 100 / (area * depth * 0.01)
#
# print('Soil moisture: ' + str(soil_moisture))

import math
import pandas as pd

# const
psychometric_constant = 0.054
plant_albedo = 0.2
solar_constant = 1366
water_flow_rate = 18 #L/min
month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def findSoilMoisture():
    soil_moisture = (surface_area * findPrecipitation()) + (water_flow_rate * time_output) + ()

def findCropEvapotranspiration():
    crop_evapotranspiration = (findCropCoefficient() * findReferenceEvapotranspiration()) / 6
    print(crop_evapotranspiration)
    return crop_evapotranspiration

def findCropCoefficient():
    if 0 <= sim_day <= 15 :
        crop_coefficient = -0.5
    elif 15 < sim_day <= 35 :
        crop_coefficient = -1.05
    elif 35 < sim_day <= 50 :
        crop_coefficient = -0.9

    return crop_coefficient

def findReferenceEvapotranspiration():
    reference_evapotranspiration = (0.408 * findSlopeVaporPressureCurve() * (findNetRadiationAtTheCropSurface() - findSoilHeatFluxDensity()) + psychometric_constant * (900 / (findTemperature() + 273)) * findWindSpeed() * (findSaturationVaporPressure() - findActualVaporPressure())) / findSlopeVaporPressureCurve() + psychometric_constant * (1 + 0.34 * findWindSpeed())
    print(reference_evapotranspiration)
    return reference_evapotranspiration

def findSlopeVaporPressureCurve():
    slope_vapor_pressure_curve = (108742725 * math.log(10) * math.pow(10, (5 * findTemperature() - 4746) / (10 * findTemperature() + 2373))) / math.pow(10 * findTemperature() + 2373, 2)

    return slope_vapor_pressure_curve

def findNetRadiationAtTheCropSurface():
    net_radiation_at_the_crop_surface = (1-plant_albedo) * findSolarRadiation() + findNetLongWaveRadiation()

    return net_radiation_at_the_crop_surface

################################################################################
def findSolarRadiation():
    solar_radiation = solar_constant * math.cos(findZ())

    return solar_radiation

def findZ():
    x = latitude
    y = findSolarDeclinationAngle()
    Z = math.acos(math.sin(x * math.pi / 180) * math.sin(y * math.pi / 180) + math.cos(x * math.pi / 180) * math.cos(y * math.pi / 180) * math.cos(findH() * math.pi / 180))

    return Z

def findH():
    h = 15 * (hour - 12)

    return h

def findSoilHeatFluxDensity():
    soil_heat_flux_density = findTemperature() * 0.324

    return soil_heat_flux_density

def findSaturationVaporPressure():
    saturation_vapor_pressure = 6.11 * math.pow(10, 7.5 * findTemperature() / (237.3 + findTemperature())) * 0.1

    return saturation_vapor_pressure

def findActualVaporPressure():
    actual_vapor_pressure = findHumidity() * 100 * findSaturationVaporPressure() / 100

    return actual_vapor_pressure

def findSolarDeclinationAngle():
    solar_declination_angle = -23.45 * math.cos(360 / 365 * (findDaysSinceStartOfYear() + 10) * math.pi / 180)

    return solar_declination_angle

def findDaysSinceStartOfYear():
    days_since_start_of_year = 0
    for i in range(0, int(month)-1):
        days_since_start_of_year += month_days[i]
    days_since_start_of_year += int(day)

    return days_since_start_of_year

def findTimeFrame():
    if (0 <= hour < 4):
        time_frame = 0
    elif (4 <= hour < 8):
        time_frame = 1
    elif (8 <= hour < 12):
        time_frame = 2
    elif (12 <= hour < 16):
        time_frame = 3
    elif (16 <= hour < 20):
        time_frame = 4
    elif (20 <= hour < 24):
        time_frame = 5
    return time_frame

def findTemperature():
    temperature = df.iloc[findTimeFrame()].Temperature
    print(temperature)
    return temperature

def findHumidity():
    humidity = df.iloc[findTimeFrame()].Humidity
    print(humidity)
    return humidity

def findWindSpeed():
    wind_speed = df.iloc[findTimeFrame()].Wind_Speed
    print(wind_speed)
    return wind_speed

def findPrecipitation():
    precipitation = df.iloc[findTimeFrame()].Precipitation
    print(precipitation)
    return precipitation

def findNetLongWaveRadiation():
    net_long_wave_radiation = df.iloc[findTimeFrame()].Long_Wave_Radiation
    print(net_long_wave_radiation)
    return net_long_wave_radiation

#temperature.iloc[3].Temperature

latitude = 37.5
longitude = -121.5

season = int(input('Growth season (days):')) #days, 50
surface_area = int(input('Surface area (m^2):')) #m^2

hour = 18
day = int(input('Day (DD):'))
month = int(input('Month (MM):'))
year = int(input('Year (YYYY):'))

depth = 1 #m
sim_day = 0

time_output = 20 #min

df = pd.read_excel(r'C:\Users\alexa\Documents\semester_project_acsef\moisture_sim\sim_datasheet\data_' + str(month) + '_' + str(day) + '_' + str(year) + '.xlsx')


# while (total_days < season):
#     df = findDataFrame()
#
#     hour += 1
#
#     if (hour > 23)
#         hour = 0
#         day += 1
#         total_days += 1
#         if (day > month_days[month - 1]):
#             day = 1
#             month += 1
#             if (month > 12):
#                 month = 1
#                 year += 1
#
#     total_days += 1

# 3/10 - 4/28

# crop_coefficient = findCropEvapotranspiration(day)
crop_evapotranspiration = findCropEvapotranspiration()

while (day <= season):
    findSoilMoisture()

print(crop_evapotranspiration)
