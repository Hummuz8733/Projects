#!/bin/bash
echo "Today is" $(date)
echo -n "You are in" $(pwd) # -n nie wypisuje endl na końcu dajemy komendy w $() żeby echo nie wypisało nazwy samej 
echo " @" $(hostname)
