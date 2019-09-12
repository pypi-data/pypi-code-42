#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import datetime
import pytest
from fixtures import *
from helpers import *
from pywr._core import Timestep, ScenarioIndex

from pywr.core import *
from pywr.domains.river import *
from pywr.parameters import Parameter, ConstantParameter, DataFrameParameter, AggregatedParameter
from pywr.recorders import assert_rec, AssertionRecorder

TEST_FOLDER = os.path.dirname(__file__)

def test_names():
    '''Test node names'''
    model = Model()

    node1 = Input(model, name='A')
    node2 = Output(model, name='B')
    assert(model.nodes['A'] is node1)
    assert(model.nodes['B'] is node2)

    nodes = sorted(model.nodes, key=lambda node: node.name)
    assert(nodes == [node1, node2])

    # rename node
    node1.name = 'C'
    assert(model.nodes['C'] is node1)
    assert('A' not in model.nodes)

    # attempt name collision (via rename)
    with pytest.raises(ValueError):
        node2.name = 'C'

    # attempt name collision (via new)
    with pytest.raises(ValueError):
        node3 = Input(model, name='C')
    assert(len(model.nodes) == 2)  # node3 not added to graph

    # attempt to create a node without a name
    with pytest.raises(TypeError):
        node4 = Input(model)


def test_model_nodes(model):
    """Test Model.nodes API"""
    node = Input(model, 'test')

    # test node by index
    assert(model.nodes['test'] is node)

    with pytest.raises(KeyError):
        model.nodes['invalid']

    # test node iterator
    all_nodes = [node for node in model.nodes]
    assert(all_nodes == [node])

    # support for item deletion
    del(model.nodes['test'])
    all_nodes = [node for node in model.nodes]
    assert(all_nodes == [])


def test_unexpected_kwarg_node():
    model = Model()

    with pytest.raises(TypeError):
        node = Node(model, 'test_node', invalid=True)
    with pytest.raises(TypeError):
        inpt = Input(model, 'test_input', invalid=True)
    with pytest.raises(TypeError):
        storage = Storage(model, 'test_storage', invalid=True)
    # none of the nodes should have been added to the model as they all
    # raised exceptions during __init__
    assert(not model.nodes)


def test_unexpected_kwarg_model():
    with pytest.raises(TypeError):
        model = Model(thisisgoingtofail=True)
    model = Model()

def test_slots_connect_disconnect():
    """Test connection and disconnection to storage node slots
    """
    model = Model()

    supply1 = Input(model, name='supply1')
    supply2 = Input(model, name='supply2')
    storage = Storage(model, name='storage', num_inputs=2, num_outputs=2)

    storage_inputs = [[x for x in storage.iter_slots(slot_name=n, is_connector=True)][0] for n in (0, 1)]
    storage_outputs = [[x for x in storage.iter_slots(slot_name=n, is_connector=False)][0] for n in (0, 1)]

    # attempt to connect to invalid slot
    # an error is raised, and no connection is made
    with pytest.raises(IndexError):
        supply1.connect(storage, to_slot=3)
    assert((supply1, storage_inputs[0]) not in model.edges())
    assert((supply1, storage_inputs[1]) not in model.edges())

    # connect node to storage slot 0
    supply1.connect(storage, to_slot=0)
    assert((supply1, storage_outputs[0]) in model.edges())
    assert((supply1, storage_inputs[1]) not in model.edges())

    # the same node can be connected to multiple slots
    # connect node to storage slot 1
    supply1.connect(storage, to_slot=1)
    assert((supply1, storage_outputs[0]) in model.edges())
    assert((supply1, storage_outputs[1]) in model.edges())

    # disconnect the node from a particular slot (recommended method)
    supply1.disconnect(storage, slot_name=0)
    assert((supply1, storage_outputs[0]) not in model.edges())
    assert((supply1, storage_outputs[1]) in model.edges())

    # disconnect the node from a particular slot (direct, not recommended)
    supply1.connect(storage, to_slot=0)
    supply1.disconnect(storage_outputs[0])
    assert((supply1, storage_outputs[0]) not in model.edges())
    assert((supply1, storage_outputs[1]) in model.edges())

    # specifying the storage in general removes the connection from all slots
    supply1.connect(storage, to_slot=0)
    supply1.disconnect(storage)
    assert((supply1, storage_outputs[0]) not in model.edges())
    assert((supply1, storage_outputs[1]) not in model.edges())

    # it's an error to attempt to disconnect if nodes aren't connected
    with pytest.raises(Exception):
        supply1.disconnect(storage)


