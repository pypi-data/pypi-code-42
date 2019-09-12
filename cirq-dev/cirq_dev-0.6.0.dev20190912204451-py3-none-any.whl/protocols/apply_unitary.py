# Copyright 2018 The Cirq Developers
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

"""A protocol for implementing high performance unitary left-multiplies."""


from typing import (
    Any,
    cast,
    Iterable,
    Optional,
    Sequence,
    Tuple,
    TYPE_CHECKING,
    TypeVar,
    Union,
)

import numpy as np
from typing_extensions import Protocol

from cirq import linalg
from cirq.protocols import qid_shape_protocol
from cirq.protocols.decompose import _try_decompose_into_operations_and_qubits
from cirq.type_workarounds import NotImplementedType

if TYPE_CHECKING:
    import cirq


# This is a special indicator value used by the apply_unitary method
# to determine whether or not the caller provided a 'default' argument. It must
# be of type np.ndarray to ensure the method has the correct type signature in
# that case. It is checked for using `is`, so it won't have a false positive if
# the user provides a different np.array([]) value.

RaiseTypeErrorIfNotProvided = np.array([])  # type: np.ndarray

TDefault = TypeVar('TDefault')


class ApplyUnitaryArgs:
    """Arguments for performing an efficient left-multiplication by a unitary.

    The receiving object is expected to mutate `target_tensor` so that it
    contains the state after multiplication, and then return `target_tensor`.
    Alternatively, if workspace is required, the receiving object can overwrite
    `available_buffer` with the results and return `available_buffer`. Or, if
    the receiving object is attempting to be simple instead of fast, it can
    create an entirely new array and return that.

    Attributes:
        target_tensor: The input tensor that needs to be left-multiplied by
            the unitary effect of the receiving object. The tensor will
            have the shape (2, 2, 2, ..., 2). It usually corresponds to
            a multi-qubit superposition, but it could also be a multi-qubit
            unitary transformation or some other concept.
        available_buffer: Pre-allocated workspace with the same shape and
            dtype as the target tensor.
        axes: Which axes the unitary effect is being applied to (e.g. the
            qubits that the gate is operating on).
    """

    def __init__(self, target_tensor: np.ndarray, available_buffer: np.ndarray,
                 axes: Iterable[int]):
        """

        Args:
            target_tensor: The input tensor that needs to be left-multiplied by
                the unitary effect of the receiving object. The tensor will
                have the shape (2, 2, 2, ..., 2). It usually corresponds to
                a multi-qubit superposition, but it could also be a multi-qubit
                unitary transformation or some other concept.
            available_buffer: Pre-allocated workspace with the same shape and
                dtype as the target tensor.
            axes: Which axes the unitary effect is being applied to (e.g. the
                qubits that the gate is operating on).

        """
        self.target_tensor = target_tensor
        self.available_buffer = available_buffer
        self.axes = tuple(axes)

    @staticmethod
    def default(num_qubits: Optional[int] = None,
                *,
                qid_shape: Optional[Tuple[int, ...]] = None
               ) -> 'ApplyUnitaryArgs':
        """A default instance starting in state |0⟩.

        Specify exactly one argument.

        Args:
            num_qubits: The number of qubits to make space for in the state.
            qid_shape: The shape of the state, specifying the dimension of each
                qid."""
        if (num_qubits is None) == (qid_shape is None):
            raise TypeError('Specify exactly one of num_qubits or qid_shape.')
        if num_qubits is not None:
            qid_shape = (2,) * num_qubits
        qid_shape = cast(Tuple[int, ...], qid_shape)  # Satisfy mypy
        num_qubits = len(qid_shape)
        state = linalg.one_hot(index=(0,) * num_qubits,
                               shape=qid_shape,
                               dtype=np.complex128)
        return ApplyUnitaryArgs(state, np.empty_like(state), range(num_qubits))

    def _for_operation_with_qid_shape(self, indices: Iterable[int],
                                      qid_shape: Tuple[int, ...]
                                     ) -> 'ApplyUnitaryArgs':
        """Creates a sliced and transposed view of `self` appropriate for an
        operation with shape `qid_shape` on qubits with the given indices.

        Example:
            sub_args = args._for_operation_with_qid_shape(indices, (2, 2, 2))
            # Slice where the first qubit is |1>.
            sub_args.target_tensor[..., 1, :, :]

        Args:
            indices: Integer indices into `self.axes` specifying which qubits
                the operation applies to.
            qid_shape: The qid shape of the operation, the expected number of
                quantum levels in each qubit the operation applies to.

        Returns: A new `ApplyUnitaryArgs` where `sub_args.target_tensor` and
            `sub_args.available_buffer` are sliced and transposed views of
            `self.target_tensor` and `self.available_buffer` respectively.
        """
        slices = [slice(0, size) for size in qid_shape]
        sub_axes = [self.axes[i] for i in indices]
        axis_set = set(sub_axes)
        other_axes = [
            axis for axis in range(len(self.target_tensor.shape))
            if axis not in axis_set
        ]
        ordered_axes = (*other_axes, *sub_axes)
        # Transpose sub_axes to the end of the shape and slice them
        target_tensor = self.target_tensor.transpose(*ordered_axes)[(...,
                                                                     *slices)]
        available_buffer = self.available_buffer.transpose(*ordered_axes)[(
            ..., *slices)]
        new_axes = range(len(other_axes), len(ordered_axes))
        return ApplyUnitaryArgs(target_tensor, available_buffer, new_axes)

    def subspace_index(
            self,
            little_endian_bits_int: int,
    ) -> Tuple[Union[slice, int, 'ellipsis'], ...]:
        """An index for the subspace where the target axes equal a value.

        Args:
            little_endian_bits_int: The desired value of the qubits at the
                targeted `axes`, packed into an integer. The least significant
                bit of the integer is the desired bit for the first axis, and
                so forth in increasing order.
            value_tuple: The desired value of the qids at the targeted `axes`,
                packed into a tuple.  Specify either `little_endian_bits_int` or
                `value_tuple`.

        Returns:
            A value that can be used to index into `target_tensor` and
            `available_buffer`, and manipulate only the part of Hilbert space
            corresponding to a given bit assignment.

        Example:
            If `target_tensor` is a 4 qubit tensor and `axes` is `[1, 3]` and
            then this method will return the following when given
            `little_endian_bits=0b01`:

                `(slice(None), 0, slice(None), 1, Ellipsis)`

            Therefore the following two lines would be equivalent:

                args.target_tensor[args.subspace_index(0b01)] += 1

                args.target_tensor[:, 0, :, 1] += 1
        """
        return linalg.slice_for_qubits_equal_to(self.axes,
                                                little_endian_bits_int)


