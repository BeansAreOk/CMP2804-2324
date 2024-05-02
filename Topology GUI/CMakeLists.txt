# CMakeList.txt : CMake project for Topology GUI, include source and define
# project specific logic here.
#

# Add source to this project's executable.
add_executable (CMakeTarget "Topology GUI.cpp" "Topology GUI.h" "Node.cpp" "Node.h" "Arc.h" "Arc.cpp")

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET CMakeTarget PROPERTY CXX_STANDARD 20)
endif()

# TODO: Add tests and install targets if needed.
include(FetchContent)

FetchContent_Declare(
  yaml-cpp
  GIT_REPOSITORY https://github.com/jbeder/yaml-cpp.git
  GIT_TAG master
)
if(NOT yaml-cpp_POPULATED)
  message(STATUS "Fetching yaml-cpp...")
  FetchContent_Populate(yaml-cpp)
  add_subdirectory(${yaml-cpp_SOURCE_DIR} ${yaml-cpp_BINARY_DIR})
endif()
target_link_libraries(CMakeTarget PRIVATE yaml-cpp::yaml-cpp) # The library or executable that require yaml-cpp library