def test_node_position():
    model = Model()

    # node position, from kwargs

    node1 = Input(model, "input", position={"schematic": (10, 20), "geographic": (-1, 52)})

    # node position, from JSON

    data = {
        "name": "output",
        "type": "output",
        "position": {
            "schematic": (30, 40),
            "geographic": (-1.5, 52.2),
        }
    }
    node2 = Node.load(data, model)

    assert(node1.position["schematic"] == (10, 20))
    assert(node1.position["geographic"] == (-1, 52))
    assert(node2.position["schematic"] == (30, 40))
    assert(node2.position["geographic"] == (-1.5, 52.2))

    node1.position["schematic"] = (50, 60)
    assert(node1.position["schematic"] == (50, 60))

    # node without position

    node3 = Node(model, "node3")
    assert(node3.position == {})

    # reservoir position, from JSON

    data = {
        "name": "reservoir",
        "type": "storage",
        "position": {
            "schematic": (99, 70),
            "geographic": (-2.5, 55.6),
        },
        "max_volume": 1000,
        "initial_volume": 500
    }

    storage = Storage.load(data, model)

    assert(storage.position["schematic"] == (99, 70))
    assert(storage.position["geographic"] == (-2.5, 55.6))


test_data = ["timeseries1.xlsx", os.path.join("models", "timeseries1.csv")]
@pytest.mark.parametrize("filename", test_data)
def test_timeseries_excel(simple_linear_model, filename):
    """Test creation of a DataFrameParameter from external data (e.g. CSV)"""
    model = simple_linear_model

    # create DataFrameParameter from external data
    filename = os.path.join(TEST_FOLDER, filename)
    data = {"url": filename, "column": "Data", "index_col": "Timestamp"}
    if filename.endswith(".csv"):
        data.update({"parse_dates": True, "dayfirst":True})
    ts = DataFrameParameter.load(model, data)

    # model (intentionally not aligned)
    model.timestepper.start = ts.dataframe.index[0] + 5
    model.timestepper.end = ts.dataframe.index[-1] - 12

    # need to assign parameter for it's setup method to be called
    model.nodes["Input"].max_flow = ts

    @assert_rec(model, ts)
    def expected(timestep, scenario_index):
        return ts.dataframe.loc[timestep.datetime]

    model.run()

def test_dirty_model():
    """Test that the LP is updated when the model structure is redefined"""
    # start dirty
    model = Model()
    assert(model.dirty)

    # add some nodes, still dirty
    supply1 = Input(model, 'supply1')
    demand1 = Output(model, 'demand1')
    supply1.connect(demand1)
    assert(model.dirty)

    # run the model, clean
    result = model.step()
    assert(not model.dirty)

    # add a new node, dirty
    supply2 = Input(model, 'supply2')

    # run the model, clean
    result = model.step()
    assert(not model.dirty)

    # add a new connection, dirty
    supply2.connect(demand1)
    assert(model.dirty)

    # run the model, clean
    result = model.step()
    assert(not model.dirty)

    # remove a connection, dirty
    supply2.disconnect()
    assert(model.dirty)

def test_reset_initial_volume():
    """
    If the model doesn't reset correctly changing the initial volume and
    re-running will cause an exception.
    """
    model = Model(
        start=pandas.to_datetime('2016-01-01'),
        end=pandas.to_datetime('2016-01-01')
    )

    storage = Storage(model, 'storage', num_inputs=1, num_outputs=0)
    otpt = Output(model, 'output', max_flow=99999, cost=-99999)
    storage.connect(otpt)

    model.check()

    for initial_volume in (50, 100):
        storage.max_volume = initial_volume
        storage.initial_volume = initial_volume
        model.run()
        assert(otpt.flow == initial_volume)

def test_shorthand_property():
    # test shorthand assignment of constant properties
    model = Model()
    node = Node(model, 'node')
    for attr in ('min_flow', 'max_flow', 'cost', 'conversion_factor'):
        # should except int, float or Paramter
        setattr(node, attr, 123)
        if attr == 'conversion_factor':
            with pytest.raises(ValueError):
                setattr(node, attr, Parameter(model))
        else:
            setattr(node, attr, Parameter(model))

        with pytest.raises(TypeError):
            setattr(node, attr, '123')
            setattr(node, attr, None)


