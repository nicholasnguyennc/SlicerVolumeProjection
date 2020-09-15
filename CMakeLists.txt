cmake_minimum_required(VERSION 3.13.4)

project(Volume Projection)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/HeroineInjection")
set(EXTENSION_CATEGORY "Projection")
set(EXTENSION_CONTRIBUTORS "Nicholas Nguyen (Sonovol)")
set(EXTENSION_DESCRIPTION "Volume Projection Thing")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/HeroineInjection.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/HeroineInjection/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(ProjectionWidget)
add_subdirectory(VolumeProjection)

## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
