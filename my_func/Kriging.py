import pandas as pd
from pykrige.ok import OrdinaryKriging


def kriging_interpolation(meteorology_data, unique_combinations, destination_folder, file_name):
    interpolated_data_list = []
    dates = meteorology_data['Date'].unique()

    for date in dates:
        current_data = meteorology_data[meteorology_data['Date'] == date]
        current_data = current_data.dropna()

        for index, point in unique_combinations.iterrows():
            Longitude_to_interpolate = point['經度']
            Latitude_to_interpolate = point['緯度']
            station_name = point['捷運站名稱']

            ok_TX01 = OrdinaryKriging(
                current_data['Longitude'],
                current_data['Latitude'],  
                current_data['TX01'],  
                variogram_model='gaussian'
                # variogram_model='linear'
                )

            z_TX01, ss_TX01 = ok_TX01.execute('grid', Longitude_to_interpolate, Latitude_to_interpolate)
            temp = z_TX01[0][0]

            if current_data['PP01'].eq(0).all():
                rain = 0
            else:
                ok_PP01 = OrdinaryKriging(
                    current_data['Longitude'], 
                    current_data['Latitude'],  
                    current_data['PP01'], 
                    variogram_model='gaussian' 
                )
                z_PP01, ss_PP01 = ok_PP01.execute('grid', Longitude_to_interpolate, Latitude_to_interpolate)
                rain = z_PP01[0][0]

            
            interpolated_data_list.append({
                'Date': date,
                'Longitude': Longitude_to_interpolate,
                'Latitude': Latitude_to_interpolate,
                'temperature': temp,
                'rainfall': rain,
                '捷運站名稱': station_name
            })

    interpolated_data = pd.DataFrame(interpolated_data_list)
    interpolated_data.loc[interpolated_data['rainfall'] < 0, 'rainfall'] = 0
    
    file_path = f"{destination_folder + file_name}"
    interpolated_data.to_csv(file_path, index=False)
