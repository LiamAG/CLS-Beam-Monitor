// utils.cpp

/*
	Author:        Liam Graham
	Date Created:  March 5, 2020
	Date Modified: March 5, 2020
	Description:
		TODO: Write file description
*/
/*
#include <pylon/PylonIncludes.h>
//#include "ImageHandlers.h"
#ifdef PYLON_WIN_BUILD
#	include <pylon/PylonGUI.h>
#endif
#include "utils.h"

//Setup functions for camera modes
const char diagnosticImage[] = "test_caps/grabbedImage.png";
const char backgroundImage[] = "background.png";

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

CInstantCamera camera(CTlFactory::GetInstance().CreateFirstDevice());
CGrabResultPtr ptrGrabResult;

void setupReview(void)
{
	// Register preset review configuration
	camera.Open();
	CFeaturePersistence::Load(reviewConfig, &camera.GetNodeMap(), true);
	camera.Close();

	// Provide functionality to change parameters? (gamma, etc.)
}


void setupBackground(void)
{
	// set camera up for single frame acquisition and background image events
	camera.Open();
	CFeaturePersistence::Load(backgroundConfig, &camera.GetNodeMap(), true);
	camera.Close();
	camera.RegisterImageEventHandler(new CImageEventBackground, RegistrationMode_Append, Cleanup_Delete);
}


void setupDiagnostic(void)
{
	// figure out how to set up for hardware acquisition OR just make a file you're happy with
	camera.RegisterImageEventHandler(new CImageEventDiagnostic, RegistrationMode_Append, Cleanup_Delete);
}


void runBackground(void)
{
	camera.GrabOne(1000, ptrGrabResult);
}
*/