class SupportsConsistentApplyUnitary(Protocol):
    """An object that can be efficiently left-multiplied into tensors."""

    def _apply_unitary_(self, args: ApplyUnitaryArgs
                        ) -> Union[np.ndarray, None, NotImplementedType]:
        """Left-multiplies a unitary effect onto a tensor with good performance.

        This method is given both the target tensor and workspace of the same
        shape and dtype. The method then either performs inline modifications of
        the target tensor and returns it, or writes its output into the
        workspace tensor and returns that. This signature makes it possible to
        write specialized simulation methods that run without performing large
        allocations, significantly increasing simulation performance.

        The target may represent a wave function, a unitary matrix, or some
        other tensor. Implementations will work in all of these cases as long as
        they correctly focus on only operating on the given axes.

        Args:
            args: A `cirq.ApplyUnitaryArgs` object with the `args.target_tensor`
                to operate on, an `args.available_workspace` buffer to use as
                temporary workspace, and the `args.axes` of the tensor to target
                with the unitary operation. Note that this method is permitted
                (and in fact expected) to mutate `args.target_tensor` and
                `args.available_workspace`.

        Returns:
            If the receiving object is not able to apply its unitary effect,
            None or NotImplemented should be returned.

            If the receiving object is able to work inline, it should directly
            mutate `args.target_tensor` and then return `args.target_tensor`.
            The caller will understand this to mean that the result is in
            `args.target_tensor`.

            If the receiving object is unable to work inline, it can write its
            output over `args.available_buffer` and then return
            `args.available_buffer`. The caller will understand this to mean
            that the result is in `args.available_buffer` (and so what was
            `args.available_buffer` will become `args.target_tensor` in the next
            call, and vice versa).

            The receiving object is also permitted to allocate a new
            numpy.ndarray and return that as its result.
        """


