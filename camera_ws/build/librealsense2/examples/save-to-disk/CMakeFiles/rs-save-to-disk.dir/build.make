# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /px4_uxrce/camera_ws/librealsense

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /px4_uxrce/camera_ws/build/librealsense2

# Include any dependencies generated for this target.
include examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/compiler_depend.make

# Include the progress variables for this target.
include examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/progress.make

# Include the compile flags for this target's objects.
include examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/flags.make

examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.o: examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/flags.make
examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.o: /px4_uxrce/camera_ws/librealsense/examples/save-to-disk/rs-save-to-disk.cpp
examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.o: examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/px4_uxrce/camera_ws/build/librealsense2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.o"
	cd /px4_uxrce/camera_ws/build/librealsense2/examples/save-to-disk && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.o -MF CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.o.d -o CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.o -c /px4_uxrce/camera_ws/librealsense/examples/save-to-disk/rs-save-to-disk.cpp

examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.i"
	cd /px4_uxrce/camera_ws/build/librealsense2/examples/save-to-disk && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /px4_uxrce/camera_ws/librealsense/examples/save-to-disk/rs-save-to-disk.cpp > CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.i

examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.s"
	cd /px4_uxrce/camera_ws/build/librealsense2/examples/save-to-disk && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /px4_uxrce/camera_ws/librealsense/examples/save-to-disk/rs-save-to-disk.cpp -o CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.s

# Object files for target rs-save-to-disk
rs__save__to__disk_OBJECTS = \
"CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.o"

# External object files for target rs-save-to-disk
rs__save__to__disk_EXTERNAL_OBJECTS =

Release/rs-save-to-disk: examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/rs-save-to-disk.cpp.o
Release/rs-save-to-disk: examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/build.make
Release/rs-save-to-disk: Release/librealsense2.so.2.55.1
Release/rs-save-to-disk: /usr/lib/x86_64-linux-gnu/libglfw.so.3.3
Release/rs-save-to-disk: /usr/lib/x86_64-linux-gnu/libOpenGL.so
Release/rs-save-to-disk: /usr/lib/x86_64-linux-gnu/libGLX.so
Release/rs-save-to-disk: /usr/lib/x86_64-linux-gnu/libGLU.so
Release/rs-save-to-disk: Release/librsutils.a
Release/rs-save-to-disk: examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/px4_uxrce/camera_ws/build/librealsense2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../Release/rs-save-to-disk"
	cd /px4_uxrce/camera_ws/build/librealsense2/examples/save-to-disk && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rs-save-to-disk.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/build: Release/rs-save-to-disk
.PHONY : examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/build

examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/clean:
	cd /px4_uxrce/camera_ws/build/librealsense2/examples/save-to-disk && $(CMAKE_COMMAND) -P CMakeFiles/rs-save-to-disk.dir/cmake_clean.cmake
.PHONY : examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/clean

examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/depend:
	cd /px4_uxrce/camera_ws/build/librealsense2 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /px4_uxrce/camera_ws/librealsense /px4_uxrce/camera_ws/librealsense/examples/save-to-disk /px4_uxrce/camera_ws/build/librealsense2 /px4_uxrce/camera_ws/build/librealsense2/examples/save-to-disk /px4_uxrce/camera_ws/build/librealsense2/examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/save-to-disk/CMakeFiles/rs-save-to-disk.dir/depend

