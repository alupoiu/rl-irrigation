import math
import pandas as pd
import matplotlib.pyplot as plt


# const
psychometric_constant = 0.054 # kPa/deg C
plant_albedo = 0.25 # 0.2-0.25 for crops
solar_constant = 1366 # W/m^2
stefan_boltzman_constant = 5.67 * math.pow(10, -8)
month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
soil_depth = 0.7 # m

# funct
def findSoilMoisture():
    soil_moisture = water_mass / soil_mass * 100
    return soil_moisture

def findWaterMass():
    water_mass = (running_time * flow_rate * 1000) + (precipitation - crop_evapotranspiration) * 1000
    return water_mass

def findEvapotranspiration(): # mm/4hr
    crop_evapotranspiration = (findCropCoefficient() * findReferenceEvapotranspiration()) / 6
    return crop_evapotranspiration

def findCropCoefficient():
    if 0 <= sim_day <= 15 :
        crop_coefficient = 0.5
    elif 15 < sim_day <= 35 :
        crop_coefficient = 1.05
    elif 35 < sim_day <= 50 :
        crop_coefficient = 0.9
    return crop_coefficient

def findReferenceEvapotranspiration(): # mm/day
    reference_evapotranspiration = (0.408 * findSlopeVaporPressureCurve() * (findNetRadiationAtTheCropSurface() - findSoilHeatFluxDensity()) + psychometric_constant * (900 / (temperature + 273)) * wind_speed * (findSaturationVaporPressure() - findActualVaporPressure())) / findSlopeVaporPressureCurve() + psychometric_constant * (1 + 0.34 * wind_speed)
    return reference_evapotranspiration

def findSlopeVaporPressureCurve(): # kPa/deg C
    slope_vapor_pressure_curve = 4098 * 0.6108 * math.exp(17.27 * temperature / (temperature + 237.3)) / math.pow(temperature + 237.3, 2)
    return slope_vapor_pressure_curve

def findNetRadiationAtTheCropSurface(): # MJ/m^2*day
    net_radiation_at_the_crop_surface = ((1 - plant_albedo) * findSolarRadiation() + (0.98 * (1.31 * math.pow(findActualVaporPressure() / (temperature + 273), 1/7) - 1) * stefan_boltzman_constant * math.pow(temperature + 273, 4))) * 3600 * 24 / 1000000
    return net_radiation_at_the_crop_surface

def findSolarRadiation(): # W/m^2
    solar_radiation = solar_constant * (math.sin(latitude * math.pi / 180) * math.sin(findSolarDeclinationAngle() * math.pi / 180) + math.cos(latitude * math.pi / 180) * math.cos(findSolarDeclinationAngle() * math.pi / 180) * math.cos(15 * (hour - 12) * math.pi / 180))
    return solar_radiation

def findSolarDeclinationAngle(): # deg
    solar_declination_angle = -23.45 * math.cos(360 / 365 * (findDaysSinceStartOfYear() + 10) * math.pi / 180)
    return solar_declination_angle

def findSoilHeatFluxDensity(): # MJ/m^2*day
    soil_heat_flux_density = temperature * 3.75 * 3600 * 24 / 1000000
    return soil_heat_flux_density

def findSaturationVaporPressure(): # kPa
    saturation_vapor_pressure = 0.611 * math.pow(10, 7.5 * temperature / (temperature + 237.3))
    return saturation_vapor_pressure

def findActualVaporPressure(): # kPa
    actual_vapor_pressure = humidity * findSaturationVaporPressure()
    return actual_vapor_pressure

def findDaysSinceStartOfYear(): # days
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

def findTemperature(): # deg C
    temperature = df.iloc[findTimeFrame()].Temperature
    return temperature

def findHumidity(): # dec
    humidity = df.iloc[findTimeFrame()].Humidity
    return humidity

def findWindSpeed(): # m/s
    wind_speed = df.iloc[findTimeFrame()].Wind_Speed
    return wind_speed

def findPrecipitation(): # mm
    precipitation = df.iloc[findTimeFrame()].Precipitation
    return precipitation


# 3/10 - 4/28 - manual inputs (commented)
# flow_rate = int(input('Irrigation flow rate (L/min): '))
# season = int(input('Growth season (days):')) #days, 50
# hour = int(input('Hour (HH): '))
# day = int(input('Day (DD): '))
# month = int(input('Month (MM): '))
# year = int(input('Year (YYYY): '))
# latitude = float(input('Latitude: '))

# automatic inputs
# L/min
flow_rate = 9
sim_day = 0
hour = 0
day = 10
month = 3
year = 2019
latitude = 37.5
# %
target_soil_moisture = 30

# depth = 1 #m

water_mass = 0
soil_mass = soil_depth * 1000000 * 1.3
soil_moisture = 0

hour_list=[]
moisture_list=[]

while (sim_day < season - 1):
    hour += 1
    if (hour > 23):
        hour = 0
        day += 1
        sim_day += 1
    if (day > month_days[month - 1]):
        day = 1
        month += 1
    if (month > 12):
        month = 1
        year += 1

    # read from datasheet
    df = pd.read_excel(r'C:\Users\alexa\Documents\semester_project_acsef\moisture_sim\sim_datasheet\data_' + str(month) + '_' + str(day) + '_' + str(year) + '.xlsx')
    temperature = findTemperature()
    humidity = findHumidity()
    wind_speed = findWindSpeed()
    precipitation = findPrecipitation()

    crop_evapotranspiration = findEvapotranspiration()
    if (crop_evapotranspiration < 0):
        crop_evapotranspiration = 0

    # determine and respond to moisture being below and above target value
    if (soil_moisture < target_soil_moisture):
        running_time = 5
    elif (soil_moisture >= target_soil_moisture):
        running_time = 0

    # add to current water content
    water_mass += findWaterMass()
    soil_moisture = findSoilMoisture()

    if (soil_moisture < 0):
        soil_moisture = 0
    if (soil_moisture > 100):
        soil_moisture = 100

    # store data
    moisture_list.append(soil_moisture)
    hour_list.append(hour)

# graph and visualize data
cts_hours=range(0,len(moisture_list))
plt.scatter(cts_hours,moisture_list)

plt.show()
