import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u


# Set the global default colors for the plot
plt.rcParams['text.color'] = '#cccccc'
plt.rcParams['axes.labelcolor'] = '#cccccc'
plt.rcParams['xtick.color'] = '#cccccc'
plt.rcParams['ytick.color'] = '#cccccc'
plt.rcParams['figure.facecolor'] = '#0c0d0d'
plt.rcParams['axes.facecolor'] = '#0c0d0d'

# Load the background image
data = plt.imread("Gaia_EDR3_flux_hammer_8k.png")
#data_flipped = np.fliplr(data)

# Load the dataset
kepler_data = pd.read_csv('kepler.csv')
kepler_data['ra'] = pd.to_numeric(kepler_data['ra'], errors='coerce')
kepler_data['dec'] = pd.to_numeric(kepler_data['dec'], errors='coerce')
kepler_data = kepler_data.dropna(subset=['ra', 'dec'])

# Drop duplicate entries based on 'kepid' to ensure each star system is represented only once
kepler_data = kepler_data.drop_duplicates(subset=['kepid'])

# Iterate through each row and convert from Equatorial coordinates to Galactic coordinates
for i, row in kepler_data.iterrows():
    coord = SkyCoord(ra=row['ra'] * u.degree, dec=row['dec'] * u.degree, frame='icrs')
    galactic_coord = coord.galactic
    
    # Save the Galactic longitude and latitude in the DataFrame
    kepler_data.at[i, 'galactic_l'] = galactic_coord.l.degree
    kepler_data.at[i, 'galactic_b'] = galactic_coord.b.degree

# Convert RA and Dec to radians for plotting
galactic_l = np.radians(kepler_data['galactic_l'])
galactic_b = np.radians(kepler_data['galactic_b'])

# Flip data onto the background star map
galactic_l = -galactic_l
fig = plt.figure(figsize=(16, 8))

# Create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
ax0.imshow(data)
#ax0.imshow(data_flipped)
ax0.axis("off")


# Create Mollweide projection axes in the foreground
ax = fig.add_subplot(111, projection="mollweide", label="polar")
ax.set_facecolor("None") # Make the background of the Mollweide projection transparent

ax.set_xlabel("Galactic l")
ax.set_ylabel("Galactic b")
ax.set_title("Kepler Survey Sky Map", pad=20, color='#cccccc')

plt.grid(True, color='#fcfcfc',alpha=0.2)

# Plot the Kepler data on the Mollweide projection
ax.scatter(galactic_l, galactic_b, s=0.005, alpha=0.1, color='#fcfcfc', marker='.')
plt.savefig('kepler_star_map.png', dpi=300)
#plt.show()