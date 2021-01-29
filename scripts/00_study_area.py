import numpy as np
from geopandas import read_file as gpd_read_file
import xarray as xr

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import seaborn as sns

plt.rcParams["font.family"] = "Arial"
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.25, rc={"lines.linewidth": 2})

# shps
shp_peru = gpd_read_file("data/shps/Sudamérica.shp").to_crs({"init": "epsg:4326"}).iloc[11:12]
shp_peru_no_lake = gpd_read_file("data/shps/Peru_no_lake.shp").to_crs({"init": "epsg:4326"})
shp_drainages = gpd_read_file("data/shps/vertientes.shp").to_crs({"init": "epsg:4326"})
shp_dep = gpd_read_file("data/shps/DEPARTAMENTOS.shp").to_crs({"init": "epsg:4326"})
shp_SA = gpd_read_file("data/shps/Sudamérica.shp").to_crs({"init": "epsg:4326"})
shp_lks = gpd_read_file("data/shps/lago_titicaca_sideteva_puno.shp").to_crs({"init": "epsg:4326"})

# gridded
pisco_p = xr.open_rasterio("data/CLIMA_ACTUAL/PPT/PPT_01.tif")
pisco_p = pisco_p.reindex(y=np.arange(-0.039, -18.347, -0.01),
                          x=np.arange(-81.327, -68.653, 0.01), method="nearest")
pisco_p = pisco_p.where(pisco_p > 0)

pisco_tx = xr.open_rasterio("data/CLIMA_ACTUAL/TMAX/TMAX_01.tif")
pisco_tx = pisco_tx.reindex(y=np.arange(-0.039, -18.347, -0.01),
                            x=np.arange(-81.327, -68.653, 0.01), method="nearest")
pisco_tx = pisco_tx.where(pisco_tx > 0)

rs_data = xr.open_rasterio("data/CLIMA_ACTUAL/RS/RS_01.tif")
rs_data = rs_data.where(rs_data > 0).\
    reindex(y=np.arange(-0.039, -18.347, -0.01),
            x=np.arange(-81.327, -68.653, 0.01), method="nearest")


# figure
fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize = (11, 8),
                                    dpi = 300, sharey=True, gridspec_kw = {'wspace':0, 'hspace':0})

plot_b = pisco_p.plot(ax = ax0, cmap='viridis_r',
                      add_colorbar=False, levels= [0, 10, 50, 100, 200, 900])
axin = inset_axes(ax0, width='4%', height='35%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax0.transAxes)
cb = plt.colorbar(plot_b, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('Precipitación ($mm$)', labelpad=-30, size = 6)
cb.ax.tick_params(labelsize = 6, pad = 0)

#shp_drainages.geometry.boundary.plot(ax = ax0, edgecolor = "black", linewidth = .75)
shp_SA.geometry.boundary.plot(ax = ax0, edgecolor = "black", linewidth = .5)
shp_dep.geometry.boundary.plot(ax = ax0, edgecolor = "black", linewidth = .25)
shp_lks.plot(ax = ax0, edgecolor = "deepskyblue", color = "deepskyblue")

ax0.set_ylim(-18.5, 0.5)
ax0.set_xlim(-81.75, -68)
ax0.set_ylabel("")
ax0.set_xlabel("")
ax0.set_title("")
ax0.xaxis.set_tick_params(labelsize = 4, pad = -3)
ax0.yaxis.set_tick_params(labelsize = 4, pad = -3)
ax0.grid(True, linestyle='--', color = "black", alpha = 0.1)

#to_plt = pisco_tx.tx.rio.set_crs(shp_peru_no_lake.crs)
plot_b = pisco_tx.plot(ax = ax1, cmap = "Spectral_r",
                       add_colorbar=False,
                       levels= [5, 10, 15, 20, 25, 30])
axin = inset_axes(ax1, width='4%', height='35%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax1.transAxes)
cb = plt.colorbar(plot_b, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('Temp. máxima ($^{\circ}C$)', labelpad=-25, size = 6)
cb.ax.tick_params(labelsize = 6, pad = 0)


# shp_drainages.geometry.boundary.plot(ax = ax1, edgecolor = "black", linewidth = .75)
shp_SA.geometry.boundary.plot(ax = ax1, edgecolor = "black", linewidth = .5)
shp_dep.geometry.boundary.plot(ax = ax1, edgecolor = "black", linewidth = .25)
shp_lks.plot(ax = ax1, edgecolor = "deepskyblue", color = "deepskyblue")

ax1.set_ylim(-18.5, 0.5)
ax1.set_xlim(-81.75, -68)
ax1.set_ylabel("")
ax1.set_xlabel("")
ax1.set_title("")
ax1.xaxis.set_tick_params(labelsize = 4, pad = -3)
ax1.yaxis.set_tick_params(labelsize = 4, pad = -3)

ax1.grid(True, linestyle='--', color = "black", alpha = 0.1)

plot_b = rs_data.plot(ax=ax2, cmap='viridis',
                      add_colorbar=False, levels= [18, 19, 20, 21, 23])
axin = inset_axes(ax2, width='4%', height='35%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax2.transAxes)
cb = plt.colorbar(plot_b, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('Radiación solar ($MJ\,m^{-2}$)', labelpad=-25, size = 5)
cb.ax.tick_params(labelsize = 6, pad = 0)

# shp_drainages.geometry.boundary.plot(ax = ax1, edgecolor = "black", linewidth = .75)
shp_SA.geometry.boundary.plot(ax = ax2, edgecolor = "black", linewidth = .5)
shp_dep.geometry.boundary.plot(ax = ax2, edgecolor = "black", linewidth = .25)
shp_lks.plot(ax = ax2, edgecolor = "deepskyblue", color = "deepskyblue")

ax2.set_ylim(-18.5, 0.5)
ax2.set_xlim(-81.75, -68)
ax2.set_ylabel("")
ax2.set_xlabel("")
ax2.set_title("")
ax2.xaxis.set_tick_params(labelsize = 4, pad = -3)
ax2.yaxis.set_tick_params(labelsize = 4, pad = -3)

ax2.grid(True, linestyle='--', color = "black", alpha = 0.1)

plt.savefig('output/study_area.png',
            bbox_inches='tight',pad_inches = 0.01, dpi = 300)

plt.close()