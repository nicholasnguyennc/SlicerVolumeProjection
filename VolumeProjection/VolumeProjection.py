import os
import unittest
import logging
import traceback
import numpy as np
import SimpleITK as itk
import sitkUtils
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

#
# VolumeProjection
#

class VolumeProjection(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Volume Projection"
        self.parent.contributors = ["Nicholas Nguyen (SonoVol Inc.), Brian Fischer (SonoVol Inc.)"]
        self.parent.categories = ["Filtering"]
#
# VolumeProjectionWidget
#

class VolumeProjectionWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)
        self.logic = None

    def setup(self):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)

        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

        # Load widget from .ui file (created by Qt Designer)
        uiWidget = slicer.util.loadUI(self.resourcePath('UI/VolumeProjection.ui'))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        self.logic = VolumeProjectionLogic()

        # Connections
        self.ui.viewProjectionButton.connect('clicked(bool)', self.onViewButton)
        self.ui.fitROIButton.connect('clicked(bool)', self.onROIButton)
        self.ui.displayROIBox.connect('toggled(bool)', self.changeROIVisibility)

        # On exit
        moduleManager = slicer.app.moduleManager()
        moduleManager.connect('moduleAboutToBeUnloaded(QString)', self.cleanup)

        # Connections to save user changes to settings on GUI (saved to MRML Scene)

        self.ui.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.enableViewButton)
        self.ui.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.enableROIButton)
        self.ui.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.enableViewButton)
        self.ui.inputSelector.setCurrentNodeIndex(-1)
        self.ui.outputSelector.setCurrentNodeIndex(-1)
        y = slicer.mrmlScene.GetNodesByClass('vtkMRMLAnnotationROINode')
        for x in y:
            slicer.mrmlScene.RemoveNode(x)
        y.UnRegister(y)
        z = slicer.mrmlScene.GetNodesByClass('vtkMRMLCropVolumeParametersNode')
        for x in z:
            slicer.mrmlScene.RemoveNode(x)
        z.UnRegister(z)

        widgetROI = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLAnnotationROINode')
        roiParameters = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLCropVolumeParametersNode')
        roiParameters.SetROINodeID(widgetROI.GetID())
        self.widgetROIid = widgetROI.GetID()
        self.roiParametersid = roiParameters.GetID()

    def cleanup(self):
        """
        Called when the application closes and the module widget is destroyed.
        """
        # slicer.mrmlScene.RemoveNode(slicer.mrmlScene.GetNodeByID(self.widgetROIid))
        # slicer.mrmlScene.RemoveNode(slicer.mrmlScene.GetNodeByID(self.roiParametersid))

        self.removeObservers()

    def enableViewButton(self):
        if self.ui.inputSelector.currentNode() and self.ui.outputSelector.currentNode():
            self.ui.viewProjectionButton.enabled = True
        else:
            self.ui.viewProjectionButton.enabled = False

    def enableROIButton(self):
        if self.ui.inputSelector.currentNode():
            self.ui.fitROIButton.enabled = True
        else:
            self.ui.fitROIButton.enabled = False



    def changeROIVisibility(self):
        if self.ui.displayROIBox.isChecked():
            slicer.mrmlScene.GetNodeByID(self.widgetROIid).SetDisplayVisibility(1)
        else:
            slicer.mrmlScene.GetNodeByID(self.widgetROIid).SetDisplayVisibility(0)

    def onROIButton(self):
        if self.ui.inputSelector.currentNode():
            slicer.mrmlScene.GetNodeByID(self.roiParametersid).SetInputVolumeNodeID(self.ui.inputSelector.currentNodeID)
            slicer.modules.cropvolume.logic().FitROIToInputVolume(slicer.mrmlScene.GetNodeByID(self.roiParametersid))
            green_slice_node = slicer.app.layoutManager().sliceWidget('Green').sliceLogic()
            green_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(self.ui.inputSelector.currentNodeID)
            slicer.app.layoutManager().sliceWidget('Green').fitSliceToBackground()
            red_slice_node = slicer.app.layoutManager().sliceWidget('Red').sliceLogic()
            red_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(self.ui.inputSelector.currentNodeID)
            slicer.app.layoutManager().sliceWidget('Red').fitSliceToBackground()
            yellow_slice_node = slicer.app.layoutManager().sliceWidget('Yellow').sliceLogic()
            yellow_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(self.ui.inputSelector.currentNodeID)
            slicer.app.layoutManager().sliceWidget('Yellow').fitSliceToBackground()

    def onViewButton(self):
        '''
        Run processing when user clicks view projection button
        '''
        try:
            self.update(self.ui.inputSelector.currentNodeID, self.ui.outputSelector.currentNodeID)
        except Exception as e:
            slicer.util.errorDisplay("Failed to compute results: " + str(e))
            traceback.print_exc()

    def update(self, inputVolume, outputVolume):

        # 0 is Coronal=Green, 1 is Axial=Red, 2 is Sagittal=Yellow
        axis_of_projection = self.ui.axisComboBox.currentIndex
        projection_type = self.ui.projectionComboBox.currentText

        # reorder the aop b/c of changed order in selector
        if axis_of_projection is 2:
            axis_of_projection = 0
        elif axis_of_projection is 0:
            axis_of_projection = 1
        elif axis_of_projection is 1:
            axis_of_projection = 2

        # Convert numpy array into image data for sitk projection

        slicer.modules.cropvolume.logic().CropVoxelBased(slicer.mrmlScene.GetNodeByID(self.widgetROIid), slicer.mrmlScene.GetNodeByID(inputVolume), slicer.mrmlScene.GetNodeByID(outputVolume), True)
        projection_array = np.copy(slicer.util.arrayFromVolume(slicer.mrmlScene.GetNodeByID(outputVolume)))

        run_function = {'Maximum': lambda array, axis: self.logic.runMax(array, axis), 'Minimum': lambda array, axis: self.logic.runMin(array, axis),
                        'Mean': lambda array, axis: self.logic.runMean(array, axis), 'Standard Deviation': lambda array, axis: self.logic.runStdDev(array, axis)}

        projection_array = run_function[projection_type](projection_array, axis_of_projection)

        slicer.util.updateVolumeFromArray(slicer.mrmlScene.GetNodeByID(outputVolume), projection_array)
        slicer.util.arrayFromVolumeModified(slicer.mrmlScene.GetNodeByID(outputVolume))

        # Change output volume's display data to be the same as the input image
        slicer.mrmlScene.GetNodeByID(outputVolume).CreateDefaultDisplayNodes()
        slicer.mrmlScene.GetNodeByID(outputVolume).GetScalarVolumeDisplayNode().SetAutoWindowLevel(0)

        # Change the slicer ui view to show the projected volume
        # axial = 1, sagitall = 2, coronal = 0
        if self.ui.showProjectionBox.isChecked():
            if axis_of_projection is 0:
                green_slice_node = slicer.app.layoutManager().sliceWidget('Green').sliceLogic()
                green_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(outputVolume)
                slicer.app.layoutManager().sliceWidget('Green').fitSliceToBackground()

                red_slice_node = slicer.app.layoutManager().sliceWidget('Red').sliceLogic()
                red_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(inputVolume)
                slicer.app.layoutManager().sliceWidget('Red').fitSliceToBackground()

                yellow_slice_node = slicer.app.layoutManager().sliceWidget('Yellow').sliceLogic()
                yellow_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(inputVolume)
                slicer.app.layoutManager().sliceWidget('Yellow').fitSliceToBackground()
            elif axis_of_projection is 1:
                red_slice_node = slicer.app.layoutManager().sliceWidget('Red').sliceLogic()
                red_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(outputVolume)
                slicer.app.layoutManager().sliceWidget('Red').fitSliceToBackground()

                yellow_slice_node = slicer.app.layoutManager().sliceWidget('Yellow').sliceLogic()
                yellow_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(inputVolume)
                slicer.app.layoutManager().sliceWidget('Yellow').fitSliceToBackground()

                green_slice_node = slicer.app.layoutManager().sliceWidget('Green').sliceLogic()
                green_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(inputVolume)
                slicer.app.layoutManager().sliceWidget('Green').fitSliceToBackground()
            elif axis_of_projection is 2:
                yellow_slice_node = slicer.app.layoutManager().sliceWidget('Yellow').sliceLogic()
                yellow_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(outputVolume)
                slicer.app.layoutManager().sliceWidget('Yellow').fitSliceToBackground()

                red_slice_node = slicer.app.layoutManager().sliceWidget('Red').sliceLogic()
                red_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(inputVolume)
                slicer.app.layoutManager().sliceWidget('Red').fitSliceToBackground()

                green_slice_node = slicer.app.layoutManager().sliceWidget('Green').sliceLogic()
                green_slice_node.GetSliceCompositeNode().SetBackgroundVolumeID(inputVolume)
                slicer.app.layoutManager().sliceWidget('Green').fitSliceToBackground()

