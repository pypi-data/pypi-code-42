from typing import List
from flask import abort, current_app, jsonify, make_response, request

"""
Class map:

SchemazerSchema
    SchemazerGroup
        SchemazerMethod
            SchemazerParameter
            SchemazerLimit
            SchemazerErrorGroup
                SchemazerErrorBase
            SchemazerResponse
                SchemazerResponseField
                    SchemazerResponseObjectField
"""


class SchemazerMethod(object):
    name = None
    group_name = None

    description: None
    parameters = None
    limits = None
    errors: list = None
    response = None
    methods = None

    @property
    def url(self):
        uri = f'{current_app.schemazer.config.HOST}{self.path}'

        if current_app.schemazer.config.HTTP_SCHEMA:
            uri = f'{current_app.schemazer.config.HTTP_SCHEMA}://{uri}'

        return uri

    @property
    def path(self):
        current_app.logger.info(f'/{self.group_name}.{self.name}')
        return f'/{self.group_name}.{self.name}'

    def __init__(self, **kwargs):
        self.methods = ['GET']
        self.__dict__.update(kwargs)


class SchemazerGroup(object):
    """
    SchemazerGroup of methods.
    """

    @property
    def __methods__(self) -> List[SchemazerMethod]:
        return [getattr(self, x) for x in dir(self) if not x.startswith('_')]


class SchemazerSchema:
    @property
    def __groups__(self) -> List[SchemazerGroup]:
        return [getattr(self, x) for x in dir(self) if not x.startswith('_')]


class SchemazerParameter(object):
    """
    SchemazerParameter of query of schema method
    """
    # parameter query name
    name = None
    description = None
    # type of parameter value
    type = None
    # parameter is required
    required = None
    # example parameter for documentation
    example = None
    # pattern for validate parameter value
    validator = None
    # default value set if parameter not in query
    default = None
    # func for check parameter value by available value interval
    interval = True

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'type': str(self.type.__name__),
            'required': self.required,
            'example': self.example,
            'validator': self.validator
        }


class SchemazerLimit(object):
    """
    Limits for access by user roles.
    """
    role = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class SchemazerErrorGroup:
    """
    Set attributes as SchemazerErrorBase objects. Use SchemazerErrorGroup for
    access to error
    object.
    """
    @property
    def __all__(self):
        return [getattr(self, x) for x in dir(self) if
                isinstance(getattr(self, x), SchemazerErrorBase)]


class SchemazerErrorBase(object):
    """
    Class for create error fields in SchemazerErrorGroup.
    """
    name = None
    # SchemazerErrorGroup name
    group_name = None
    description = None

    def __init__(self, group_name, name, description=None):
        self.group_name = group_name
        self.name = name
        self.description = description

    def to_dict(self) -> dict:
        return {
            'code': self.code,
            'description': self.description
        }

    @property
    def code(self) -> str:
        return f'{self.group_name}.{self.name}'

    def json_abort(self, failure_field: str=None, extend_msg: str=''):
        """
        Abort response with error object.
        :param dict failure_field: SchemazerParameter in which the error
        occurred
        :param str extend_msg: Extend message with error description.
        :return:
        """
        data = {
            'error':
                {
                    'code': self.code,
                    'msg': f'{self.description} {extend_msg}' if extend_msg
                    else self.description,
                    'failure_param': failure_field,
                    'params': request.query.args or {},
                }
        }

        return make_response(jsonify(data),
                             current_app.config.get('ERROR_HTTP_CODE'))


class SchemazerResponseField(object):
    """
    Class use for create documentation. Simple field with
    single field. For create object with many params or  list or objects use
    `SchemazerResponseObjectField`.
    """
    name = None
    type = None
    description = None
    data_example = None  # example of return data

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self) -> dict:
        return {
            self.name: {
                'type': self.type.__name__ or 'undefined',
                'description': self.description,
            }
        }

    @property
    def example(self):
        return {self.name: self.data_example}


class SchemazerResponseObjectField(object):
    """
    Class use for create documentation .
    """
    name = None
    fields = None
    is_list = False

    def __init__(self, name=None, fields: list=None, is_list=False):
        self.name = name
        self.fields = fields or list()
        self.is_list = is_list

    def to_dict(self):
        obj = {}
        for x in self.fields:
            obj.update(x.to_dict())

        if self.name:
            return {obj if not self.is_list else [obj]}
        else:
            return obj if not self.is_list else [obj]

    @property
    def example(self):
        example = {}
        for x in self.fields:
            example.update(x.example)

        if self.name:
            return {example if not self.is_list else [example]}
        else:
            return example if not self.is_list else [example]


class SchemazerResponse(object):
    schema = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return {'response': self.schema.to_dict()}

    @property
    def example(self):
        return {'response': self.schema.example}
