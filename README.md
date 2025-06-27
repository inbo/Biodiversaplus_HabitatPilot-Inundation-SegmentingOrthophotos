# AI for orthomosaics

### Requirements
- Pycharm (community edition) or Visual studio
- Python 3.12 (or 3.13, but then the requirements file must be updated).
- QGIS (e.g. 3.40.4)

### Install python modules
1. Open terminal
2. Type following command in the terminal
~~~shell
pip install -r requirements.txt
~~~

:rocket: Ready to start :rocket:

### General processing steps
1. Modify the hyperparameters in the .env file. 
2. drawRaster.py: makes raster of tiles for DL model, select buffer to be large enough to cover full orthomosaic.
3. correctRaster.py: remove empty boxes (with no pixels).
4. extractTiles.py: crop the orthomosaic to the extent of every box.
5. Label the images using labelme. Type following command in the terminal:

~~~shell
labelme 
~~~

6. Convert_json_to_polygons.py: make shape file with labels.

