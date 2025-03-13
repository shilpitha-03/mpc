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
include examples/C/depth/CMakeFiles/rs-depth.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include examples/C/depth/CMakeFiles/rs-depth.dir/compiler_depend.make

# Include the progress variables for this target.
include examples/C/depth/CMakeFiles/rs-depth.dir/progress.make

# Include the compile flags for this target's objects.
include examples/C/depth/CMakeFiles/rs-depth.dir/flags.make

examples/C/depth/CMakeFiles/rs-depth.dir/rs-depth.c.o: examples/C/depth/CMakeFiles/rs-depth.dir/flags.make
examples/C/depth/CMakeFiles/rs-depth.dir/rs-depth.c.o: /px4_uxrce/camera_ws/librealsense/examples/C/depth/rs-depth.c
examples/C/depth/CMakeFiles/rs-depth.dir/rs-depth.c.o: examples/C/depth/CMakeFiles/rs-depth.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/px4_uxrce/camera_ws/build/librealsense2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object examples/C/depth/CMakeFiles/rs-depth.dir/rs-depth.c.o"
	cd /px4_uxrce/camera_ws/build/librealsense2/examples/C/depth && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT examples/C/depth/CMakeFiles/rs-depth.dir/rs-depth.c.o -MF CMakeFiles/rs-depth.dir/rs-depth.c.o.d -o CMakeFiles/rs-depth.dir/rs-depth.c.o -c /px4_uxrce/camera_ws/librealsense/examples/C/depth/rs-depth.c

examples/C/depth/CMakeFiles/rs-depth.dir/rs-depth.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rs-depth.dir/rs-depth.c.i"
	cd /px4_uxrce/camera_ws/build/librealsense2/examples/C/depth && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /px4_uxrce/camera_ws/librealsense/examples/C/depth/rs-depth.c > CMakeFiles/rs-depth.dir/rs-depth.c.i

examples/C/depth/CMakeFiles/rs-depth.dir/rs-depth.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rs-depth.dir/rs-depth.c.s"
	cd /px4_uxrce/camera_ws/build/librealsense2/examples/C/depth && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /px4_uxrce/camera_ws/librealsense/examples/C/depth/rs-depth.c -o CMakeFiles/rs-depth.dir/rs-depth.c.s

# Object files for target rs-depth
rs__depth_OBJECTS = \
"CMakeFiles/rs-depth.dir/rs-depth.c.o"

# External object files for target rs-depth
rs__depth_EXTERNAL_OBJECTS =

Release/rs-depth: examples/C/depth/CMakeFiles/rs-depth.dir/rs-depth.c.o
Release/rs-depth: examples/C/depth/CMakeFiles/rs-depth.dir/build.make
Release/rs-depth: Release/librealsense2.so.2.55.1
Release/rs-depth: /usr/lib/x86_64-linux-gnu/libglfw.so.3.3
Release/rs-depth: /usr/lib/x86_64-linux-gnu/libOpenGL.so
Release/rs-depth: /usr/lib/x86_64-linux-gnu/libGLX.so
Release/rs-depth: /usr/lib/x86_64-linux-gnu/libGLU.so
Release/rs-depth: Release/librsutils.a
Release/rs-depth: examples/C/depth/CMakeFiles/rs-depth.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/px4_uxrce/camera_ws/build/librealsense2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../../Release/rs-depth"
	cd /px4_uxrce/camera_ws/build/librealsense2/examples/C/depth && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rs-depth.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/C/depth/CMakeFiles/rs-depth.dir/build: Release/rs-depth
.PHONY : examples/C/depth/CMakeFiles/rs-depth.dir/build

examples/C/depth/CMakeFiles/rs-depth.dir/clean:
	cd /px4_uxrce/camera_ws/build/librealsense2/examples/C/depth && $(CMAKE_COMMAND) -P CMakeFiles/rs-depth.dir/cmake_clean.cmake
.PHONY : examples/C/depth/CMakeFiles/rs-depth.dir/clean

examples/C/depth/CMakeFiles/rs-depth.dir/depend:
	cd /px4_uxrce/camera_ws/build/librealsense2 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /px4_uxrce/camera_ws/librealsense /px4_uxrce/camera_ws/librealsense/examples/C/depth /px4_uxrce/camera_ws/build/librealsense2 /px4_uxrce/camera_ws/build/librealsense2/examples/C/depth /px4_uxrce/camera_ws/build/librealsense2/examples/C/depth/CMakeFiles/rs-depth.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/C/depth/CMakeFiles/rs-depth.dir/depend

