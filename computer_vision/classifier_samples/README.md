Classifier training
===================

Tools for classifier training

`mergevec.py` is from [here](https://github.com/wulfebw/mergevec). Thanks.

The original perl script (not included) and merging code which inspired my approach is from [Naotoshi Seo](http://note.sonots.com/SciSoftware/haartraining.html).

`create_samples_batch.sh` takes two arguments: a text file containing listing for positives, and a text file containing listings for negatives. What it does is it creates samples using OpenCV createsamples for each image, then merges them, and finally trains classifier. Beware this might overtrain or give false positives, since createsamples generates artificial samples by scalling, rotating images.