def test_shorthand_property_storage():
    # test shorthand assignment of constant properties
    model = Model()
    node = Storage(model, 'node')
    for attr in ('min_volume', 'max_volume', 'cost', 'level'):
        # should except int, float or Paramter
        setattr(node, attr, 123)
        if attr == 'conversion_factor':
            with pytest.raises(ValueError):
                setattr(node, attr, Parameter(model))
        else:
            setattr(node, attr, Parameter(model))

        with pytest.raises(TypeError):
            setattr(node, attr, '123')
            setattr(node, attr, None)


def test_reset_before_run():
    # See issue #82. Previously this would raise:
    #    AttributeError: Memoryview is not initialized
    model = Model()
    node = Node(model, 'node')
    model.reset()


def test_check_isolated_nodes(simple_linear_model):
    """Test model storage checker"""
    # the simple model shouldn't have any isolated nodes
    model = simple_linear_model
    model.check()

    # add a node, but don't connect it to the network
    isolated_node = Input(model, 'isolated')
    with pytest.raises(ModelStructureError):
        model.check()

def test_check_isolated_nodes_storage():
    """Test model structure checker with Storage

    The Storage node itself doesn't have any connections, but it's child
    nodes do need to be connected.
    """
    model = Model()

    # add a storage, but don't connect it's outflow to anything
    storage = Storage(model, 'storage', num_inputs=1, num_outputs=0)
    with pytest.raises(ModelStructureError):
        model.check()

    # add a demand node and connect it to the storage outflow
    demand = Output(model, 'demand')
    storage.connect(demand, from_slot=0)
    model.check()

def test_storage_max_volume_zero():
    """Test a that an max_volume of zero results in a NaN for current_pc and no exception

    """

    model = Model(
        start=pandas.to_datetime('2016-01-01'),
        end=pandas.to_datetime('2016-01-01')
    )

    storage = Storage(model, 'storage', num_inputs=1, num_outputs=0)
    otpt = Output(model, 'output', max_flow=99999, cost=-99999)
    storage.connect(otpt)

    storage.max_volume = 0

    model.run()
    assert np.isnan(storage.current_pc)


def test_storage_max_volume_param():
    """Test a that an max_volume with a Parameter results in the correct current_pc

    """

    model = Model(
        start=pandas.to_datetime('2016-01-01'),
        end=pandas.to_datetime('2016-01-01')
    )

    storage = Storage(model, 'storage', num_inputs=1, num_outputs=0)
    otpt = Output(model, 'output', max_flow=99999, cost=-99999)
    storage.connect(otpt)

    p = ConstantParameter(model, 20.0)
    storage.max_volume = p
    storage.initial_volume = 10.0

    model.setup()
    np.testing.assert_allclose(storage.current_pc, 0.5)

    model.run()

    p.set_double_variables(np.asarray([40.0, ]))
    model.reset()
    np.testing.assert_allclose(storage.current_pc, 0.25)


def test_storage_initial_volume_pc():
    """Test that setting initial volume as a percentage works as expected.
    """
    model = Model(
        start=pandas.to_datetime('2016-01-01'),
        end=pandas.to_datetime('2016-01-01')
    )

    storage = Storage(model, 'storage', num_inputs=1, num_outputs=0)
    otpt = Output(model, 'output', max_flow=99999, cost=-99999)
    storage.connect(otpt)

    p = ConstantParameter(model, 20.0)
    storage.max_volume = p
    storage.initial_volume_pc = 0.5

    model.setup()
    np.testing.assert_allclose(storage.current_pc, 0.5)
    np.testing.assert_allclose(storage.volume, 10.0)

    model.run()

    p.set_double_variables(np.asarray([40.0, ]))
    model.reset()
    np.testing.assert_allclose(storage.current_pc, 0.5)
    np.testing.assert_allclose(storage.volume, 20.0)


def test_storage_max_volume_param_raises():
    """Test a that an max_volume with a Parameter that has children.
    
    Only some aggregated style parameters should work here.
    """

    model = Model(
        start=pandas.to_datetime('2016-01-01'),
        end=pandas.to_datetime('2016-01-01')
    )

    storage = Storage(model, 'storage', num_inputs=1, num_outputs=0)
    otpt = Output(model, 'output', max_flow=99999, cost=-99999)
    storage.connect(otpt)

    p = AggregatedParameter(model, [ConstantParameter(model, 20.0), ConstantParameter(model, 20.0)], agg_func='sum')

    storage.max_volume = p
    storage.initial_volume = 10.0

    model.setup()
    np.testing.assert_allclose(storage.current_pc, 0.25)


