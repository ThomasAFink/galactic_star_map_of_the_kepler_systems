# Galactic Star Map of The Kepler Systems
This repository contains the code for generating a Galactic Star Map of all stars mapped by NASA's Kepler / K2 Telescope. The Kepler mission has provided an unprecedented dataset for identifying exoplanets in our galaxy downloaded from Kaggle at https://www.kaggle.com/datasets/nasa/kepler-exoplanet-search-results and the background 60MB starmap is provided by ESA's Gaia satellite downloaded from https://sci.esa.int/web/gaia/-/60169-gaia-s-sky-in-colour. This is a simple visualalization of the positions of the Kepler star systems.


## Importing Libraries
```
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
```
This section imports essential Python libraries for data handling and visualization. numpy is used for numerical operations, matplotlib.pyplot for plotting, pandas for data manipulation, and astropy components for astronomical calculations, specifically for converting celestial coordinates.

## Setting Global Plot Aesthetics
```
plt.rcParams['text.color'] = '#cccccc'
plt.rcParams['axes.labelcolor'] = '#cccccc'
plt.rcParams['xtick.color'] = '#cccccc'
plt.rcParams['ytick.color'] = '#cccccc'
plt.rcParams['figure.facecolor'] = '#0c0d0d'
plt.rcParams['axes.facecolor'] = '#0c0d0d'
```
This part of the code customizes the appearance of the plots. It sets the colors of text, labels, ticks, and the background to ensure the plot is visually coherent and aesthetically pleasing against a dark background, mimicking a night sky.

## Loading the Data and Pre-processing
```
data = plt.imread("kepler/Gaia_EDR3_flux_hammer_8k.png")
kepler_data = pd.read_csv('kepler.csv')
kepler_data['ra'] = pd.to_numeric(kepler_data['ra'], errors='coerce')
kepler_data['dec'] = pd.to_numeric(kepler_data['dec'], errors='coerce')
kepler_data = kepler_data.dropna(subset=['ra', 'dec'])
```

Here, the background image for the plot is loaded, and the Kepler dataset is read from a CSV file. The ra (right ascension) and dec (declination) columns are converted to numeric types, handling non-numeric values gracefully by coercing them to NaNs and then dropping any rows with NaNs in these crucial columns. This ensures the dataset is clean and ready for further processing.

## Coordinate Transformation
```
for i, row in kepler_data.iterrows():
    coord = SkyCoord(ra=row['ra'] * u.degree, dec=row['dec'] * u.degree, frame='icrs')
    galactic_coord = coord.galactic
    kepler_data.at[i, 'galactic_l'] = galactic_coord.l.degree
    kepler_data.at[i, 'galactic_b'] = galactic_coord.b.degree
```
In this loop, each star's coordinates are transformed from the Equatorial system (right ascension and declination) to the Galactic coordinate system (longitude and latitude). This step aligns the stars according to the Milky Way's structure, preparing the data for a galactic-centric visualization.

## Adjusting and Plotting the Data
```
galactic_l = np.radians(kepler_data['galactic_l'])
galactic_b = np.radians(kepler_data['galactic_b'])
galactic_l = -galactic_l
```
The Galactic longitude (galactic_l) is converted to radians and then inverted to align with the orientation of the Milky Way in the background image. This ensures that the data visualization accurately reflects the stars' positions within the galaxy.

## Creating the Visualization
```
fig = plt.figure(figsize=(12, 8))
ax0 = fig.add_subplot(111)
ax0.imshow(data)
ax0.axis("off")
ax = fig.add_subplot(111, projection="mollweide", label="polar")
ax.set_facecolor("None")
ax.set_xlabel("Galactic l")
ax.set_ylabel("Galactic b")
ax.set_title("Kepler Survey Sky Map", pad=20, color='#cccccc')
plt.grid(True, color='#fcfcfc', alpha=0.2)
ax.scatter(galactic_l, galactic_b, s=0.001, alpha=0.1, color='#fcfcfc', marker='.')
```

A figure is created with a subplot for displaying the background image of the Milky Way. Another subplot using the Mollweide projection overlays the Kepler data on top of this background. The subplot for the data is made transparent so the background image is visible. The plot is then customized with labels for Galactic longitude and latitude, a title, and a customized grid. The Kepler data is plotted with small, semi-transparent white dots to represent stars, ensuring the visualization is both informative and visually appealing.

## Conclusion
This code creates a detailed and visually engaging map of stars observed by the Kepler telescope, plotted over an image of the Milky Way. The transformation of coordinates to the Galactic system and the careful customization of the plot's aesthetics ensure that the visualization is not only scientifically accurate but also accessible and educational for viewers, highlighting the distribution of exoplanet-host


