#!/bin/bash
let sum=0
let n=0
read number
while [ $? != 1 ]#kiedy dostajemy ctrl+d read daje exit code 1
do
	let sum+=number
	let n+=1
	read number
done
let ans=sum/n
echo $ans