def test_storage_max_volume_param_raises():
    """Test a that an max_volume with a Parameter that has children is an error

    """

    model = Model(
        start=pandas.to_datetime('2016-01-01'),
        end=pandas.to_datetime('2016-01-01')
    )

    storage = Storage(model, 'storage', num_inputs=1, num_outputs=0)
    otpt = Output(model, 'output', max_flow=99999, cost=-99999)
    storage.connect(otpt)

    p = AggregatedParameter(model, [ConstantParameter(model, 20.0), ConstantParameter(model, 20.0)], agg_func='sum')
    p1 = AggregatedParameter(model, [p, ConstantParameter(model, 1.5)], agg_func="product")

    storage.max_volume = p1
    storage.initial_volume = 10.0

    with pytest.raises(RuntimeError):
        model.run()


def test_storage_initial_volume_table():
    """ Test loading initial storage volume from a table """
    filename = os.path.join(TEST_FOLDER, "models", "reservoir_initial_vol_from_table.json")
    model = Model.load(filename)

    np.testing.assert_allclose(model.nodes["supply1"].initial_volume, 0.0)
    np.testing.assert_allclose(model.nodes["supply2"].initial_volume, 35.0)


def test_recursive_delete():
    """Test recursive deletion of child nodes for compound nodes"""
    model = Model()
    n1 = Input(model, "n1")
    n2 = Output(model, "n2")
    s = Storage(model, "s", num_outputs=2)
    assert len(model.nodes) == 3
    assert len(model.graph.nodes()) == 6
    del(model.nodes["n1"])
    assert len(model.nodes) == 2
    assert len(model.graph.nodes()) == 5
    del(model.nodes["s"])
    assert len(model.nodes) == 1
    assert len(model.graph.nodes()) == 1


def test_json_include():
    """Test include in JSON document"""
    filename = os.path.join(TEST_FOLDER, "models", "extra1.json")
    model = Model.load(filename)

    supply1 = model.nodes["supply1"]
    supply2 = model.nodes["supply2"]
    assert(isinstance(supply2.max_flow, ConstantParameter))

def test_json_min_version():
    """Test warning is raised if document minimum version is more than we have"""
    filename = os.path.join(TEST_FOLDER, "models", "version1.json")
    with pytest.warns(RuntimeWarning):
        model = Model.load(filename)

def test_initial_timestep():
    """Current timestep before model has started is undefined"""
    filename = os.path.join(TEST_FOLDER, "models", "extra1.json")
    model = Model.load(filename)
    assert(model.timestepper.current is None)
    model.run()
    assert(isinstance(model.timestepper.current, Timestep))

def test_timestepper_repr(model):
    timestepper = model.timestepper
    print(timestepper)

def test_timestep_repr():
    filename = os.path.join(TEST_FOLDER, "models", "simple1.json")
    model = Model.load(filename)
    model.timestepper.end = "2015-01-05"
    res = model.run()
    assert(isinstance(res.timestep, Timestep))
    assert("2015-01-05" in str(res.timestep))

def test_virtual_storage_cost():
    """VirtualStorage doesn't (currently) implement its cost attribute"""
    model = Model()
    A = Input(model, "A")
    B = Output(model, "B")
    A.connect(B)
    node = VirtualStorage(model, "storage", [A, B])
    node.check()
    node.cost = 5.0
    with pytest.raises(NotImplementedError):
        model.check()

def test_json_invalid():
    """JSON exceptions should report file name"""
    filename = os.path.join(TEST_FOLDER, "models", "invalid"+".json")
    with pytest.raises(ValueError) as excinfo:
        model = Model.load(filename)
    assert("invalid.json" in str(excinfo.value))

def test_json_invalid_include():
    """JSON exceptions should report file name, even for includes"""
    filename = os.path.join(TEST_FOLDER, "models", "invalid_include"+".json")
    with pytest.raises(ValueError) as excinfo:
        model = Model.load(filename)
    assert("invalid.json" in str(excinfo.value))


def test_variable_load():
    """Current timestep before model has started is undefined"""
    filename = os.path.join(TEST_FOLDER, "models", "demand_saving2_with_variables.json")
    model = Model.load(filename)

    # Test the correct number of each component is loaded
    assert len(model.variables) == 3
    assert len(model.objectives) == 1
    assert len(model.constraints) == 1
    # Test the names are as expected
    assert sorted([c.name for c in model.variables]) == ["demand_profile", "level1", "level2"]
    assert sorted([c.name for c in model.objectives]) == ["total_deficit", ]
    assert sorted([c.is_objective for c in model.objectives]) == ["minimise", ]
    assert sorted([c.name for c in model.constraints]) == ["min_volume", ]

