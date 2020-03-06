// utils.h

/*
	Author:        Liam Graham
	Date Created:  March 5, 2020
	Date Modified: March 5, 2020
	Description:
		TODO: Write file description
*/

#pragma once
// Pylon settings files
#include <pylon/PylonIncludes.h>
using namespace Pylon;

const char reviewConfig[] = "PylonSettings.psf";
const char backgroundConfig[] = "background.psf";

// Setup functions
void setupReview();
void setupBackground();
void setupDiagnostic();

// Execution functions
void runReview();
void runBackground();
void runDiagnostic();
/*
class CImageEventBackground : public CImageEventHandler
{
public:
	virtual void OnImageGrabbed(CInstantCamera& camera, const CGrabResultPtr& ptrGrabResult);
};


class CImageEventDiagnostic : public CImageEventHandler
{
public:
	virtual void OnImageGrabbed(CInstantCamera& camera, const CGrabResultPtr& ptrGrabResult);

*/