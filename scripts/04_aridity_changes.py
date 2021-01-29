import xarray as xr
import numpy as np
from geopandas import read_file as gpd_read_file

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.family"] = "Arial"
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.25, rc={"lines.linewidth": 2})

exec(open("src/utils.py").read())

# shps
shp_peru = gpd_read_file("data/shps/Sudamérica.shp").to_crs({"init": "epsg:4326"}).iloc[11:12]
shp_peru_no_lake = gpd_read_file("data/shps/Peru_no_lake.shp").to_crs({"init": "epsg:4326"})
shp_drainages = gpd_read_file("data/shps/vertientes.shp").to_crs({"init": "epsg:4326"})
shp_dep = gpd_read_file("data/shps/DEPARTAMENTOS.shp").to_crs({"init": "epsg:4326"})
shp_SA = gpd_read_file("data/shps/Sudamérica.shp").to_crs({"init": "epsg:4326"})
shp_lks = gpd_read_file("data/shps/lago_titicaca_sideteva_puno.shp").to_crs({"init": "epsg:4326"})


# Future Aridity (in RA) discordance
path_files = "data/ARIDEZ_FUTURO/"

ra_hadgem = xr.open_rasterio(path_files + "ARIDEZ_REG_HADGEM.tif")
ra_hadgem = ra_hadgem.where(ra_hadgem > 0)
ra_mpiesm = xr.open_rasterio(path_files + "ARIDEZ_REG_MPIESM.tif")
ra_mpiesm = ra_hadgem.where(ra_mpiesm > 0)
ra_acces = xr.open_rasterio(path_files + "ARIDEZ_REG_ACCES.tif")
ra_acces = ra_acces.where(ra_mpiesm > 0)
ra_future = xr.concat([ra_hadgem, ra_mpiesm, ra_acces], dim="time")

ra_similar = xr.apply_ufunc(similar_subtypes,
                            ra_future,
                            input_core_dims=[['time']],
                            vectorize=True,
                            output_dtypes=['float64'])

# Subtypes transicion from present to future in RA
ra_future_mean = xr.open_rasterio(path_files + "ARIDEZ_REG_PROMF.tif")
ra_future_mean = ra_future_mean.where(ra_future_mean > 0)
ra_future_mean = np.abs(ra_future_mean - 10) # changing order as in aridity_comparison2

ra_present = xr.open_rasterio("data/ARIDEZ_ACTUAL/ARIDEZ_REGIMEN.tif")
ra_present = ra_present.where(ra_present > 0)
ra_present = np.abs(ra_present - 10)

ra_change = xr.apply_ufunc(change_of_RA,
                           ra_present,
                           ra_future_mean,
                           vectorize=True,
                           output_dtypes=['float64'])

fig, (ax, ax1) = plt.subplots(ncols=2, sharey=True, sharex=True, gridspec_kw = {'wspace':0, 'hspace':0}, figsize=(12, 10))

im = ra_change.plot(ax = ax, cmap = "seismic", levels = np.arange(0, 20), add_colorbar=False, center=9.5)
axin = inset_axes(ax, width='5%', height='40%', loc = 'lower left', bbox_to_anchor = (0.06, 0.025, 1 ,1), bbox_transform = ax.transAxes)
cb = plt.colorbar(im, cax=axin, orientation = "vertical", aspect = 7, ticks = np.arange(0.5, 20, 1))
cb.ax.set_yticklabels(['->>',
                       '1 ->',
                       '2 ->',
                       '3 ->',
                       '4 ->',
                       '5 ->',
                       '6 ->',
                       '7 ->',
                       '8 ->',
                       'NC',
                       '<- 9',
                       '<- 8',
                       '<- 7',
                       '<- 6',
                       '<- 5',
                       '<- 4',
                       '<- 3',
                       '<- 2',
                       '<<-'])
cb.ax.set_ylabel('Cambio en RA', labelpad=-35, size = 8)
cb.ax.tick_params(labelsize = 6, pad = 1)

shp_SA.geometry.boundary.plot(ax = ax, edgecolor = "black", linewidth = .5)
shp_dep.geometry.boundary.plot(ax = ax, edgecolor = "black", linewidth = .25)
shp_lks.plot(ax = ax, edgecolor = "deepskyblue", color = "deepskyblue")

ax.set_ylim(-18.5, 0.5)
ax.set_xlim(-81.75, -68)
ax.set_ylabel("")
ax.set_xlabel("")
ax.set_title("")
ax.xaxis.set_tick_params(labelsize = 5, pad=-3)
ax.yaxis.set_tick_params(labelsize = 5, pad=-3)

ax.grid(True, linestyle='--', color = "black", alpha = 0.1)


im = ra_similar.plot(ax=ax1, cmap = "YlOrRd", levels = np.arange(0, 4), add_colorbar=False)
axin = inset_axes(ax1, width='5%', height='30%', loc = 'lower left', bbox_to_anchor = (0.06, 0.025, 1 ,1), bbox_transform = ax1.transAxes)
cb = plt.colorbar(im, cax=axin, orientation = "vertical", aspect = 4, ticks = np.arange(0.5, 3, 1))
cb.ax.set_yticklabels(['CC','V1','V2+'])
cb.ax.set_ylabel('Coincidencia', labelpad=-37, size = 8)
cb.ax.tick_params(labelsize = 7, pad = 1)

shp_SA.geometry.boundary.plot(ax = ax1, edgecolor = "black", linewidth = .5)
shp_dep.geometry.boundary.plot(ax = ax1, edgecolor = "black", linewidth = .25)
shp_lks.plot(ax = ax1, edgecolor = "deepskyblue", color = "deepskyblue")

ax1.set_ylim(-18.5, 0.5)
ax1.set_xlim(-81.75, -68)
ax1.set_ylabel("")
ax1.set_xlabel("")
ax1.set_title("")
ax1.xaxis.set_tick_params(labelsize = 5, pad=-3)
ax1.yaxis.set_tick_params(labelsize = 5, pad=-3)

ax1.grid(True, linestyle='--', color = "black", alpha = 0.1)

plt.savefig('output/aridity_changes.png',
            bbox_inches='tight',pad_inches = 0.01, dpi = 200)

plt.close()