def apply_unitary(unitary_value: Any,
                  args: ApplyUnitaryArgs,
                  default: TDefault = RaiseTypeErrorIfNotProvided
                  ) -> Union[np.ndarray, TDefault]:
    """High performance left-multiplication of a unitary effect onto a tensor.

    Applies the unitary effect of `unitary_value` to the tensor specified in
    `args` by using the following strategies:

    A. Try to use `unitary_value._apply_unitary_(args)`.
        Case a) Method not present or returns `NotImplemented`.
            Continue to next strategy.
        Case b) Method returns `None`.
            Conclude `unitary_value` has no unitary effect.
        Case c) Method returns a numpy array.
            Forward the successful result to the caller.

    B. Try to use `unitary_value._unitary_()`.
        Case a) Method not present or returns `NotImplemented`.
            Continue to next strategy.
        Case b) Method returns `None`.
            Conclude `unitary_value` has no unitary effect.
        Case c) Method returns a numpy array.
            Multiply the matrix onto the target tensor and return to the caller.

    C. Try to use `unitary_value._decompose_()`.
        Case a) Method not present or returns `NotImplemented` or `None`.
            Continue to next strategy.
        Case b) Method returns an OP_TREE.
            Delegate to `cirq.apply_unitaries`.

    D. Conclude that `unitary_value` has no unitary effect.

    The order that the strategies are tried depends on the number of qubits
    being operated on. For small numbers of qubits (4 or less) the order is
    ABCD. For larger numbers of qubits the order is ACBD (because it is expected
    that decomposing will outperform generating the raw matrix).

    Args:
        unitary_value: The value with a unitary effect to apply to the target.
        args: A mutable `cirq.ApplyUnitaryArgs` object describing the target
            tensor, available workspace, and axes to operate on. The attributes
            of this object will be mutated as part of computing the result.
        default: What should be returned if `unitary_value` doesn't have a
            unitary effect. If not specified, a TypeError is raised instead of
            returning a default value.

    Returns:
        If the receiving object does not have a unitary effect, then the
        specified default value is returned (or a TypeError is raised). If
        this occurs, then `target_tensor` should not have been mutated.

        Otherwise the result is the `np.ndarray` instance storing the result.
        This may be `args.target_tensor`, `args.available_workspace`, or some
        other numpy array. It is the caller's responsibility to correctly handle
        all three of these cases. In all cases `args.target_tensor` and
        `args.available_buffer` may have been mutated.

    Raises:
        TypeError: `unitary_value` doesn't have a unitary effect and `default`
            wasn't specified.
    """

    # Decide on order to attempt application strategies.
    if len(args.axes) <= 4:
        strats = [
            _strat_apply_unitary_from_apply_unitary,
            _strat_apply_unitary_from_unitary,
            _strat_apply_unitary_from_decompose
        ]
    else:
        strats = [
            _strat_apply_unitary_from_apply_unitary,
            _strat_apply_unitary_from_decompose,
            _strat_apply_unitary_from_unitary
        ]

    # Try each strategy, stopping if one works.
    for strat in strats:
        result = strat(unitary_value, args)
        if result is None:
            break
        if result is not NotImplemented:
            return result

    # Don't know how to apply. Fallback to specified default behavior.
    if default is not RaiseTypeErrorIfNotProvided:
        return default
    raise TypeError(
        "cirq.apply_unitary failed. "
        "Value doesn't have a (non-parameterized) unitary effect.\n"
        "\n"
        "type: {}\n"
        "value: {!r}\n"
        "\n"
        "The value failed to satisfy any of the following criteria:\n"
        "- An `_apply_unitary_(self, args) method that returned a value "
        "besides None or NotImplemented.\n"
        "- A `_unitary_(self)` method that returned a value "
        "besides None or NotImplemented.\n"
        "- A `_decompose_(self)` method that returned a "
        "list of unitary operations.\n"
        "".format(type(unitary_value), unitary_value))


