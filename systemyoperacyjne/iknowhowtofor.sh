#!/bin/bash
array=("I used Windows" "I used MacOS" "I used Linux" "I must try BSD.")
let i=0
while [ $i -lt ${#array[@]} ]# -lt to less than, # daje ilość elementów w tablicy
do 
	echo ${array[i]}#ita komórka
	let i+=1
done

