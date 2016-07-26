# Extended Essay
Here, you can find all of the programs used in the research for my IB Extended Essay on Artificial Neural Networks in the recognition of handwritten digits from the MNIST library.


### NOTICE
Not all files could be included in this repo.  Specifically, the MNIST dataset and the data produced when this program was run were unable to be inculded due to their size.  As such, in order to run this program, you must follow these instructions.

#### Obtaining Generated Data
Please use [this link](https://dl.dropboxusercontent.com/u/93182171/Extended%20Essay/Run%2022.zip) to download the data for Run 22.  Run 22.zip contains all of the data produced during the data collection run of this program.  In order to run the program, this file must be unzipped and its contents placed in a folder with the name "Run 22".  The complete directory should look something like this: `./Data/Run 22/`


#### Downloading MNIST dataset
The copy of the MNIST dataset I used has been provided by Michael Nielsen provided at [this repo] (https://github.com/mnielsen/neural-networks-and-deep-learning.git).  However, as this link or file may be updated, I have included the copy I used as a [download from my Dropbox](https://dl.dropboxusercontent.com/u/93182171/Extended%20Essay/mnist.pkl).  This is solely to ensure that the programming found in this repo is resilient to external changes.  After the download, please place this file in the root directory alongside `mnist.py`.

## Sources
Some of the programs found on this repository uses code snippets from other websites and sources.  I have done my best to reference these snippets here.

### [`map` Function] (https://mail.python.org/pipermail/tutor/2013-August/097291.html)
This function is used in `mnist.py`.

### [Image Loading in `mnist.py`] (https://github.com/colah/nnftd/blob/master/fig/chap3/mnist.py)
This program borrows the function `get_images` from the URL above.
