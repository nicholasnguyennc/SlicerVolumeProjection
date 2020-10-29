cmake_minimum_required(VERSION 3.13.4)

project(VolumeProjection)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/nicholasnguyennc/SlicerVolumeProjection")
set(EXTENSION_CATEGORY "Filtering")
set(EXTENSION_CONTRIBUTORS "Nicholas Nguyen (SonoVol Inc), Brian Fischer (SonoVol Inc)")
set(EXTENSION_DESCRIPTION "The extension is a tool used to perform maximum, minimum, mean, and standard deviation projections along axial, sagittal, and coronal axes with customizable bounds.")
set(EXTENSION_ICONURL "")
set(EXTENSION_SCREENSHOTURLS "https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/ProjectionUI.png https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/SampleData.png https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/SelectVolume.png https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/CreateVolume.png https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/AdjustROI.png https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/StoredProjection.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(VolumeProjection)

## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
