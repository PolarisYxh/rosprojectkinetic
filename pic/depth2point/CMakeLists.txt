cmake_minimum_required( VERSION 2.8 )
project( joinMap )

set( CMAKE_BUILD_TYPE Release )
set( CMAKE_CXX_FLAGS "-std=c++11 -O3" )
#dubug 模式
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0")
set (CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -g -O0")#-O0不进行调试优化
# opencv 
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

# eigen 
include_directories( "/usr/include/eigen3/" )

# pcl 
find_package( PCL REQUIRED COMPONENT common io )
include_directories( ${PCL_INCLUDE_DIRS} )
add_definitions( ${PCL_DEFINITIONS} )

add_executable(image2pcl image2pcl.cpp )
target_link_libraries(image2pcl ${OpenCV_LIBS} ${PCL_LIBRARIES} )

add_executable(8bitimage2pcl 8bitimage2pcl.cpp )
target_link_libraries(8bitimage2pcl ${OpenCV_LIBS} ${PCL_LIBRARIES} )

add_executable(rotatematrix2rpy rotatematrix2rpy.cpp )