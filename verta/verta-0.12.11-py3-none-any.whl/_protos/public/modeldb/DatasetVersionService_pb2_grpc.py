# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from ...public.modeldb import CommonService_pb2 as protos_dot_public_dot_modeldb_dot_CommonService__pb2
from ...public.modeldb import DatasetVersionService_pb2 as protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2


class DatasetVersionServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.createDatasetVersion = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/createDatasetVersion',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.CreateDatasetVersion.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.CreateDatasetVersion.Response.FromString,
        )
    self.getAllDatasetVersionsByDatasetId = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/getAllDatasetVersionsByDatasetId',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetAllDatasetVersionsByDatasetId.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetAllDatasetVersionsByDatasetId.Response.FromString,
        )
    self.deleteDatasetVersion = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/deleteDatasetVersion',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersion.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersion.Response.FromString,
        )
    self.deleteDatasetVersions = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/deleteDatasetVersions',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersions.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersions.Response.FromString,
        )
    self.getLatestDatasetVersionByDatasetId = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/getLatestDatasetVersionByDatasetId',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetLatestDatasetVersionByDatasetId.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetLatestDatasetVersionByDatasetId.Response.FromString,
        )
    self.getDatasetVersionById = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/getDatasetVersionById',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetDatasetVersionById.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetDatasetVersionById.Response.FromString,
        )
    self.findDatasetVersions = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/findDatasetVersions',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.FindDatasetVersions.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.FindDatasetVersions.Response.FromString,
        )
    self.updateDatasetVersionDescription = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/updateDatasetVersionDescription',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.UpdateDatasetVersionDescription.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.UpdateDatasetVersionDescription.Response.FromString,
        )
    self.addDatasetVersionTags = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/addDatasetVersionTags',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.AddDatasetVersionTags.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.AddDatasetVersionTags.Response.FromString,
        )
    self.getDatasetVersionTags = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/getDatasetVersionTags',
        request_serializer=protos_dot_public_dot_modeldb_dot_CommonService__pb2.GetTags.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_CommonService__pb2.GetTags.Response.FromString,
        )
    self.deleteDatasetVersionTags = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/deleteDatasetVersionTags',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersionTags.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersionTags.Response.FromString,
        )
    self.addDatasetVersionAttributes = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/addDatasetVersionAttributes',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.AddDatasetVersionAttributes.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.AddDatasetVersionAttributes.Response.FromString,
        )
    self.updateDatasetVersionAttributes = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/updateDatasetVersionAttributes',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.UpdateDatasetVersionAttributes.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.UpdateDatasetVersionAttributes.Response.FromString,
        )
    self.getDatasetVersionAttributes = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/getDatasetVersionAttributes',
        request_serializer=protos_dot_public_dot_modeldb_dot_CommonService__pb2.GetAttributes.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_CommonService__pb2.GetAttributes.Response.FromString,
        )
    self.deleteDatasetVersionAttributes = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/deleteDatasetVersionAttributes',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersionAttributes.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersionAttributes.Response.FromString,
        )
    self.setDatasetVersionVisibility = channel.unary_unary(
        '/com.mitdbg.modeldb.DatasetVersionService/setDatasetVersionVisibility',
        request_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.SetDatasetVersionVisibilty.SerializeToString,
        response_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.SetDatasetVersionVisibilty.Response.FromString,
        )


class DatasetVersionServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def createDatasetVersion(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getAllDatasetVersionsByDatasetId(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def deleteDatasetVersion(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def deleteDatasetVersions(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getLatestDatasetVersionByDatasetId(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getDatasetVersionById(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def findDatasetVersions(self, request, context):
    """queries
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def updateDatasetVersionDescription(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def addDatasetVersionTags(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getDatasetVersionTags(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def deleteDatasetVersionTags(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def addDatasetVersionAttributes(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def updateDatasetVersionAttributes(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getDatasetVersionAttributes(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def deleteDatasetVersionAttributes(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def setDatasetVersionVisibility(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DatasetVersionServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'createDatasetVersion': grpc.unary_unary_rpc_method_handler(
          servicer.createDatasetVersion,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.CreateDatasetVersion.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.CreateDatasetVersion.Response.SerializeToString,
      ),
      'getAllDatasetVersionsByDatasetId': grpc.unary_unary_rpc_method_handler(
          servicer.getAllDatasetVersionsByDatasetId,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetAllDatasetVersionsByDatasetId.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetAllDatasetVersionsByDatasetId.Response.SerializeToString,
      ),
      'deleteDatasetVersion': grpc.unary_unary_rpc_method_handler(
          servicer.deleteDatasetVersion,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersion.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersion.Response.SerializeToString,
      ),
      'deleteDatasetVersions': grpc.unary_unary_rpc_method_handler(
          servicer.deleteDatasetVersions,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersions.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersions.Response.SerializeToString,
      ),
      'getLatestDatasetVersionByDatasetId': grpc.unary_unary_rpc_method_handler(
          servicer.getLatestDatasetVersionByDatasetId,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetLatestDatasetVersionByDatasetId.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetLatestDatasetVersionByDatasetId.Response.SerializeToString,
      ),
      'getDatasetVersionById': grpc.unary_unary_rpc_method_handler(
          servicer.getDatasetVersionById,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetDatasetVersionById.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.GetDatasetVersionById.Response.SerializeToString,
      ),
      'findDatasetVersions': grpc.unary_unary_rpc_method_handler(
          servicer.findDatasetVersions,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.FindDatasetVersions.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.FindDatasetVersions.Response.SerializeToString,
      ),
      'updateDatasetVersionDescription': grpc.unary_unary_rpc_method_handler(
          servicer.updateDatasetVersionDescription,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.UpdateDatasetVersionDescription.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.UpdateDatasetVersionDescription.Response.SerializeToString,
      ),
      'addDatasetVersionTags': grpc.unary_unary_rpc_method_handler(
          servicer.addDatasetVersionTags,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.AddDatasetVersionTags.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.AddDatasetVersionTags.Response.SerializeToString,
      ),
      'getDatasetVersionTags': grpc.unary_unary_rpc_method_handler(
          servicer.getDatasetVersionTags,
          request_deserializer=protos_dot_public_dot_modeldb_dot_CommonService__pb2.GetTags.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_CommonService__pb2.GetTags.Response.SerializeToString,
      ),
      'deleteDatasetVersionTags': grpc.unary_unary_rpc_method_handler(
          servicer.deleteDatasetVersionTags,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersionTags.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersionTags.Response.SerializeToString,
      ),
      'addDatasetVersionAttributes': grpc.unary_unary_rpc_method_handler(
          servicer.addDatasetVersionAttributes,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.AddDatasetVersionAttributes.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.AddDatasetVersionAttributes.Response.SerializeToString,
      ),
      'updateDatasetVersionAttributes': grpc.unary_unary_rpc_method_handler(
          servicer.updateDatasetVersionAttributes,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.UpdateDatasetVersionAttributes.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.UpdateDatasetVersionAttributes.Response.SerializeToString,
      ),
      'getDatasetVersionAttributes': grpc.unary_unary_rpc_method_handler(
          servicer.getDatasetVersionAttributes,
          request_deserializer=protos_dot_public_dot_modeldb_dot_CommonService__pb2.GetAttributes.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_CommonService__pb2.GetAttributes.Response.SerializeToString,
      ),
      'deleteDatasetVersionAttributes': grpc.unary_unary_rpc_method_handler(
          servicer.deleteDatasetVersionAttributes,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersionAttributes.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.DeleteDatasetVersionAttributes.Response.SerializeToString,
      ),
      'setDatasetVersionVisibility': grpc.unary_unary_rpc_method_handler(
          servicer.setDatasetVersionVisibility,
          request_deserializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.SetDatasetVersionVisibilty.FromString,
          response_serializer=protos_dot_public_dot_modeldb_dot_DatasetVersionService__pb2.SetDatasetVersionVisibilty.Response.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'com.mitdbg.modeldb.DatasetVersionService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
