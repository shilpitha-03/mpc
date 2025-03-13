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
include tools/recorder/CMakeFiles/rs-record.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include tools/recorder/CMakeFiles/rs-record.dir/compiler_depend.make

# Include the progress variables for this target.
include tools/recorder/CMakeFiles/rs-record.dir/progress.make

# Include the compile flags for this target's objects.
include tools/recorder/CMakeFiles/rs-record.dir/flags.make

tools/recorder/CMakeFiles/rs-record.dir/rs-record.cpp.o: tools/recorder/CMakeFiles/rs-record.dir/flags.make
tools/recorder/CMakeFiles/rs-record.dir/rs-record.cpp.o: /px4_uxrce/camera_ws/librealsense/tools/recorder/rs-record.cpp
tools/recorder/CMakeFiles/rs-record.dir/rs-record.cpp.o: tools/recorder/CMakeFiles/rs-record.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/px4_uxrce/camera_ws/build/librealsense2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object tools/recorder/CMakeFiles/rs-record.dir/rs-record.cpp.o"
	cd /px4_uxrce/camera_ws/build/librealsense2/tools/recorder && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT tools/recorder/CMakeFiles/rs-record.dir/rs-record.cpp.o -MF CMakeFiles/rs-record.dir/rs-record.cpp.o.d -o CMakeFiles/rs-record.dir/rs-record.cpp.o -c /px4_uxrce/camera_ws/librealsense/tools/recorder/rs-record.cpp

tools/recorder/CMakeFiles/rs-record.dir/rs-record.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/rs-record.dir/rs-record.cpp.i"
	cd /px4_uxrce/camera_ws/build/librealsense2/tools/recorder && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /px4_uxrce/camera_ws/librealsense/tools/recorder/rs-record.cpp > CMakeFiles/rs-record.dir/rs-record.cpp.i

tools/recorder/CMakeFiles/rs-record.dir/rs-record.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/rs-record.dir/rs-record.cpp.s"
	cd /px4_uxrce/camera_ws/build/librealsense2/tools/recorder && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /px4_uxrce/camera_ws/librealsense/tools/recorder/rs-record.cpp -o CMakeFiles/rs-record.dir/rs-record.cpp.s

# Object files for target rs-record
rs__record_OBJECTS = \
"CMakeFiles/rs-record.dir/rs-record.cpp.o"

# External object files for target rs-record
rs__record_EXTERNAL_OBJECTS =

Release/rs-record: tools/recorder/CMakeFiles/rs-record.dir/rs-record.cpp.o
Release/rs-record: tools/recorder/CMakeFiles/rs-record.dir/build.make
Release/rs-record: Release/librealsense2.so.2.55.1
Release/rs-record: Release/librsutils.a
Release/rs-record: tools/recorder/CMakeFiles/rs-record.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/px4_uxrce/camera_ws/build/librealsense2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../Release/rs-record"
	cd /px4_uxrce/camera_ws/build/librealsense2/tools/recorder && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rs-record.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tools/recorder/CMakeFiles/rs-record.dir/build: Release/rs-record
.PHONY : tools/recorder/CMakeFiles/rs-record.dir/build

tools/recorder/CMakeFiles/rs-record.dir/clean:
	cd /px4_uxrce/camera_ws/build/librealsense2/tools/recorder && $(CMAKE_COMMAND) -P CMakeFiles/rs-record.dir/cmake_clean.cmake
.PHONY : tools/recorder/CMakeFiles/rs-record.dir/clean

tools/recorder/CMakeFiles/rs-record.dir/depend:
	cd /px4_uxrce/camera_ws/build/librealsense2 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /px4_uxrce/camera_ws/librealsense /px4_uxrce/camera_ws/librealsense/tools/recorder /px4_uxrce/camera_ws/build/librealsense2 /px4_uxrce/camera_ws/build/librealsense2/tools/recorder /px4_uxrce/camera_ws/build/librealsense2/tools/recorder/CMakeFiles/rs-record.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tools/recorder/CMakeFiles/rs-record.dir/depend

