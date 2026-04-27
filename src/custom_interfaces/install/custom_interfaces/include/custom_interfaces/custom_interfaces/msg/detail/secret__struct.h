// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_interfaces:msg/SECRET.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "custom_interfaces/msg/secret.h"


#ifndef CUSTOM_INTERFACES__MSG__DETAIL__SECRET__STRUCT_H_
#define CUSTOM_INTERFACES__MSG__DETAIL__SECRET__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'id'
// Member 'data'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/SECRET in the package custom_interfaces.
typedef struct custom_interfaces__msg__SECRET
{
  rosidl_runtime_c__String id;
  rosidl_runtime_c__String data;
} custom_interfaces__msg__SECRET;

// Struct for a sequence of custom_interfaces__msg__SECRET.
typedef struct custom_interfaces__msg__SECRET__Sequence
{
  custom_interfaces__msg__SECRET * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_interfaces__msg__SECRET__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__SECRET__STRUCT_H_
