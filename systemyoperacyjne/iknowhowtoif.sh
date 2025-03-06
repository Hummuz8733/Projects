#!/bin/bash
echo "What is your favourite OS?"
read OS
if [ $OS == Windows ]
then 
	echo "I used Windows once. What is that blue screen for?"
elif [ $OS == MacOS ]
then 
	echo "Your OS can do anything as long as it is on AppStore."
elif [ $OS == Linux ]
then 
	echo "Linux is free if your time is worthless."
else
	echo "Is $OS an operating system?"
fi
