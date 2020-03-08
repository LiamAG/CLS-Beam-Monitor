// app.cpp

/*
	Author:	       Liam Graham
	Date Created:  March 5, 2020
	Date Modified: March 5, 2020
	Description:
		TODO: Write file description
*/

#include <iostream>
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#	include <pylon/PylonGUI.h>
#endif
// Include custom headers for utility code and image handler classes
//#include "utils.h"	     // Header file for setup and exectuion functions used by the application

// Get namespaces for std and Pylon functions
using namespace std;
using namespace Pylon;
using namespace GenApi;

const char diagnosticImage[] = "test_caps/grabbedImage.png";
const char backgroundImage[] = "background.png";
const char testImage[] = "test_caps/grabbedImage.png";

const char diagnosticFile[] = "DiagnosticSettings.pfs";
const char singleFile[] = "SingleImageSettings.pfs";

class CImageEventBackground : public CImageEventHandler
{
public:

	virtual void OnImageGrabbed(CInstantCamera& camera, const CGrabResultPtr& ptrGrabResult)
	{
		std::cout << "OnImageGrabbed event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;

		// Image grabbed successfully?
		if (ptrGrabResult->GrabSucceeded())
		{

			// Display the grabbed image.
			Pylon::DisplayImage(1, ptrGrabResult);
			// Save image
			CImagePersistence::Save(ImageFileFormat_Png, backgroundImage, ptrGrabResult);

		}
		else
		{
			std::cout << "Error: " << ptrGrabResult->GetErrorCode() << " " << ptrGrabResult->GetErrorDescription() << std::endl;
		}
	}
};


class CImageEventTestGrab : public CImageEventHandler
{
public:

	virtual void OnImageGrabbed(CInstantCamera& camera, const CGrabResultPtr& ptrGrabResult)
	{
		std::cout << "OnImageGrabbed event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;

		// Image grabbed successfully?
		if (ptrGrabResult->GrabSucceeded())
		{

			// Display the grabbed image.
			Pylon::DisplayImage(1, ptrGrabResult);
			// Save image
			CImagePersistence::Save(ImageFileFormat_Png, testImage, ptrGrabResult);

		}
		else
		{
			std::cout << "Error: " << ptrGrabResult->GetErrorCode() << " " << ptrGrabResult->GetErrorDescription() << std::endl;
		}
	}
};


class CImageEventDiagnostic : public CImageEventHandler
{
public:

	virtual void OnImageGrabbed(CInstantCamera& camera, const CGrabResultPtr& ptrGrabResult)
	{
		std::cout << "OnImageGrabbed event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;

		// Image grabbed successfully?
		if (ptrGrabResult->GrabSucceeded())
		{

			// Display the grabbed image.
			Pylon::DisplayImage(1, ptrGrabResult);
			// Save image
			CImagePersistence::Save(ImageFileFormat_Png, diagnosticImage, ptrGrabResult);

		}
		else
		{
			std::cout << "Error: " << ptrGrabResult->GetErrorCode() << " " << ptrGrabResult->GetErrorDescription() << std::endl;
		}
	}
};

void setupBackground(CInstantCamera& camera)
{
	camera.Open();
	cout << "Camera opened \n";
	CFeaturePersistence::Load(singleFile, &camera.GetNodeMap(), true);
	cout << "Features loaded successfully \n";
	camera.Close();
	cout << "Camera closed \n";
	camera.RegisterConfiguration(new CSoftwareTriggerConfiguration, RegistrationMode_Append, Cleanup_Delete);
	camera.RegisterImageEventHandler(new CImageEventBackground, RegistrationMode_ReplaceAll, Cleanup_Delete);
	cout << "Single image configuration and handlers successfully registered. \n";
}

void setupTestGrab(CInstantCamera& camera)
{
	camera.Open();
	cout << "Camera opened \n";
	CFeaturePersistence::Load(singleFile, &camera.GetNodeMap(), true);
	cout << "Features loaded successfully \n";
	camera.Close();
	cout << "Camera closed \n";
	camera.RegisterConfiguration(new CSoftwareTriggerConfiguration, RegistrationMode_Append, Cleanup_Delete);
	camera.RegisterImageEventHandler(new CImageEventTestGrab, RegistrationMode_ReplaceAll, Cleanup_Delete);
	cout << "Single image configuration and handlers successfully registered. \n";
}

void setupDiagnostic(CInstantCamera& camera)
{
	camera.Open();
	cout << "Camera opened \n";
	CFeaturePersistence::Load(diagnosticFile, &camera.GetNodeMap(), true);
	cout << "Features loaded successfully \n";
	camera.Close();
	cout << "Camera closed \n";
	camera.RegisterImageEventHandler(new CImageEventHandler, RegistrationMode_ReplaceAll, Cleanup_Delete);
	cout << "Diagnostic image event handler successfully registered.\n";
}

int main(int argc, char* argv[])
{
	int exitCode = 0;
	PylonInitialize();
	try
	{
		CInstantCamera camera(CTlFactory::GetInstance().CreateFirstDevice());
		CGrabResultPtr ptrGrabResult;
		cout << "Using device " << camera.GetDeviceInfo().GetModelName() << endl;
		char key;
		cerr << endl << "Welcome to the Beam Doctor diagnostic system at the Canadian Light Source. Please select an option to proceed. Or, enter \"e\" to exit." << endl;
		cerr << endl << "To grab a test image, press \"g\". To capture a background image, enter \"b\". To begin executing beam diagnostics, enter \"d\"." << endl;
		do
		{
			cin.get(key);
			if (key == 'b')
			{
				setupBackground(camera);
				camera.StartGrabbing(GrabStrategy_OneByOne, GrabLoop_ProvidedByInstantCamera);
				char key2;
				do
				{
					cin.get(key2);
					if ((key2 == 't' || key2 == 'T'))
					{
						// Execute the software trigger
						camera.ExecuteSoftwareTrigger();
					}
				} while ((key2 != 'e') && (key2 != 'E'));
				camera.StopGrabbing();
			}
			else if (key == 'g')
			{
				setupTestGrab(camera);
				camera.StartGrabbing(GrabStrategy_OneByOne, GrabLoop_ProvidedByInstantCamera);
				char key2;
				do
				{
					cin.get(key2);
					if ((key2 == 't' || key2 == 'T'))
					{
						// Execute the software trigger
						camera.ExecuteSoftwareTrigger();
					}
				} while ((key2 != 'e') && (key2 != 'E'));
				camera.StopGrabbing();
			}
			else if (key == 'd')
			{
			setupDiagnostic(camera);
			camera.MaxNumBuffer = 1;
				camera.StartGrabbing(GrabStrategy_OneByOne);
				cout << "Grabbing images on line 3 rising edge. Enter \'e'\ to stop.\n";
				while (true)
				{
					camera.RetrieveResult(INFINITE, ptrGrabResult);
					Pylon::DisplayImage(1, ptrGrabResult);
					CImagePersistence::Save(ImageFileFormat_Png, diagnosticImage, ptrGrabResult);
				}
			}
			cerr << endl << "Welcome back, please select a new execution mode, or enter \"e\" to exit." << endl;
		} while ((key != 'e') && (key != 'E'));
		camera.StopGrabbing();

	}
	catch (const GenericException & e)
	{
		// Error handling.
		cerr << "An exception occurred." << endl << e.GetDescription() << endl;
		exitCode = 1;
	}
}