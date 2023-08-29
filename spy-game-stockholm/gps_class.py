import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


class GPSVis(object):
    """
        Class for GPS data visualization using pre-downloaded
        OpenStreetMap map in image format.
    """
    def __init__(self, data_path, locations, map_path, points):
        """
        :param data_path: Path to file containing GPS records.
        :param map_path: Path to pre-downloaded OSM map in image format.
        :param points: Upper-left, and lower-right GPS points of the map (lat1, lon1, lat2, lon2).
        """
        self.suspect_data_value = data_path
        self.data_path = "data-00" + str(data_path) + ".csv"
        self.locations = locations
        self.points = points
        self.map_path = map_path

        self.result_image = Image
        self.x_ticks = []
        self.y_ticks = []

    def plot_map(self, output='save'):
        """
        Method for plotting the map. You can choose to save it in file or to plot it.
        :param output: Type 'plot' to show the map or 'save' to save it.
        :return:
        """
        self.get_ticks()
        fig, axis1 = plt.subplots(figsize=(20, 20))
        axis1.imshow(self.result_image)
        if output == 'save':
            plt.savefig("result-map-00" + str(self.suspect_data_value))
        else:
            plt.show()

    def create_image(self, color, width=2):
        """
        Create the image that contains the original map and the GPS records.
        :param color: Color of the GPS records.
        :param width: Width of the drawn GPS records.
        :return:
        """

        data = pd.read_csv(self.data_path, names=['LATITUDE', 'LONGITUDE'], sep=',')

        self.result_image = Image.open(self.map_path, 'r')
        img_points = []
        gps_data = tuple(zip(data['LATITUDE'].values, data['LONGITUDE'].values))
        for d in gps_data:
            x1, y1 = self.scale_to_img(d, (self.result_image.size[0], self.result_image.size[1]))
            img_points.append((x1, y1))
        draw = ImageDraw.Draw(self.result_image)
        draw.line(img_points, fill=color, width=width)

        radius = 22
        d_locations = pd.read_csv(self.locations, sep=',')
        l_data = tuple(zip(d_locations['Type'].values, d_locations['Location ID'].values,
                           d_locations['Latitude'].values, d_locations['Longitude'].values))
        font = ImageFont.truetype("Arial Bold", radius)
        for d in l_data:
            fill_color = "red"
            text_color = "white"
            if d[0] == "Residence":
                fill_color = "yellow"
                text_color = "black"
            x1, y1 = self.scale_to_img((d[2], d[3]), (self.result_image.size[0], self.result_image.size[1]))
            draw.ellipse((x1 - radius, y1 - radius, x1 + radius, y1 + radius), fill=fill_color, outline="black", width=4)
            draw.text((x1, y1), d[1], font=font, fill=text_color, anchor="mm")

    def scale_to_img(self, lat_lon, h_w):
        """
        Conversion from latitude and longitude to the image pixels.
        It is used for drawing the GPS records on the map image.
        :param lat_lon: GPS record to draw (lat1, lon1).
        :param h_w: Size of the map image (w, h).
        :return: Tuple containing x and y coordinates to draw on map image.
        """
        # https://gamedev.stackexchange.com/questions/33441/how-to-convert-a-number-from-one-min-max-set-to-another-min-max-set/33445
        old = (self.points[2], self.points[0])
        new = (0, h_w[1])
        y = ((lat_lon[0] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
        old = (self.points[1], self.points[3])
        new = (0, h_w[0])
        x = ((lat_lon[1] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
        # y must be reversed because the orientation of the image in the matplotlib.
        # image - (0, 0) in upper left corner; coordinate system - (0, 0) in lower left corner
        return int(x), h_w[1] - int(y)

    def get_ticks(self):
        """
        Generates custom ticks based on the GPS coordinates of the map for the matplotlib output.
        :return:
        """
        self.x_ticks = map(
            lambda x: round(x, 4),
            np.linspace(self.points[1], self.points[3], num=7))
        y_ticks = map(
            lambda x: round(x, 4),
            np.linspace(self.points[2], self.points[0], num=8))
        # Ticks must be reversed because the orientation of the image in the matplotlib.
        # image - (0, 0) in upper left corner; coordinate system - (0, 0) in lower left corner
        self.y_ticks = sorted(y_ticks, reverse=True)
