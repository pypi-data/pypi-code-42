from typing import *

from cognite.seismic._api.api import API
from cognite.seismic.data_classes.trace_list import Trace3DList
from cognite.seismic.protos.query_service_messages_pb2 import (
    GeometryCubeRequest,
    LineBasedRectangle,
    LineCubeRequest,
    PositionQuery,
)
from cognite.seismic.protos.types_pb2 import CRS, GeoJson, Geometry, Wkt


class VolumeAPI(API):
    def __init__(self, query, metadata):
        super().__init__(query=query, metadata=metadata)

    @staticmethod
    def _verify_input(crs: str = None, wkt: str = None, geo_json: str = None):
        if not crs:
            raise Exception("CRS is required")
        if not wkt and not geo_json:
            raise Exception("Either `wkt` or `geo_json` needs to be specified")
        if wkt and geo_json:
            raise Exception("Only `wkt` or `geo_json` should be specified")

    def get_cube_by_lines(
        self,
        file_id: Optional[str] = None,
        file_name: Optional[str] = None,
        top_left_inline=None,
        top_left_crossline=None,
        bottom_right_inline=None,
        bottom_right_crossline=None,
        include_trace_header=False,
    ):
        file = self.identify(file_id, file_name)
        top_left = PositionQuery(iline=top_left_inline, xline=top_left_crossline)
        bottom_right = PositionQuery(iline=bottom_right_inline, xline=bottom_right_crossline)
        rectangle = LineBasedRectangle(top_left=top_left, bottom_right=bottom_right)
        request = LineCubeRequest(file=file, rectangle=rectangle, include_trace_header=include_trace_header)
        return Trace3DList([i for i in self.query.GetCubeByLines(request, metadata=self.metadata)])

    def get_cube_by_geometry(
        self,
        file_id: Optional[str] = None,
        file_name: Optional[str] = None,
        crs: str = None,
        wkt: str = None,
        geo_json=None,
        include_trace_header: bool = False,
    ):
        file = self.identify(file_id, file_name)
        self._verify_input(crs, wkt, geo_json)
        geo = (
            Geometry(crs=CRS(crs=crs), wkt=Wkt(geometry=wkt))
            if wkt
            else Geometry(crs=CRS(crs=crs), geo=GeoJson(json=geo_json))
        )
        request = GeometryCubeRequest(file=file, geometry=geo, include_trace_header=include_trace_header)
        return Trace3DList([i for i in self.query.GetCubeByGeometry(request, metadata=self.metadata)])
