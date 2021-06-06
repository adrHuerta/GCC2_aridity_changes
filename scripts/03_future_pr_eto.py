import xarray as xr
import numpy as np
from geopandas import read_file as gpd_read_file

import matplotlib.pyplot as plt
import matplotlib.colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import seaborn as sns

plt.rcParams["font.family"] = "Arial"
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.25, rc={"lines.linewidth": 2})

cmap_c = matplotlib.colors.LinearSegmentedColormap.from_list("", ["royalblue","white","tomato"])
cmap_c_rev = matplotlib.colors.LinearSegmentedColormap.from_list("", ["tomato","white","royalblue"])

# shps
shp_peru = gpd_read_file("data/shps/Sudamérica.shp").to_crs({"init": "epsg:4326"}).iloc[11:12]
shp_peru_no_lake = gpd_read_file("data/shps/Peru_no_lake.shp").to_crs({"init": "epsg:4326"})
shp_drainages = gpd_read_file("data/shps/vertientes.shp").to_crs({"init": "epsg:4326"})
shp_dep = gpd_read_file("data/shps/DEPARTAMENTOS.shp").to_crs({"init": "epsg:4326"})
shp_SA = gpd_read_file("data/shps/Sudamérica.shp").to_crs({"init": "epsg:4326"})
shp_lks = gpd_read_file("data/shps/lago_titicaca_sideteva_puno.shp").to_crs({"init": "epsg:4326"})

# gridded present
path_files = "data/CLIMA_ACTUAL/"
Eo = [path_files + "ETP/ETP_" + str(i+1).zfill(2) + ".tif" for i in range(12)]
Eo = xr.concat([xr.open_rasterio(i) for i in Eo], dim="time").sum(dim="time")

Pr = [path_files + "PPT/PPT_" + str(i+1).zfill(2) + ".tif" for i in range(12)]
Pr = xr.concat([xr.open_rasterio(i) for i in Pr], dim="time").sum(dim="time")

# gridded future
path_files = "data/CLIMA_FUTURO/"
Eo_hadgem = [path_files + "ETP/ETP_" + "HADGEM" + "_" + str(i+1).zfill(2) + ".tif" for i in range(12)]
Eo_acces = [path_files + "ETP/ETP_" + "ACCES" + "_" + str(i+1).zfill(2) + ".tif" for i in range(12)]
Eo_mpiesm = [path_files + "ETP/ETP_" + "MPIESM" + "_" + str(i+1).zfill(2) + ".tif" for i in range(12)]

Pr_hadgem = [path_files + "PPT/PPT_" + "HADGEM" + "_" + str(i+1).zfill(2) + ".tif" for i in range(12)]
Pr_acces = [path_files + "PPT/PPT_" + "ACCES" + "_" + str(i+1).zfill(2) + ".tif" for i in range(12)]
Pr_mpiesm = [path_files + "PPT/PPT_" + "MPIESM" + "_" + str(i+1).zfill(2) + ".tif" for i in range(12)]

## to annual values
Eo_hadgem = xr.concat([xr.open_rasterio(i) for i in Eo_hadgem], dim="time").sum(dim="time")
Eo_acces = xr.concat([xr.open_rasterio(i) for i in Eo_acces], dim="time").sum(dim="time")
Eo_mpiesm = xr.concat([xr.open_rasterio(i) for i in Eo_mpiesm], dim="time").sum(dim="time")

Pr_hadgem = xr.concat([xr.open_rasterio(i) for i in Pr_hadgem], dim="time").sum(dim="time")
Pr_acces = xr.concat([xr.open_rasterio(i) for i in Pr_acces], dim="time").sum(dim="time")
Pr_mpiesm = xr.concat([xr.open_rasterio(i) for i in Pr_mpiesm], dim="time").sum(dim="time")

## matching coordinates
Pr_hadgem = Pr_hadgem.assign_coords(y=Pr.y.values)
Pr_acces = Pr_acces.assign_coords(y=Pr.y.values)
Pr_mpiesm = Pr_mpiesm.assign_coords(y=Pr.y.values)

