#!/usr/bin/python2.7
"""
Copyright (C) 2014 Reinventing Geospatial, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>,
or write to the Free Software Foundation, Inc., 59 Temple Place -
Suite 330, Boston, MA 02111-1307, USA.

Author: Jenifer Cochran, Reinventing Geospatial Inc (RGi)
Date: 2018-11-11
   Requires: sqlite3, argparse
   Optional: Python Imaging Library (PIL or Pillow)
Credits:
  MapProxy imaging functions: http://mapproxy.org
  gdal2mb on github: https://github.com/developmentseed/gdal2mb

Version:
"""


class ContentEntry(object):
    """
    Content that represents a row in the gpkg_contents table
    """

    def __init__(self,
                 table_name,
                 data_type,
                 identifier,
                 min_x,
                 min_y,
                 max_x,
                 max_y,
                 srs_id):
        """
        Constructor

        :param table_name:  The name of the tiles, feature, or extension specific content table
        :type table_name: str

        :param data_type: Type of data stored in the table: "features" per clause Features, "tiles" per clause Tiles, or
        an implementer-defined value for other data tables per clause in an Extended GeoPackage.
        :type data_type: str

        :param min_x: Bounding box minimum easting or longitude for all content
        :type min_x: float

        :param min_y: Bounding box minimum northing or latitude for all content
        :type min_y: float

        :param max_x: Bounding box maximum easting or longitude for all content
        :type max_x: float

        :param max_y: Bounding box maximum northing or latitude for all content
        :type max_y: float

        :param srs_id: Spatial Reference System (SRS) identifier (i.e. 4326)
        :type srs_id: int
        """

        self.table_name = table_name
        self.data_type = data_type
        self.identifier = identifier
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.srs_id = srs_id
