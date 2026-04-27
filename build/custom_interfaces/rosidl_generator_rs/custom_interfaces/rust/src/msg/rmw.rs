#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "custom_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__custom_interfaces__msg__SECRET() -> *const std::ffi::c_void;
}

#[link(name = "custom_interfaces__rosidl_generator_c")]
extern "C" {
    fn custom_interfaces__msg__SECRET__init(msg: *mut SECRET) -> bool;
    fn custom_interfaces__msg__SECRET__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SECRET>, size: usize) -> bool;
    fn custom_interfaces__msg__SECRET__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SECRET>);
    fn custom_interfaces__msg__SECRET__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SECRET>, out_seq: *mut rosidl_runtime_rs::Sequence<SECRET>) -> bool;
}

// Corresponds to custom_interfaces__msg__SECRET
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SECRET {

    // This member is not documented.
    #[allow(missing_docs)]
    pub id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub data: rosidl_runtime_rs::String,

}



impl Default for SECRET {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !custom_interfaces__msg__SECRET__init(&mut msg as *mut _) {
        panic!("Call to custom_interfaces__msg__SECRET__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SECRET {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { custom_interfaces__msg__SECRET__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { custom_interfaces__msg__SECRET__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { custom_interfaces__msg__SECRET__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SECRET {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SECRET where Self: Sized {
  const TYPE_NAME: &'static str = "custom_interfaces/msg/SECRET";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__custom_interfaces__msg__SECRET() }
  }
}


