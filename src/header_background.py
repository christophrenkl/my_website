#!/usr/bin/env python

# modules tom import
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import cmocean.cm as cmo
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr


# warnings.simplefilter('ignore') # filter some warning messages

def main():

    # data URL
    url = 'https://www.ncei.noaa.gov/thredds/dodsC/OisstBase/NetCDF/V2.1/AVHRR/202012/oisst-avhrr-v02r01.20201210_preliminary.nc'

    # access data
    ds = xr.open_dataset(url)

    ### Plotting #####
    
    proj = ccrs.Orthographic(central_longitude=-40.,
                             central_latitude=20.)

    # resolve longitude wrap-around
    sst_cyc, lon_cyc = add_cyclic_point(ds.sst, coord=ds.lon)
    ice_cyc, _ = add_cyclic_point(ds.ice.fillna(-.1), coord=ds.lon)

    # create figure
    fig, (ax1, ax2), = plt.subplots(1, 2, figsize=(15, 7.5),
                                    subplot_kw={'projection': proj})    

    ax1.remove()

    ax2.set_global()
    ax2.background_patch.set_facecolor('k')

    ax2.contourf(lon_cyc, ds.lat, sst_cyc.squeeze(),
                 levels=np.linspace(-2, 26, 29),
                 cmap=cmo.thermal,
                 extend='both',
                 transform=ccrs.PlateCarree())

    ax2.contourf(lon_cyc, ds.lat, ice_cyc.squeeze(),
                 levels=np.linspace(0, 1, 255),
                 cmap=cmo.ice,
                 transform=ccrs.PlateCarree(),
                 zorder=1)
    
    ax2.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m'),
                    edgecolor='none',
                    facecolor='k')

    # save figure
    fig.canvas.draw()
    fig.tight_layout()
    fig.savefig('static/media/headers/header_background.png',
                dpi=300)


if __name__ == '__main__':

    # run main method
    main()