#
# VolumeProjectionLogic
#

class VolumeProjectionLogic(ScriptedLoadableModuleLogic):

    axis_dict = {0: 'Coronal', 1: 'Axial', 2: 'Sagittal'}
    def runMax(self, data, axis):

        image_data = itk.GetImageFromArray(data)
        projectionType = itk.MaximumProjectionImageFilter()
        logging.info('Ran Maximum Projection along %s', self.axis_dict[axis])
        projectionType.SetProjectionDimension(axis)
        proj_array = itk.GetArrayViewFromImage(projectionType.Execute(image_data))
        return proj_array

    def runMin(self, data, axis):
        image_data = itk.GetImageFromArray(data)
        projectionType = itk.MinimumProjectionImageFilter()
        logging.info('Ran Minimum Projection along %s', self.axis_dict[axis])
        proj_array = itk.GetArrayViewFromImage(projectionType.Execute(image_data))
        return proj_array

    def runMean(self, data, axis):
        image_data = itk.GetImageFromArray(data)
        projectionType = itk.MeanProjectionImageFilter()
        logging.info('Ran Mean Projection along %s', self.axis_dict[axis])
        projectionType.SetProjectionDimension(axis)
        proj_array = itk.GetArrayViewFromImage(projectionType.Execute(image_data))
        return proj_array

    def runStdDev(self, data, axis):
        image_data = itk.GetImageFromArray(data)
        projectionType = itk.StandardDeviationProjectionImageFilter()
        logging.info('Ran Standard Deviation Projection along %s', self.axis_dict[axis])
        projectionType.SetProjectionDimension(axis)
        proj_array = itk.GetArrayViewFromImage(projectionType.Execute(image_data))
        return proj_array

#
# VolumeProjectionTest
#


class VolumeProjectionTest():

    def setUp(self):
        slicer.mrmlScene.Clear(0)
    def runTest(self):
        self.setUp()
        self.test_VolumeProjection1()
    def test_VolumeProjection1(self):
        self.delayDisplay("Starting the test")
        self.delayDisplay('Test passed')
