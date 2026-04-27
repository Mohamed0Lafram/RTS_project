// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:msg/SECRET.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "custom_interfaces/msg/secret.hpp"


#ifndef CUSTOM_INTERFACES__MSG__DETAIL__SECRET__BUILDER_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__SECRET__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/msg/detail/secret__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace msg
{

namespace builder
{

class Init_SECRET_data
{
public:
  explicit Init_SECRET_data(::custom_interfaces::msg::SECRET & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::msg::SECRET data(::custom_interfaces::msg::SECRET::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::msg::SECRET msg_;
};

class Init_SECRET_id
{
public:
  Init_SECRET_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SECRET_data id(::custom_interfaces::msg::SECRET::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_SECRET_data(msg_);
  }

private:
  ::custom_interfaces::msg::SECRET msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::msg::SECRET>()
{
  return custom_interfaces::msg::builder::Init_SECRET_id();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__SECRET__BUILDER_HPP_
