// camera.cpp

/*
	Author:		   Liam Graham
	Date Created:  March 3, 2020
	Date Modified: March 3, 2020
	Description:
	This file handles end-to-end operation of the Basler camera
	used with the 2019-2020 EP Capstone project at the CLS.
	Currently, the program grabs images every second, saving them 
	to a hardcoded output directory.
*/

// Include files to use the pylon API
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#	include <pylon/PylonGUI.h>
#endif

// Namespace for using pylong objects
using namespace Pylon;

// Standard namespace
using namespace std;

// Name of pylon feature stream file
const char streamFile[] = "camerasetting.pfs";

class CImageEventPrinter : public CImageEventHandler
{
public:

	virtual void OnImageGrabbed(CInstantCamera& camera, const CGrabResultPtr& ptrGrabResult)
	{
		std::cout << "OnImageGrabbed event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;

		// Image grabbed successfully?
		if (ptrGrabResult->GrabSucceeded())
		{
			std::cout << "SizeX: " << ptrGrabResult->GetWidth() << std::endl;
			std::cout << "SizeY: " << ptrGrabResult->GetHeight() << std::endl;
			const uint8_t* pImageBuffer = (uint8_t*)ptrGrabResult->GetBuffer();
			std::cout << "Gray value of first pixel: " << (uint32_t)pImageBuffer[0] << std::endl;
			std::cout << std::endl;
			// Save image?
			CImagePersistence::Save(ImageFileFormat_Png, "GrabbedImage.png", ptrGrabResult);
		}
		else
		{
			std::cout << "Error: " << ptrGrabResult->GetErrorCode() << " " << ptrGrabResult->GetErrorDescription() << std::endl;
		}
	}
};


int main(int argc, char* argv[])
{
	// Application exit code
	int exitCode = 0;

	// Initialize pylon runtime
	PylonInitialize();

	try
	{
		// Create an instant camera object
		CInstantCamera camera(CTlFactory::GetInstance().CreateFirstDevice());

		// Register software triggering configurations
		camera.RegisterConfiguration(new CSoftwareTriggerConfiguration, RegistrationMode_ReplaceAll, Cleanup_Delete);
		camera.RegisterImageEventHandler(new CImageEventPrinter, RegistrationMode_Append, Cleanup_Delete);


		// Print camera model name
		cout << "Using device" << camera.GetDeviceInfo().GetModelName() << endl;

		// Set up grab result pointer
		CGrabResultPtr ptrGrabResult;
		if (camera.CanWaitForFrameTriggerReady())
		{
			// Start the grabbing using the grab loop thread, by setting the grabLoopType parameter
			// to GrabLoop_ProvidedByInstantCamera. The grab results are delivered to the image event handlers.
			// The GrabStrategy_OneByOne default grab strategy is used.
			camera.StartGrabbing(GrabStrategy_OneByOne, GrabLoop_ProvidedByInstantCamera);

			cerr << endl << "Enter \"t\" to trigger the camera or \"e\" to exit and press enter? (t/e)" << endl << endl;

			// Wait for user input to trigger the camera or exit the program.
			// The grabbing is stopped, the device is closed and destroyed automatically when the camera object goes out of scope.
			char key;
			do
			{
				cin.get(key);
				if ((key == 't' || key == 'T'))
				{
					// Execute the software trigger. Wait up to 500 ms for the camera to be ready for trigger.
					if (camera.WaitForFrameTriggerReady(500, TimeoutHandling_ThrowException))
					{
						camera.ExecuteSoftwareTrigger();
					}
				}

			} while ((key != 'e') && (key != 'E'));
		}
		else
		{
			// See the documentation of CInstantCamera::CanWaitForFrameTriggerReady() for more information.
			cout << endl;
			cout << "This sample can only be used with cameras that can be queried whether they are ready to accept the next frame trigger.";
			cout << endl;
			cout << endl;
		}
	}
	catch (const GenericException &e)
	{

	}
}