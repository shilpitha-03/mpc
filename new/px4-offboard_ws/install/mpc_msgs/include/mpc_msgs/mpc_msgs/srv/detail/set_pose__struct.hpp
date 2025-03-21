// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mpc_msgs:srv/SetPose.idl
// generated code does not contain a copyright notice

#ifndef MPC_MSGS__SRV__DETAIL__SET_POSE__STRUCT_HPP_
#define MPC_MSGS__SRV__DETAIL__SET_POSE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__mpc_msgs__srv__SetPose_Request __attribute__((deprecated))
#else
# define DEPRECATED__mpc_msgs__srv__SetPose_Request __declspec(deprecated)
#endif

namespace mpc_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetPose_Request_
{
  using Type = SetPose_Request_<ContainerAllocator>;

  explicit SetPose_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pose(_init)
  {
    (void)_init;
  }

  explicit SetPose_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pose(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _pose_type pose;

  // setters for named parameter idiom
  Type & set__pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    mpc_msgs::srv::SetPose_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const mpc_msgs::srv::SetPose_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mpc_msgs::srv::SetPose_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mpc_msgs::srv::SetPose_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mpc_msgs::srv::SetPose_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mpc_msgs::srv::SetPose_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mpc_msgs::srv::SetPose_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mpc_msgs::srv::SetPose_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mpc_msgs::srv::SetPose_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mpc_msgs::srv::SetPose_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mpc_msgs__srv__SetPose_Request
    std::shared_ptr<mpc_msgs::srv::SetPose_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mpc_msgs__srv__SetPose_Request
    std::shared_ptr<mpc_msgs::srv::SetPose_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetPose_Request_ & other) const
  {
    if (this->pose != other.pose) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetPose_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetPose_Request_

// alias to use template instance with default allocator
using SetPose_Request =
  mpc_msgs::srv::SetPose_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace mpc_msgs


#ifndef _WIN32
# define DEPRECATED__mpc_msgs__srv__SetPose_Response __attribute__((deprecated))
#else
# define DEPRECATED__mpc_msgs__srv__SetPose_Response __declspec(deprecated)
#endif

namespace mpc_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetPose_Response_
{
  using Type = SetPose_Response_<ContainerAllocator>;

  explicit SetPose_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->result = false;
    }
  }

  explicit SetPose_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->result = false;
    }
  }

  // field types and members
  using _result_type =
    bool;
  _result_type result;

  // setters for named parameter idiom
  Type & set__result(
    const bool & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    mpc_msgs::srv::SetPose_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const mpc_msgs::srv::SetPose_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mpc_msgs::srv::SetPose_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mpc_msgs::srv::SetPose_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mpc_msgs::srv::SetPose_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mpc_msgs::srv::SetPose_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mpc_msgs::srv::SetPose_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mpc_msgs::srv::SetPose_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mpc_msgs::srv::SetPose_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mpc_msgs::srv::SetPose_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mpc_msgs__srv__SetPose_Response
    std::shared_ptr<mpc_msgs::srv::SetPose_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mpc_msgs__srv__SetPose_Response
    std::shared_ptr<mpc_msgs::srv::SetPose_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetPose_Response_ & other) const
  {
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetPose_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetPose_Response_

// alias to use template instance with default allocator
using SetPose_Response =
  mpc_msgs::srv::SetPose_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace mpc_msgs

namespace mpc_msgs
{

namespace srv
{

struct SetPose
{
  using Request = mpc_msgs::srv::SetPose_Request;
  using Response = mpc_msgs::srv::SetPose_Response;
};

}  // namespace srv

}  // namespace mpc_msgs

#endif  // MPC_MSGS__SRV__DETAIL__SET_POSE__STRUCT_HPP_
