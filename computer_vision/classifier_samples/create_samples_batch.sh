#!/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Legend: samples_list_TXT negatives_list_TXT"
else
	samplesListTxt=$1
	negativesListTxt=$2
	basePath=$(dirname $samplesListTxt)
	objectName=$(basename $samplesListTxt .txt)

	#create directory in vector
	mkdir -p vector_files

	mkdir -p "./vector_files/"$objectName
	countSamples=0
	countPositives=0
	countNegatives=0

	perImage=150
	while IFS='' read -r line || [[ -n "$line" ]]; do
		#for each image, create samples
		countSamples=$((countSamples+1))
		echo $basePath"/"$line
		echo $basePath"/" $countSamples".vec"
		opencv_createsamples \
			-bgcolor 0 -bgthresh 0 -pngoutput \
			-maxxangle 0 -maxyangle 0 maxzangle 0 -maxidev 40 \
			-w 40 -h 40 \
			-num $perImage \
			-img $basePath"/"$line \
			-bg $2 \
			-vec "./vector_files/"$objectName"/"$objectName"_"$countSamples".vec"

		countPositives=$((countPositives+$perImage))
	done < "$1"
	countNegatives=$(wc -l < $2)

	#merge vectors
	python mergevec.py -v "./vector_files/"$objectName -o "./vector_files/"$objectName".vec"

	#create directory for classifiers
	mkdir -p classifiers

	mkdir -p "./classifiers/"$objectName
	#start the classifier
	opencv_traincascade -data "./classifiers/"$objectName -vec "./vector_files/"$objectName".vec" -bg $2 \
		-numStages 10 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos $countPositives \
		-numNeg $countNegatives -w 40 -h 40 -mode ALL -precalcValBufSize 1024 \
		-precalcIdxBufSize 2048
fi
