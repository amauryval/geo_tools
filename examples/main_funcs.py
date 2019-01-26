from geotools.core import GeoTools

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource


class BokehCore(GeoTools):

    _plot = figure()

    def __init__(self):
        super().__init__()

    def _bokeh_global_params(self):
        self._plot.legend.click_policy = "hide"

    def _format_simple_feature(self, feature):
        return ColumnDataSource({
            'x': self.geometry_2_bokeh_format(feature, 'x'),
            'y': self.geometry_2_bokeh_format(feature, 'y')
        })

    def add_multi_lines(self, feature, legend, color='blue', line_width=2):
        self._plot.multi_line(xs="x", ys="y", legend=legend, line_color=color, line_width=line_width, source=self._format_simple_feature(feature))
        self._bokeh_global_params()

    def add_lines(self, features, legend, color='blue', line_width=2):
        for enum, feature in enumerate(features):
            self._plot.line(x="x", y="y", legend=f'{legend}_{enum}', line_color=color, line_width=line_width, source=self._format_simple_feature(feature))
        self._bokeh_global_params()

    def add_points(self, feature, legend, fill_color='red', size=4):
        self._plot.circle(x="x", y="y", color=fill_color, size=size, legend=legend, source=self._format_simple_feature(feature))
        self._bokeh_global_params()

    def add_polygons(self, feature, legend, fill_color='red'):
        self._plot.multi_polygons(xs="x", ys="y", legend=legend, fill_color=fill_color, source=self._format_simple_feature(feature))
        self._bokeh_global_params()


class ExamplesCore(GeoTools):

    def __init__(self):
        super().__init__()

    def run_get_intersection_nodes(self, geometry, mode):
        return self.get_intersection_nodes(geometry, mode)

    def run_convert_geometry_to_simple_linestrings(self, geometry):
        return self.convert_geometry_to_simple_linestrings(geometry)