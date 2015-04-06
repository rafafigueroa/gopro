#include <stdio.h>
#include <fcntl.h>

void writeString(char *str)
{
	int i = 0;
	int j = 0;
	char buf[250];

	printf("Writing %s\n", str);
	sprintf(buf, "echo '   %s' > /dev/ttyUSB0", str);
	system(buf);
}
	
void initConsoleMC()
{

	system("stty -F /dev/ttyUSB0 speed 115200 raw");
}


void consoleSetSpeed(int spd)
{
	
	char buf[25];

	sprintf(buf, "     %+04i", spd);
	writeString(buf);
}
