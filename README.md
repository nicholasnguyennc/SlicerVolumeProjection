Volume Projection

Volume Projection is an extension for Slicer.
Load volumes and perform maximum, minimum, mean, and standard deviation projections along axial, sagittal, and coronal axes with customizable bounds.

![Image of UI](https://github.com/nicholasnguyennc/SlicerVolumeProjection/tree/assets/ProjectionUI.png)

Tutorial:
1. In 3D-Slicer, navigate to the Sample Data Module
2. Select the MRHead data set (Slicer will then download and import this set)
3. Open the Volume Projection Module via Modules>Filtering>Volume Projection
4. Load a volume into the scene
5. Select the input volume with the input volume combo box
6. Load/Create a volume with the output volume combo box
7. Adjust the ROI
8. Click the apply projection button to store the projection to the output volume

Contained Modules:
ROIModule - Provides custom Slicer Annotation ROI to bound input volume 
SimpleITK - Performs maximum, minimum, mean, and standard deviation projection operations
Crop Volume Module - Crops data from input volume based upon custom bounds

License: 3D Slicer License (https://github.com/Slicer/Slicer/blob/master/License.txt)


Nicholas Nguyen. SonoVol Inc.
August 2020.
