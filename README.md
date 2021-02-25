# MimtPy
MIami Multi Track tools in Python  
MimtpyApp works based on the S1***.he5, exclude_data.txt and inputs floder generated by Mintpy.

## 1. Installation:
Test only on Linux, not sure about MacOS and Windows

### 1.1 Download and setup
Run the following in your terminal to download the development version of MimiPy

```
cd rsmas_insar/source/  
git clone https://github.com/geodesymiami/mimtpy.git  
```

Seting the following environment variables in your environment.bash  

```
export MIMTPY_HOME=${RSMASINSAR_HOME}/sources/MimtPy  
export PYTHONPATH=${PYTHONPATH}:${MIMTPY_HOME}  
export PATH=${PATH}:${MIMTPY_HOME}/mimtpy  
```

### 1.2. the packages used in MimtPy that should be installed

#### via conda
rasterio  
geopandas  
osgeo  

#### install Kite following its handbook
Kite  

## 2. the Pre-requirement of MimtPy

The folder structure of MintPy product should be:  

```
$SCRATCHDIR
-Project1  
--mintpy  
---HDFEOS file  
---inputs  
----geometryRadar.h5
```

## Folder structure after runing mimtpyApp.py:

```
$SCRATCHDIR  
-Project1  
--mintpy  
---HDFEOS file  
---inputs
----geometryRadar.h5
---velocity
----velocity_date1_date2.h5
---displacement
----displacement_date1_date2.h5`
```

## 2. Runing MimtPy

### 2.1 Routine workflow of mimtpyApp.py

MimtPy only use HDFEOS file and geometryRadar.h5 file generated by MintPy. In order to run mimtpyApp.py, you must organize the folder structure as ``2.the Pre-requirement of MimtPy``. 

```
mimtpyApp.py -h/--help #help
mimtpyApp.py <template> # run mimtpy using mimtpyApp.template
```
The example of template can be found in samples folder
Inside the mimtpyApp.py it can generate displacement or velocity between two dates; do concatenation of adjacent trakcs; calculate horizontal and vertical data and plot figures. What's more, mimtpyApp.py can process one or more project as the same time, according to user's setting.

## 2.2 other function in MimtPy

```
### Basic module

mimtpyApp.py: generate files according to mimtpyApp.template 

plot_geotiff.py: plot geotiff files with given *.shp files and gps velocity vector field.

HDFEOS_to_geotiff.py: transferring S1**.he5 file into *.h5 and *.geotiff files based on given dataset name.

### Analysis module

track_offsets.py: concatenate adjacent tracks

multi_transects.py: Extract data along the profiles which are perpendicular to the fault

overlap2horz_vert.py: Calculate horizontal and vertical value from the overlap region between adjacent tracks

### Tool module

H5UNW_to_geotiff.py: transferring *.unw or *.h5 file into geotiff file.

generate_track_polygon.py: Get the footprint scene of each project  

synthetic_S1.py: simulate linear ramps

### Preprocess module

save_geodmod.py: generate files used by Geodmod software.

save_kite.py: generate Kite scene using HDFEOS data.

save_insamp.py: prepare data for Barnhart's InSAMP software (written in Matlab). Please note that the data used by this script must be geocoded.

### RELAX module
generate_script_RELAX_V2.py: generate template files for RELAX. People must given one example file.

gridsearch_ramps_batch_relax: doing gridseach batchlly

gridsearch_ramps_relax: doing gridsearch for one pair of parameter
```

## Access to mintpy data products
Browse through all directories using: https://129.114.104.223/data/HDF5EOS 

Get them via wget using:
```
wget -r -nH --cut-dirs=2 --no-parent --reject="index.html*" --no-check-certificate https://129.114.104.223/data/HDF5EOS/unittestGalapagosSenDT128/mintpy
```
If you have access to jetstream and  your public key is added in the .ssh directory:
```
scp -rp centos@129.114.104.223:/data/HDF5EOS/KashgarSenAT129 .
```
## links to software packages

for Kite:
git clone https://github.com/pyrocko/kite.git

for InSAMP:
git clone https://github.com/williamBarnhart/InSamp.git