def _strat_apply_unitary_from_apply_unitary(unitary_value: Any,
                                            args: ApplyUnitaryArgs
                                           ) -> Optional[np.ndarray]:
    # Check for magic method.
    func = getattr(unitary_value, '_apply_unitary_', None)
    if func is None:
        return NotImplemented
    op_qid_shape = qid_shape_protocol.qid_shape(unitary_value,
                                                (2,) * len(args.axes))
    sub_args = args._for_operation_with_qid_shape(range(len(op_qid_shape)),
                                                  op_qid_shape)
    sub_result = func(sub_args)
    if sub_result is NotImplemented or sub_result is None:
        return sub_result
    return _incorporate_result_into_target(args, sub_args, sub_result)


def _strat_apply_unitary_from_unitary(unitary_value: Any, args: ApplyUnitaryArgs
                                     ) -> Optional[np.ndarray]:
    # Check for magic method.
    method = getattr(unitary_value, '_unitary_', None)
    if method is None:
        return NotImplemented

    # Attempt to get the unitary matrix.
    matrix = method()
    if matrix is NotImplemented or matrix is None:
        return matrix

    val_qid_shape = qid_shape_protocol.qid_shape(unitary_value,
                                                 default=(2,) * len(args.axes))
    sub_args = args._for_operation_with_qid_shape(range(len(val_qid_shape)),
                                                  val_qid_shape)
    matrix = matrix.astype(sub_args.target_tensor.dtype)
    if len(val_qid_shape) == 1 and val_qid_shape[0] <= 2:
        # Special case for single-qubit, 2x2 or 1x1 operations.
        # np.einsum is faster for larger cases.
        subspaces = [(..., level) for level in range(val_qid_shape[0])]
        sub_result = linalg.apply_matrix_to_slices(
            sub_args.target_tensor,
            matrix,
            subspaces,
            out=sub_args.available_buffer)
    else:
        # General case via np.einsum.
        sub_result = linalg.targeted_left_multiply(
            matrix.reshape(val_qid_shape * 2),
            sub_args.target_tensor,
            sub_args.axes,
            out=sub_args.available_buffer)
    return _incorporate_result_into_target(args, sub_args, sub_result)


def _strat_apply_unitary_from_decompose(val: Any, args: ApplyUnitaryArgs
                                       ) -> Optional[np.ndarray]:
    operations, qubits, _ = _try_decompose_into_operations_and_qubits(val)
    if operations is None:
        return NotImplemented
    return apply_unitaries(operations, qubits, args, None)


