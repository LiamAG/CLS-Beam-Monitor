#pragma once

#include <pylon/PylonIncludes.h>
using namespace Pylon;

// Output directory variables
char diagnosticImage[] = "./test_caps/grabbedImage.png";
char backgroundImage[] = "./background.png";

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