#include <stdio.h>

#include "consoleMC.h"


int main()
{
	int spd;

	initConsoleMC();
	while(1)
	{
		printf("Speed:");
		scanf("%i", &spd);
		consoleSetSpeed(spd);
	}
}

		
