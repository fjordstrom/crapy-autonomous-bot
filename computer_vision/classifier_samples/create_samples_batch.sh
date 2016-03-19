#!/bin/bash

if [ "$#" -lt 1 ]; then
	echo "??"
else
	samplesListTxt=$1
	negativesListTxt=$2
	basePath=$(dirname $samplesListTxt)
	objectName=$(basename $samplesListTxt .txt)

	#create directory in vector
	mkdir -p vector_files

	mkdir -p $objectName
	countSamples=0
	countPositives=0
	countNegatives=0
	while IFS='' read -r line || [[ -n "$line" ]]; do
		#for each image, create samples
		countSamples=countSamples+1
		echo $basePath"/"$line
		echo $basePath"/" $countSamples".vec"
		opencv_createsamples \
			-bgcolor 0 -bgthresh 0 -pngoutput \
			-maxxangle 1.1 -maxyangle 1.1 maxzangle 0.5 -maxidev 40 \
			-w 40 -h 40 \
			-num 500 \
			-img $basePath"/"$line \
			-bg $2 \
			-vec "./vector_files/"$objectName"/"$objectName"_"$countSamples".vec"

		countPositives=countPositives+500
	done < "$1"
	countNegatives=$(wc -l < $2)

	#merge vectors
	python mergevec.py -v "./vector_files/"$objectName -o "./vector_files/"$objectName".vec"

	#create directory for classifiers
	mkdir -p classifiers

	mkdir -p "./classifiers/"$objectName
	#start the classifier
	opencv_traincascade -data "./classifiers/"$objectName -vec "./vector_files/"$objectName".vec" -bg $2 \
		-numStages 5 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos $countPositives \
		-numNeg $countNegatives -w 40 -h 40 -mode ALL -precalcValBufSize 1024 \
		-precalcIdxBufSize 4096
fi