## percent change by model
Pr_change = xr.concat([(100*(Pr_hadgem - Pr)/Pr), (100*(Pr_acces - Pr)/Pr), (100*(Pr_mpiesm - Pr)/Pr)], dim="models")
Eo_change = xr.concat([(100*(Eo_hadgem - Eo)/Eo), (100*(Eo_acces - Eo)/Eo), (100*(Eo_mpiesm - Eo)/Eo)], dim="models")


# figure
fig, (ax, ax1) = plt.subplots(ncols=2, sharey=True, sharex=True, gridspec_kw = {'wspace':0, 'hspace':0}, figsize=(10, 8))

plot_Eo = Eo_change.mean(dim="models").plot(ax = ax, levels = np.arange(-10, 15, 5), cmap=cmap_c,add_colorbar=False, center = 0)
axin = inset_axes(ax, width='4%', height='35%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax.transAxes)
cb = plt.colorbar(plot_Eo, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('Cambio de ET$_{o}$ (%)', labelpad=-37, size = 8)
cb.ax.tick_params(labelsize = 8, pad = 1)

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

plot_Eo_sd = Eo_change.std(dim="models").plot(ax = ax1, add_colorbar=False, cmap='Greys', levels = np.arange(0, 11, 1))
axin = inset_axes(ax1, width='4%', height='35%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax1.transAxes)
cb = plt.colorbar(plot_Eo_sd, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('SD de Cambio de ET$_{o}$ (%)', labelpad=-30, size = 6)
cb.ax.tick_params(labelsize = 8, pad = 1)

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

plt.savefig('output/delta_change_eo.png',
            bbox_inches='tight',pad_inches = 0.01, dpi = 200)

plt.close()


fig, (ax2, ax3) = plt.subplots(ncols=2, sharey=True, sharex=True, gridspec_kw = {'wspace':0, 'hspace':0}, figsize=(10, 8))

plot_Pr = Pr_change.mean(dim="models").plot(ax = ax2, levels = np.arange(-30, 35, 5), cmap=cmap_c_rev,add_colorbar=False, center = 0)
axin = inset_axes(ax2, width='4%', height='35%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax2.transAxes)
cb = plt.colorbar(plot_Pr, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('Cambio de P (%)', labelpad=-37, size = 8)
cb.ax.tick_params(labelsize = 8, pad = 1)

shp_SA.geometry.boundary.plot(ax = ax2, edgecolor = "black", linewidth = .5)
shp_dep.geometry.boundary.plot(ax = ax2, edgecolor = "black", linewidth = .25)
shp_lks.plot(ax = ax2, edgecolor = "deepskyblue", color = "deepskyblue")

ax2.set_ylim(-18.5, 0.5)
ax2.set_xlim(-81.75, -68)
ax2.set_ylabel("")
ax2.set_xlabel("")
ax2.set_title("")
ax2.xaxis.set_tick_params(labelsize = 5, pad=-3)
ax2.yaxis.set_tick_params(labelsize = 5, pad=-3)

ax2.grid(True, linestyle='--', color = "black", alpha = 0.1)


plot_Pr_sd = Pr_change.std(dim="models").plot(ax = ax3, add_colorbar=False, cmap='Greys', levels = np.arange(0, 11, 1))
axin = inset_axes(ax3, width='4%', height='35%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax3.transAxes)
cb = plt.colorbar(plot_Pr_sd, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('SD de Cambio de P (%)', labelpad=-30, size = 6)
cb.ax.tick_params(labelsize = 8, pad = 1)

shp_SA.geometry.boundary.plot(ax = ax3, edgecolor = "black", linewidth = .5)
shp_dep.geometry.boundary.plot(ax = ax3, edgecolor = "black", linewidth = .25)
shp_lks.plot(ax = ax3, edgecolor = "deepskyblue", color = "deepskyblue")

ax3.set_ylim(-18.5, 0.5)
ax3.set_xlim(-81.75, -68)
ax3.set_ylabel("")
ax3.set_xlabel("")
ax3.set_title("")
ax3.xaxis.set_tick_params(labelsize = 5, pad=-3)
ax3.yaxis.set_tick_params(labelsize = 5, pad=-3)

ax3.grid(True, linestyle='--', color = "black", alpha = 0.1)

plt.savefig('output/delta_change_pr.png',
            bbox_inches='tight',pad_inches = 0.01, dpi = 200)

plt.close()
