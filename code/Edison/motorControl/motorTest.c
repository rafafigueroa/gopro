#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> //sleep

#include "motor.h"

int main()
{
	initMotorControl();

	int i = 0;
	
	while (i != 5000)
	{
		printf("Speed (5000 quits):");
		scanf("%i", &i);
		if (i > 128)
			break;
		printf("Testing Speed: %i\n", i);
		setMotorSpeed(1, i);
		//setMotorSpeed(1, 0);
	}
	setMotorSpeed(1,0);
}
