Volume Projection

Volume Projection is an extension for Slicer.
The extension is a GUI tool used to perform maximum, minimum, mean, and standard deviation projections along axial, sagittal, and coronal axes with customizable bounds.

![Image of UI](https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/ProjectionUI.png)

Tutorial:
1. In 3D-Slicer, navigate to the Sample Data Module
2. Select the MRHead data set (Slicer will then download and import this set)

![Image of Data Set](https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/SampleData.png)

3. Open the Volume Projection Module via Modules>Filtering>Volume Projection
4. Select the MRHEAD volume with the input volume combo box

![Select Input](https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/SelectVolume.png)

5. Create a volume with the output volume combo box

![Create Output](https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/CreateVolume.png)

6. Customize the ROI

![CustomizeROI](https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/AdjustROI.png)

7. Click the apply projection button to store the projection to the output volume

![EndResult](https://raw.githubusercontent.com/nicholasnguyennc/SlicerVolumeProjection/assets/StoredProjection.png)

Contained Modules:

ROIModule - Provides custom Slicer Annotation ROI to bound input volume 

SimpleITK - Performs maximum, minimum, mean, and standard deviation projection operations

Crop Volume Module - Crops data from input volume based upon custom bounds

License: 3D Slicer License (https://github.com/Slicer/Slicer/blob/master/License.txt)


Collaborators: Nicholas Nguyen (SonoVol Inc.), Brian Fischer (SonoVol Inc.)

August 2020.
