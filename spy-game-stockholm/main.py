from gps_class import GPSVis

vis = GPSVis(
    data_path=5,                                    # <--- data file with GSM positions (change only this row)
    locations="data-locations.csv",                 # restaurants and residences
    map_path="data-map.png",                        # Map downloaded from OSM (https://www.openstreetmap.org/export)
    points=(59.3700, 17.9900, 59.3100, 18.0900)     # Two coordinates of the map (upper left, lower right)
)

vis.create_image(color=(0, 0, 255), width=5)  # Set the color and the width of the GNSS tracks.
vis.plot_map(output='save')

# print()
