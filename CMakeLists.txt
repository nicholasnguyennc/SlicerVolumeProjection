cmake_minimum_required(VERSION 3.13.4)

project(Volume Projection Projection)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/VolumeProjection")
set(EXTENSION_CATEGORY "Filtering")
set(EXTENSION_CONTRIBUTORS "Nicholas Nguyen (SonoVol Inc), Brian Fischer (SonoVol Inc)")
set(EXTENSION_DESCRIPTION "Volume Projection is an extension for Slicer. Load volumes and perform maximum, minimum, mean, and standard deviation projections along axial, sagittal, and coronal axes with customizable bounds.")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/VolumeProjection.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/VolumeProjection/Screenshots/1.png")
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
