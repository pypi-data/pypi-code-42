# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python2, python3
"""Functions to create grids suitable for PDE pricing."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

import numpy as np
from six.moves import range
from six.moves import zip
import tensorflow as tf

GridSpec = collections.namedtuple(
    'GridSpec',
    [
        'dim',  # The dimension of the grid. Positive integer `Tensor`.
        'minimums',  # The lower end points of the grid as an iterable.
        # A real-valued `Tensor` of a shape `batch_shape` for each
        # axis.
        'maximums',  # The upper end points of the grid as an iterable.
        # A real-valued `Tensor` of a shape `batch_shape` for each
        # axis.
        'sizes',  # The number of points along each grid axis. One integer value
        # greater than 2 for each axis as an iterable.
        'locations',  # The grid locations as projected along each axis. One
        # `Tensor` of shape `[..., n]`, where `n` is the number of
        # points along that axis . The first dimensions are
        # the batch shape. The grid itself can be
        # seen as a cartesian product of the locations array.
        'deltas',  # The difference between consecutive elements of the
        # locations along each axis. Represented as an array of `Tensor`s. Each
        # `Tensor` is of a shape that will broadcast with a `Tensor` of
        # shape [..., n-1] where n is the number of points along that
        # axis and first dimensions are the batch shape, same as for
        # locations. Note that it should not be assumed that the shape
        # itself will be `[..., n-1]`. For example, it may be a scalar.
        'grid'  # The full grid of coordinates. The grid is a single real
        # `Tensor` of shape `batch_shape + sizes` + [dim].  For example, if
        # sizes = [3, 4], the grid is a `Tensor` of shape [3, 4, 2] and
        # grid[0, 0, :] is the (x, y) coordinate of the bottom left corner
        # of the grid.
    ])


def uniform_grid(minimums,
                 maximums,
                 sizes,
                 dtype=None,
                 validate_args=False,
                 name=None):
  """Creates a grid spec for a uniform grid.

  A uniform grid is characterized by having a constant gap between neighboring
  points along each axis.

  Note that the shape of all three parameters must be fully defined and equal
  to each other. The shape is used to determine the dimension of the grid.

  Args:
    minimums: Real `Tensor` of rank 1 containing the lower end points of the
      grid. Must have the same shape as those of `maximums` and `sizes` args.
    maximums: `Tensor` of the same dtype and shape as `minimums`. The upper
      endpoints of the grid.
    sizes: Integer `Tensor` of the same shape as `minimums`. The size of the
      grid in each axis. Each entry must be greater than or equal to 2 (i.e. the
      sizes include the end points). For example, if minimums = [0.] and
      maximums = [1.] and sizes = [3], the grid will have three points at [0.0,
      0.5, 1.0].
    dtype: Optional tf.dtype. The default dtype to use for the grid.
    validate_args: Python boolean indicating whether to validate the supplied
      arguments. The validation checks performed are (a) `maximums` > `minimums`
      (b) `sizes` >= 2.
    name: Python str. The name prefixed to the ops created by this function. If
      not supplied, the default name 'uniform_grid_spec' is used.

  Returns:
    An instance of `GridSpec`.

  Raises:
    ValueError if the shape of maximums, minimums and sizes are not fully
    defined or they are not identical to each other or they are not rank 1.
  """
  with tf.compat.v1.name_scope(name, 'uniform_grid',
                               [minimums, maximums, sizes]):
    minimums = tf.convert_to_tensor(minimums, dtype=dtype, name='minimums')
    maximums = tf.convert_to_tensor(maximums, dtype=dtype, name='maximums')
    sizes = tf.convert_to_tensor(sizes, name='sizes')
    # Check that the shape of `sizes` is statically defined.
    if not _check_shapes_fully_defined(minimums, maximums, sizes):
      raise ValueError('The shapes of minimums, maximums and sizes '
                       'must be fully defined.')

    if not (minimums.shape == maximums.shape and minimums.shape == sizes.shape):
      raise ValueError('The shapes of minimums, maximums and sizes must be '
                       'identical.')

    if len(minimums.shape.as_list()) != 1:
      raise ValueError('The minimums, maximums and sizes must all be rank 1.')

    control_deps = []
    if validate_args:
      control_deps = [
          tf.debugging.assert_greater(maximums, minimums),
          tf.debugging.assert_greater_equal(sizes, 2)
      ]
    with tf.compat.v1.control_dependencies(control_deps):
      dim = sizes.shape[0]
      deltas = tf.unstack(
          (maximums - minimums) / tf.cast(sizes - 1, dtype=maximums.dtype),
          axis=0)
      locations = [
          tf.linspace(minimums[i], maximums[i], num=sizes[i])
          for i in range(dim)
      ]
      grid = tf.stack(tf.meshgrid(*locations, indexing='ij'), axis=-1)
      return GridSpec(
          dim=tf.convert_to_tensor(dim, name='dim'),
          minimums=tf.unstack(minimums, axis=0),
          maximums=tf.unstack(maximums, axis=0),
          sizes=tf.unstack(sizes, axis=0),
          deltas=deltas,
          locations=locations,
          grid=grid)


def log_uniform_grid(minimums,
                     maximums,
                     sizes,
                     dtype=None,
                     validate_args=False,
                     name=None):
  """Creates a grid spec for a uniform grid in a log-space.

  A log-uniform grid is characterized by having a constant gap between
  neighboring points along each axis in the log-space, i.e., the logarithm of
  output grid is the uniform grid.

  Note that the shape of all three parameters must be fully defined and equal
  to each other. The shape is used to determine the dimension of the grid.
  Note that all the parameters are supplied and returned for the original space
  and not the log-space.

  #### Examples

  ```python
  dtype = np.float64
  min_x, max_x, sizes = [0.1], [3.0], [5]
  # Here min_x and max_x are in the original space and *not* in the log-space.
  grid = log_uniform_grid(min_x, max_x, sizes,dtype=dtype)
  with tf.Session() as sess:
    grid = sess.run(grid)
  # Note that the minimum and maximum grid locations are the same as min_x and
  # max_x.
  print('locations: ', grid.locations)
  # locations:  [array([ 0.1, 0.234, 0.548, 1.282, 3.0])]
  print('grid: ', grid.grid)
  # grid: array([[ 0.1], [0.234], [0.548], [1.282], [ 3.0]])
  print('deltas: ', grid.deltas)
  # deltas: [array([ 0.134, 0.314, 0.734, 1.718])]
  ```

  Args:
    minimums: Real `Tensor` of rank 1 containing the lower end points of the
      output grid. Must have the same shape as those of `maximums` and `sizes`
      args.
    maximums: `Tensor` of the same dtype and shape as `minimums`. The upper
      endpoints of the output grid.
    sizes: Integer `Tensor` of the same shape as `minimums`. The size of the
      grid in each axis. Each entry must be greater than or equal to 2 (i.e. the
      sizes include the end points).
    dtype: Optional tf.dtype. The default dtype to use for the grid.
    validate_args: Python boolean indicating whether to validate the supplied
      arguments. The validation checks performed are (a) `maximums` > `minimums`
      (b) `minimums` > 0.0 (c) `sizes` >= 2.
    name: Python str. The name prefixed to the ops created by this function. If
      not supplied, the default name 'uniform_grid_spec' is used.

  Returns:
    An instance of `GridSpec`.

  Raises:
    ValueError if the shape of maximums, minimums and sizes are not fully
    defined or they are not identical to each other or they are not rank 1.
  """
  with tf.compat.v1.name_scope(name, 'log_uniform_grid',
                               [minimums, maximums, sizes]):
    minimums = tf.convert_to_tensor(minimums, dtype=dtype, name='minimums')
    maximums = tf.convert_to_tensor(maximums, dtype=dtype, name='maximums')
    sizes = tf.convert_to_tensor(sizes, name='sizes')
    # Check that the shape of `sizes` is statically defined.
    if not _check_shapes_fully_defined(minimums, maximums, sizes):
      raise ValueError('The shapes of minimums, maximums and sizes '
                       'must be fully defined.')

    if not (minimums.shape == maximums.shape and minimums.shape == sizes.shape):
      raise ValueError('The shapes of minimums, maximums and sizes must be '
                       'identical.')

    if len(minimums.shape.as_list()) != 1:
      raise ValueError('The minimums, maximums and sizes must all be rank 1.')

    control_deps = []
    if validate_args:
      control_deps = [
          tf.debugging.assert_greater(maximums, minimums),
          tf.debugging.assert_greater(minimums, tf.constant(0, dtype=dtype)),
          tf.debugging.assert_greater_equal(sizes, 2)
      ]
    # Generate a uniform grid in the log-space taking into account that the
    # arguments were already validated.
    with tf.compat.v1.control_dependencies(control_deps):
      dim = sizes.shape[0]
      log_maximums = tf.log(maximums)
      log_minimums = tf.log(minimums)

      locations = [
          tf.exp(tf.linspace(log_minimums[i], log_maximums[i], num=sizes[i]))
          for i in range(dim)
      ]
      grid = tf.stack(tf.meshgrid(*locations, indexing='ij'), axis=-1)

      deltas = [location[1:] - location[:-1] for location in locations]

      return GridSpec(
          dim=tf.convert_to_tensor(dim, name='dim'),
          minimums=tf.unstack(minimums, axis=0),
          maximums=tf.unstack(maximums, axis=0),
          sizes=tf.unstack(sizes, axis=0),
          deltas=deltas,
          locations=locations,
          grid=grid)


def rectangular_grid(axis_locations,
                     dtype=None,
                     validate_args=False,
                     name=None):
  """Specifies parameters for an axis-wise non-uniform grid in n-dimensions.

  This specifies rectangular grids formed by taking the cartesian product
  of points along each axis. For example, in two dimensions, one may specify
  a grid by specifying points along the x-axis as [0.0, 1.0, 1.3] and along the
  y-axis by [3.0, 3.6, 4.3, 7.0]. Taking the cartesian product of the two,
  produces a 3 x 4 grid which is rectangular but non-uniform along each axis.

  The points along each axis should be in ascending order and there must be at
  least two points specified along each axis. If `validate_args` is set to
  True, both these conditions are explicitly verified.

  Args:
    axis_locations: A Python iterable of rank 1 real `Tensor`s. The number of
      `Tensor`s in the list is the dimension of the grid. The i'th element
      specifies the coordinates of the points of the grid along that axis. Each
      `Tensor` must have at least two elements.
    dtype: Optional tf.dtype. The default dtype to use for the grid.
    validate_args: Python boolean indicating whether to validate the supplied
      arguments. The validation checks performed are (a) Length of each element
      of `axis_locations` >= 2 (b) Each element of `axis_locations` is in
      ascending order.
    name: Python str. The name prefixed to the ops created by this class. If not
      supplied, the default name 'rectangular_grid' is used.

  Returns:
    An instance of `GridSpec`.

  Raises:
    ValueError if `axis_locations` is empty.
  """
  with tf.compat.v1.name_scope(name, 'rectangular_grid', [axis_locations]):
    if not axis_locations:
      raise ValueError('The axis locations parameter cannot be empty.')

    dim = len(axis_locations)
    locations = [
        tf.convert_to_tensor(
            location, dtype=dtype, name='location_axis_{}'.format(i))
        for i, location in enumerate(axis_locations)
    ]
    control_deps = []
    if validate_args:
      control_deps = [
          tf.assert_greater(tf.size(location), 1) for location in locations
      ]

    deltas = []
    for location in locations:
      deltas.append(location[1:] - location[:-1])
      if validate_args:
        control_deps.append(tf.assert_greater(deltas[-1], 0.))
    with tf.compat.v1.control_dependencies(control_deps):
      grid = tf.stack(tf.meshgrid(*locations, indexing='ij'), axis=-1)
      minimums, maximums, sizes = list(
          zip(*[(loc[0], loc[-1], tf.size(loc)) for loc in locations]))
      return GridSpec(
          dim=tf.convert_to_tensor(dim, name='dim'),
          minimums=minimums,
          maximums=maximums,
          sizes=sizes,
          deltas=deltas,
          locations=locations,
          grid=grid)


def uniform_grid_with_extra_point(minimums,
                                  maximums,
                                  sizes,
                                  extra_grid_point,
                                  dtype=None,
                                  validate_args=False,
                                  name=None):
  """Creates a grid spec for a uniform grid with an extra grid point.

  A uniform grid is characterized by having a constant gap between neighboring
  points along each axis. An extra grid point is useful, for example, when
  computing sensitivities for a value through a grid pricing method

  #### Examples

  ```python
  dtype = np.float64
  extra_locations = tf.constant([[1, 2], [2, 3]], dtype=dtype)
  min_x, max_x, sizes = [[0, 0], [0, 0]], [[10, 5], [100, 5]], [3, 2]
  # Here min_x and max_x are in the original space and *not* in the log-space.
  grid = uniform_grid_with_extra_point(
      min_x, max_x, sizes,
      extra_grid_point=extra_locations, dtype=dtype)
  with tf.Session() as sess:
    grid = sess.run(grid)
  # Note that the minimum and maximum grid locations are the same as min_x and
  # max_x.
  print(grid.locations[0])
  # [[0, 1, 5, 10], [0, 2, 50, 100]]
  print(grid.locations[1])
  # [[0, 2, 5], [0, 3, 5]]
  ```

  Note that the shape of all four parameters must be fully defined and equal
  to each other. The shape is used to determine the dimension of the grid.

  Args:
    minimums: Real `Tensor` of rank 1 or 2 containing the lower end points of
      the grid. Must have the same shape as those of `maximums`. When rank is 2
      the first dimension is the batch dimension.
    maximums: `Tensor` of the same dtype and shape as `minimums`. The upper
      endpoints of the grid.
    sizes: Integer rank 1 `Tensor` of the same shape as `minimums`. The size of
      the grid in each axis. Each entry must be greater than or equal to 2 (i.e.
      the sizes include the end points). For example, if minimums = [0.] and
      maximums = [1.] and sizes = [3], the grid will have three points at [0.0,
      0.5, 1.0].
    extra_grid_point: A `Tensor` of the same `dtype` as `minimums` and of shape
      `[batch_size, n]`, where `batch_shape` is a positive integer and `n` is
      the number of points along a dimension. These are the extra points added
      to the grid, so that the output grid `locations` have shape `[batch_shape,
      n+1]`.
    dtype: Optional tf.dtype. The default dtype to use for the grid.
    validate_args: Python boolean indicating whether to validate the supplied
      arguments. The validation checks performed are (a) `maximums` > `minimums`
      (b) `sizes` >= 2.
    name: Python str. The name prefixed to the ops created by this function. If
      not supplied, the default name 'uniform_grid_spec' is used.

  Returns:
    An instance of `GridSpec` with batch shape `[batch_size]`.

  Raises:
    ValueError if the shape of maximums, minimums and sizes are not fully
    defined or they are not identical to each other or they are not rank 1.
  """
  with tf.compat.v1.name_scope(name, 'uniform_grid',
                               [minimums, maximums, sizes]):
    minimums = tf.convert_to_tensor(minimums, dtype=dtype, name='minimums')
    maximums = tf.convert_to_tensor(maximums, dtype=dtype, name='maximums')
    extra_grid_point = tf.convert_to_tensor(
        extra_grid_point, dtype=dtype, name='extra_grid_point')
    batch_shape = tf.shape(extra_grid_point)[0]
    sizes = tf.convert_to_tensor(sizes, name='sizes')
    # Check that the shape of `sizes` is statically defined.
    if not _check_shapes_fully_defined(minimums, maximums, sizes):
      raise ValueError('The shapes of minimums, maximums and sizes '
                       'must be fully defined.')

    if minimums.shape != maximums.shape:
      raise ValueError('The shapes of minimums and maximums must be identical.')

    control_deps = []
    if validate_args:
      control_deps = [
          tf.debugging.assert_greater(maximums, minimums),
          tf.debugging.assert_greater_equal(sizes, 2)
      ]
    locations = []
    with tf.compat.v1.control_dependencies(control_deps):
      dim = sizes.shape[0]
      for i in range(dim):
        locations.append(
            tf.expand_dims(minimums[..., i], -1) +
            tf.expand_dims((maximums[..., i] - minimums[..., i]), -1) * tf
            .linspace(tf.constant(0., dtype=minimums.dtype), 1.0, num=sizes[i]))
      # Broadcast `locations` to the shape `[batch_shape, size]`
      for i, location in enumerate(locations):
        locations[i] = location + tf.zeros([batch_shape, sizes[i]], dtype=dtype)
      # Add `extra_grid_point` to `locations`
      sizes = []
      for i, location in enumerate(locations):
        location_update = tf.sort(
            tf.concat(
                [location, tf.expand_dims(extra_grid_point[:, i], -1)], -1), -1)
        locations[i] = location_update
        sizes.append(tf.shape(location_update)[-1])
      deltas = [
          location[..., 1:] - location[..., :-1] for location in locations
      ]
      grid = _meshgrid(batch_shape, locations, sizes)

      return GridSpec(
          dim=tf.convert_to_tensor(dim, name='dim'),
          minimums=tf.unstack(minimums, axis=0),
          maximums=tf.unstack(maximums, axis=0),
          sizes=tf.unstack(sizes, axis=0),
          deltas=deltas,
          locations=locations,
          grid=grid)


def log_uniform_grid_with_extra_point(minimums,
                                      maximums,
                                      sizes,
                                      extra_grid_point,
                                      dtype=None,
                                      validate_args=False,
                                      name=None):
  """Creates a grid for a uniform grid in a log-space with an extra grid point.

  A log-uniform grid is characterized by having a constant gap between
  neighboring points along each axis in the log-space, i.e., the logarithm of
  output grid is the uniform grid.  An extra grid point is useful, for example,
  when computing sensitivities for a value through a grid pricing method.

  Note that the shape of all three parameters must be fully defined and equal
  to each other. The shape is used to determine the dimension of the grid.
  Note that all the parameters are supplied and returned for the original space
  and not the log-space.

  #### Examples

  ```python
  dtype = np.float64
  extra_locations = tf.constant([[0.5, 2], [2, 3]], dtype=dtype)
  min_x, max_x, sizes = [[0.1, 0.1], [0.01, 0.1]], [[10, 5], [100, 5]], [3, 2]
  # Here min_x and max_x are in the original space and *not* in the log-space.
  grid = log_uniform_grid_with_extra_point(
      min_x, max_x, sizes,
      extra_grid_point=extra_locations, dtype=dtype)
  with tf.Session() as sess:
    grid = sess.run(grid)
  # Note that the minimum and maximum grid locations are the same as min_x and
  # max_x.
  print(grid.locations[0])
  # [[0.1, 0.5, 1.0, 10.0], [0.01, 1.0, 2.0, 100.0]]
  print(grid.locations[1])
  # [[0.1, 2, 5], [0.1, 3, 5]]
  ```

  Args:
    minimums: Real `Tensor` of rank 1 or 2 containing the lower end points of
      the grid. Must have the same shape as those of `maximums`. When rank is 2
      the first dimension is the batch dimension.
    maximums: `Tensor` of the same dtype and shape as `minimums`. The upper
      endpoints of the grid.
    sizes: Integer rank 1 `Tensor` of the same shape as `minimums`. The size of
      the grid in each axis. Each entry must be greater than or equal to 2 (i.e.
      the sizes include the end points).
    extra_grid_point: A `Tensor` of the same `dtype` as `minimums` and of shape
      `[batch_size, n]`, where `batch_shape` is a positive integer and `n` is
      the number of points along a dimension. These are the extra points added
      to the grid, so that the output grid `locations` have shape `[batch_shape,
      n+1]`.
    dtype: Optional tf.dtype. The default dtype to use for the grid.
    validate_args: Python boolean indicating whether to validate the supplied
      arguments. The validation checks performed are (a) `maximums` > `minimums`
      (b) `minimums` > 0.0 (c) `sizes` >= 2.
    name: Python str. The name prefixed to the ops created by this function. If
      not supplied, the default name 'uniform_grid_spec' is used.

  Returns:
     An instance of `GridSpec` with batch shape `[batch_size]`.

  Raises:
    ValueError if the shape of maximums, minimums and sizes are not fully
    defined or they are not identical to each other or they are not rank 1.
  """
  with tf.compat.v1.name_scope(name, 'log_uniform_grid',
                               [minimums, maximums, sizes]):
    minimums = tf.convert_to_tensor(minimums, dtype=dtype, name='minimums')
    maximums = tf.convert_to_tensor(maximums, dtype=dtype, name='maximums')
    sizes = tf.convert_to_tensor(sizes, name='sizes')
    extra_grid_point = tf.convert_to_tensor(
        extra_grid_point, dtype=dtype, name='extra_grid_point')
    batch_shape = tf.shape(extra_grid_point)[0]
    # Check that the shape of `sizes` is statically defined.
    if not _check_shapes_fully_defined(minimums, maximums, sizes):
      raise ValueError('The shapes of minimums, maximums and sizes '
                       'must be fully defined.')

    if minimums.shape != maximums.shape:
      raise ValueError('The shapes of minimums and maximums must be identical.')

    control_deps = []
    if validate_args:
      control_deps = [
          tf.debugging.assert_greater(maximums, minimums),
          tf.debugging.assert_greater(minimums, tf.constant(0, dtype=dtype)),
          tf.debugging.assert_greater_equal(sizes, 2)
      ]
    # Generate a uniform grid in the log-space taking into account that the
    # arguments were already validated.
    locations = []
    with tf.compat.v1.control_dependencies(control_deps):
      dim = sizes.shape[0]
      log_maximums = tf.log(maximums)
      log_minimums = tf.log(minimums)
      for i in range(dim):
        locations.append(
            tf.expand_dims(log_minimums[..., i], -1) +
            tf.expand_dims((log_maximums[..., i] - log_minimums[..., i]), -1) *
            tf.linspace(
                tf.constant(0., dtype=minimums.dtype), 1.0, num=sizes[i]))
      # Broadcast `locations` to the shape `[batch_shape, size]`
      for i, location in enumerate(locations):
        locations[i] = location + tf.zeros([batch_shape, sizes[i]], dtype=dtype)
      # Add `extra_grid_point` to `locations`
      sizes = []
      for i, location in enumerate(locations):
        location_update = tf.sort(
            tf.concat(
                [location,
                 tf.expand_dims(tf.log(extra_grid_point[:, i]), -1)], -1), -1)
        locations[i] = tf.exp(location_update)
        sizes.append(tf.shape(location_update)[-1])
      deltas = [
          location[..., 1:] - location[..., :-1] for location in locations
      ]
      grid = _meshgrid(batch_shape, locations, sizes)

      return GridSpec(
          dim=tf.convert_to_tensor(dim, name='dim'),
          minimums=tf.unstack(minimums, axis=0),
          maximums=tf.unstack(maximums, axis=0),
          sizes=tf.unstack(sizes, axis=0),
          deltas=deltas,
          locations=locations,
          grid=grid)


def _check_shapes_fully_defined(*args):
  """Checks if all the arguments have fully defined shapes."""
  return np.all([arg.shape.is_fully_defined() for arg in args])


def _meshgrid(batch_shape, locations, sizes):
  """Extends tf.meshgrid to accept batched locations."""
  dim = len(locations)
  extra_dims = (1,) * dim
  output = []
  zeros = tf.zeros([batch_shape] + sizes, dtype=locations[0].dtype)
  for i, location in enumerate(locations):
    output.append(
        tf.reshape(location, (batch_shape,) + extra_dims[:i] +
                   (-1,) + extra_dims[i + 1:]) + zeros)
  return tf.stack(output, -1)
