// ImageHandlers.h

/*
	Author:        Liam Graham
	Date Created:  March 5, 2020
	Date Modified: March 5, 2020
	Description:
		TODO: Write file description
*/

#pragma once

#include <pylon/PylonIncludes.h>
using namespace Pylon;

// Output directory variables
const char diagnosticImage[] = "test_caps/grabbedImage.png";
const char backgroundImage[] = "background.png";


// Image handler override classes
class CImageEventBackground : public CImageEventHandler
{
public:
	virtual void OnImageGrabbed(CInstantCamera& camera, const CGrabResultPtr& ptrGrabResult);
};


class CImageEventDiagnostic : public CImageEventHandler
{
public:
	virtual void OnImageGrabbed(CInstantCamera& camera, const CGrabResultPtr& ptrGrabResult);
};