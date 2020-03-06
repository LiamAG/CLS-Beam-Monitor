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
#include "utils.h"	     // Header file for setup and exectuion functions used by the application

// Get namespaces for std and Pylon functions
using namespace std;
using namespace Pylon;


void cameraSetup(char option)
{
	// create camera device
	CInstantCamera camera(CTlFactory::GetInstance().CreateFirstDevice());
	// setup configuration appropriate to the selected option
	if ((option == 'r') || (option == 'R'))
	{
		// Run review mode setup function
	}
	else if ((option == 'b') || (option == 'B'))
	{
		// Run background mode setup function
	}
	else if ((option == 'd') || (option == 'D'))
	{
		// Run diagnostic mode setup function
	}
	else
	{
		throw invalid_argument("Invalid selection. Setup option must be \'r\', \'b\', or \'s\'");
	}
}


void cameraRun(char option)
{
	if ((option == 'r') || (option == 'R'))
	{
		// Execute in review mode
	}
	else if ((option == 'b') || (option == 'B'))
	{
		// Execute in background mode
	}
	else if ((option == 'd') || (option == 'D'))
	{
		// Execute in diagnostic mode
	}
	else
	{
		throw invalid_argument("Invalid selection. Setup option must be \"r\", \"b\", or \"d\"");
	}
}


int main(int argc, char* argv[])
{
	char key;
	cerr << endl << "Welcome to the Beam Doctor diagnostic system at the Canadian Light Source. Please select an option to proceed. Or, enter \"e\" to exit." << endl;
	cerr << endl << "To review current settings via video feed, enter \"r\". To capture a background image, enter \"b\". To begin executing beam diagnostics, enter \"d\"." << endl;
	do
	{
		cin.get(key);
		cameraSetup(key);
		cameraRun(key);
		cerr << endl << "Welcome back, please select a new execution mode, or enter \"e\" to exit." << endl;
	} while ((key != 'e') && (key != 'E'));
}