def apply_unitaries(unitary_values: Iterable[Any],
                    qubits: Sequence['cirq.Qid'],
                    args: Optional[ApplyUnitaryArgs] = None,
                    default: Any = RaiseTypeErrorIfNotProvided
                   ) -> Optional[np.ndarray]:
    """Apply a series of unitaries onto a state tensor.

    Uses `cirq.apply_unitary` on each of the unitary values, to apply them to
    the state tensor from the `args` argument.

    CAUTION: if one of the given unitary values does not have a unitary effect,
    forcing the method to terminate, the method will not rollback changes
    from previous unitary values.

    Args:
        unitary_values: The values with unitary effects to apply to the target.
        qubits: The qubits that will be targeted by the unitary values. These
            qubits match up, index by index, with the `indices` property of the
            `args` argument.
        args: A mutable `cirq.ApplyUnitaryArgs` object describing the target
            tensor, available workspace, and axes to operate on. The attributes
            of this object will be mutated as part of computing the result. If
            not specified, this defaults to the zero state of the given qubits
            with an axis ordering matching the given qubit ordering.
        default: What should be returned if any of the unitary values actually
            don't have a unitary effect. If not specified, a TypeError is
            raised instead of returning a default value.

    Returns:
        If any of the unitary values do not have a unitary effect, the
        specified default value is returned (or a TypeError is raised).
        CAUTION: If this occurs, the contents of `args.target_tensor`
        and `args.available_buffer` may have been mutated.

        If all of the unitary values had a unitary effect that was
        successfully applied, this method returns the `np.ndarray`
        storing the final result. This `np.ndarray` may be
        `args.target_tensor`, `args.available_buffer`, or some
        other instance. The caller is responsible for dealing with
        this potential aliasing of the inputs and the result.

    Raises:
        TypeError: An item from `unitary_values` doesn't have a unitary effect
            and `default` wasn't specified.
    """
    if args is None:
        qid_shape = qid_shape_protocol.qid_shape(qubits)
        args = ApplyUnitaryArgs.default(qid_shape=qid_shape)
    if len(qubits) != len(args.axes):
        raise ValueError('len(qubits) != len(args.axes)')
    qubit_map = {
        q.with_dimension(1): args.axes[i] for i, q in enumerate(qubits)
    }
    state = args.target_tensor
    buffer = args.available_buffer

    for op in unitary_values:
        indices = [qubit_map[q.with_dimension(1)] for q in op.qubits]
        result = apply_unitary(unitary_value=op,
                               args=ApplyUnitaryArgs(state, buffer, indices),
                               default=None)

        # Handle failure.
        if result is None:
            if default is RaiseTypeErrorIfNotProvided:
                raise TypeError(
                    "cirq.apply_unitaries failed. "
                    "There was a non-unitary value in the `unitary_values` "
                    "list.\n"
                    "\n"
                    "non-unitary value type: {}\n"
                    "non-unitary value: {!r}".format(type(op), op))
            return default

        # Handle aliasing of results.
        if result is buffer:
            buffer = state
        state = result

    return state


def _incorporate_result_into_target(args: 'ApplyUnitaryArgs',
                                    sub_args: 'ApplyUnitaryArgs',
                                    sub_result: np.ndarray):
    """Takes the result of calling `_apply_unitary_` on `sub_args` and
    copies it back into `args.target_tensor` or `args.available_buffer` as
    necessary to return the result of applying the unitary to the full args.
    Also swaps the buffers so the result is always in `args.target_tensor`.

    Args:
        args: The original args.
        sub_args: A version of `args` with transposed and sliced views of
            it's tensors.
        sub_result: The result of calling an object's `_apply_unitary_`
            method on `sub_args`.  A transposed subspace of the desired
            result.

    Returns: The full result tensor after applying the unitary.  Always
        `args.target_tensor`.
    """
    if not (np.may_share_memory(args.target_tensor, sub_args.target_tensor) and
            np.may_share_memory(args.available_buffer,
                                sub_args.available_buffer)):
        raise ValueError(
            'sub_args.target_tensor and .available_buffer must be views of '
            'args.target_tensor and .available_buffer respectively.')
    is_subspace = sub_args.target_tensor.size < args.target_tensor.size
    if sub_result is sub_args.target_tensor:
        return args.target_tensor
    if sub_result is sub_args.available_buffer:
        if is_subspace:
            # The subspace that was modified is likely much smaller than
            # the whole tensor so copy sub_result back into target_tensor.
            sub_args.target_tensor[...] = sub_result
            return args.target_tensor
        return args.available_buffer
    # The subspace that was modified is likely much smaller than
    # the whole tensor so copy sub_result back into target_tensor.
    # It's an uncommon case where sub_result is a new array.
    if np.may_share_memory(sub_args.target_tensor, sub_result):
        # Someone did something clever.  E.g. implementing SWAP with a
        # reshape.
        # Copy to available_buffer instead.
        if is_subspace:
            args.available_buffer[...] = args.target_tensor
        sub_args.available_buffer[...] = sub_result
        return args.available_buffer
    sub_args.target_tensor[...] = sub_result
    return args.target_tensor
