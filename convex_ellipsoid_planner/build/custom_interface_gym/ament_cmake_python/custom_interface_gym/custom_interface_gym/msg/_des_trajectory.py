# generated from rosidl_generator_py/resource/_idl.py.em
# with input from custom_interface_gym:msg/DesTrajectory.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'matrices_flat'
# Member 'duration_vector'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_DesTrajectory(type):
    """Metaclass of message 'DesTrajectory'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'ACTION_ADD': 1,
        'ACTION_ABORT': 2,
        'ACTION_WARN_START': 3,
        'ACTION_WARN_FINAL': 4,
        'ACTION_WARN_IMPOSSIBLE': 5,
        'ACTION_BACKUP': 6,
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('custom_interface_gym')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'custom_interface_gym.msg.DesTrajectory')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__des_trajectory
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__des_trajectory
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__des_trajectory
            cls._TYPE_SUPPORT = module.type_support_msg__msg__des_trajectory
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__des_trajectory

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'ACTION_ADD': cls.__constants['ACTION_ADD'],
            'ACTION_ABORT': cls.__constants['ACTION_ABORT'],
            'ACTION_WARN_START': cls.__constants['ACTION_WARN_START'],
            'ACTION_WARN_FINAL': cls.__constants['ACTION_WARN_FINAL'],
            'ACTION_WARN_IMPOSSIBLE': cls.__constants['ACTION_WARN_IMPOSSIBLE'],
            'ACTION_BACKUP': cls.__constants['ACTION_BACKUP'],
        }

    @property
    def ACTION_ADD(self):
        """Message constant 'ACTION_ADD'."""
        return Metaclass_DesTrajectory.__constants['ACTION_ADD']

    @property
    def ACTION_ABORT(self):
        """Message constant 'ACTION_ABORT'."""
        return Metaclass_DesTrajectory.__constants['ACTION_ABORT']

    @property
    def ACTION_WARN_START(self):
        """Message constant 'ACTION_WARN_START'."""
        return Metaclass_DesTrajectory.__constants['ACTION_WARN_START']

    @property
    def ACTION_WARN_FINAL(self):
        """Message constant 'ACTION_WARN_FINAL'."""
        return Metaclass_DesTrajectory.__constants['ACTION_WARN_FINAL']

    @property
    def ACTION_WARN_IMPOSSIBLE(self):
        """Message constant 'ACTION_WARN_IMPOSSIBLE'."""
        return Metaclass_DesTrajectory.__constants['ACTION_WARN_IMPOSSIBLE']

    @property
    def ACTION_BACKUP(self):
        """Message constant 'ACTION_BACKUP'."""
        return Metaclass_DesTrajectory.__constants['ACTION_BACKUP']


class DesTrajectory(metaclass=Metaclass_DesTrajectory):
    """
    Message class 'DesTrajectory'.

    Constants:
      ACTION_ADD
      ACTION_ABORT
      ACTION_WARN_START
      ACTION_WARN_FINAL
      ACTION_WARN_IMPOSSIBLE
      ACTION_BACKUP
    """

    __slots__ = [
        '_header',
        '_trajectory_id',
        '_action',
        '_num_order',
        '_num_segment',
        '_matrices_flat',
        '_duration_vector',
        '_debug_info',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'trajectory_id': 'uint32',
        'action': 'uint32',
        'num_order': 'uint32',
        'num_segment': 'uint32',
        'matrices_flat': 'sequence<double>',
        'duration_vector': 'sequence<double>',
        'debug_info': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.trajectory_id = kwargs.get('trajectory_id', int())
        self.action = kwargs.get('action', int())
        self.num_order = kwargs.get('num_order', int())
        self.num_segment = kwargs.get('num_segment', int())
        self.matrices_flat = array.array('d', kwargs.get('matrices_flat', []))
        self.duration_vector = array.array('d', kwargs.get('duration_vector', []))
        self.debug_info = kwargs.get('debug_info', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.trajectory_id != other.trajectory_id:
            return False
        if self.action != other.action:
            return False
        if self.num_order != other.num_order:
            return False
        if self.num_segment != other.num_segment:
            return False
        if self.matrices_flat != other.matrices_flat:
            return False
        if self.duration_vector != other.duration_vector:
            return False
        if self.debug_info != other.debug_info:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def trajectory_id(self):
        """Message field 'trajectory_id'."""
        return self._trajectory_id

    @trajectory_id.setter
    def trajectory_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'trajectory_id' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'trajectory_id' field must be an unsigned integer in [0, 4294967295]"
        self._trajectory_id = value

    @builtins.property
    def action(self):
        """Message field 'action'."""
        return self._action

    @action.setter
    def action(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'action' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'action' field must be an unsigned integer in [0, 4294967295]"
        self._action = value

    @builtins.property
    def num_order(self):
        """Message field 'num_order'."""
        return self._num_order

    @num_order.setter
    def num_order(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'num_order' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'num_order' field must be an unsigned integer in [0, 4294967295]"
        self._num_order = value

    @builtins.property
    def num_segment(self):
        """Message field 'num_segment'."""
        return self._num_segment

    @num_segment.setter
    def num_segment(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'num_segment' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'num_segment' field must be an unsigned integer in [0, 4294967295]"
        self._num_segment = value

    @builtins.property
    def matrices_flat(self):
        """Message field 'matrices_flat'."""
        return self._matrices_flat

    @matrices_flat.setter
    def matrices_flat(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'matrices_flat' array.array() must have the type code of 'd'"
            self._matrices_flat = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'matrices_flat' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._matrices_flat = array.array('d', value)

    @builtins.property
    def duration_vector(self):
        """Message field 'duration_vector'."""
        return self._duration_vector

    @duration_vector.setter
    def duration_vector(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'duration_vector' array.array() must have the type code of 'd'"
            self._duration_vector = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'duration_vector' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._duration_vector = array.array('d', value)

    @builtins.property
    def debug_info(self):
        """Message field 'debug_info'."""
        return self._debug_info

    @debug_info.setter
    def debug_info(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'debug_info' field must be of type 'str'"
        self._debug_info = value
