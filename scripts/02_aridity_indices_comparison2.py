import numpy as np
from geopandas import read_file as gpd_read_file
import xarray as xr

import matplotlib.pyplot as plt
import matplotlib.colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import seaborn as sns

exec(open("src/utils.py").read())

plt.rcParams["font.family"] = "Arial"
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.25, rc={"lines.linewidth": 1})

# shps
shp_peru = gpd_read_file("data/shps/Sudamérica.shp").to_crs({"init": "epsg:4326"}).iloc[11:12]
shp_peru_no_lake = gpd_read_file("data/shps/Peru_no_lake.shp").to_crs({"init": "epsg:4326"})
shp_drainages = gpd_read_file("data/shps/vertientes.shp").to_crs({"init": "epsg:4326"})
shp_dep = gpd_read_file("data/shps/DEPARTAMENTOS.shp").to_crs({"init": "epsg:4326"})
shp_SA = gpd_read_file(".data/shps/Sudamérica.shp").to_crs({"init": "epsg:4326"})
shp_lks = gpd_read_file("data/shps/lago_titicaca_sideteva_puno.shp").to_crs({"init": "epsg:4326"})


# gridded
ia = xr.open_rasterio("./data/observed/aridez/ARIDEZ_INDICE.tif")
ia = ia.reindex(y=np.arange(-0.039, -18.347, -0.01),
                x=np.arange(-81.327, -68.653, 0.01), method="nearest")
ia = ia.where(ia > 0)

ra = xr.open_rasterio("./data/observed/aridez/ARIDEZ_REGIMEN.tif")
ra = ra.reindex(y=np.arange(-0.039, -18.347, -0.01),
                x=np.arange(-81.327, -68.653, 0.01), method="nearest")
ra = ra.where(ra > 0)
ra = np.abs(ra - 10) # 9(arid) -> 1(wet) ->> 1(arid) -> 9 (wet)

IA_2 = xr.apply_ufunc(IA_two, ia, vectorize=True)/10
RA_2 = xr.apply_ufunc(RA_two, ra, vectorize=True)/10
RAIA_2 = xr.apply_ufunc(RAIA, RA_2, IA_2, vectorize=True)/10


# figure
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["lightyellow","lightgreen","indianred", "royalblue"])


fig, ax0 = plt.subplots(figsize = (5, 5),
                          dpi = 300)

plot_b = RAIA_2.plot(ax = ax0, cmap=cmap,
                      add_colorbar=False, levels = np.arange(1, 6))
axin = inset_axes(ax0, width='5%', height='35%', loc = 'lower left', bbox_to_anchor = (0.01, 0.01, 1 ,1), bbox_transform = ax0.transAxes)
cb = plt.colorbar(plot_b, cax=axin, orientation = "vertical",aspect = 5, ticks = np.arange(1.5, 5, 1))
cb.ax.set_yticklabels(['Árido ($RA$) -\n Árido ($I_{a}$)',
                  'Húmedo ($RA$) -\n Húmedo ($I_{a}$)',
                  'Árido ($RA$) -\n Húmedo ($I_{a}$)',
                  'Húmedo ($RA$) -\n Árido ($I_{a}$)'], size = 5.5)
cb.ax.tick_params(axis='y', direction='out', length = 2)
#cb.ax.set_ylabel('Niveles', labelpad=-40, size = 6)

#cb.ax.tick_params(labelsize = 6)

#shp_drainages.geometry.boundary.plot(ax = ax0, edgecolor = "black", linewidth = .75)
shp_SA.geometry.boundary.plot(ax = ax0, edgecolor = "black", linewidth = .5)
shp_dep.geometry.boundary.plot(ax = ax0, edgecolor = "black", linewidth = .25)
shp_lks.plot(ax = ax0, edgecolor = "deepskyblue", color = "deepskyblue")

ax0.set_ylim(-18.5, 0.5)
ax0.set_xlim(-81.75, -68)
ax0.set_ylabel("")
ax0.set_xlabel("")
ax0.set_title("")
ax0.xaxis.set_tick_params(labelsize = 3.5, pad = -3)
ax0.yaxis.set_tick_params(labelsize = 3.5, pad = -3)
ax0.grid(True, linestyle='--', color = "black", alpha = 0.1)

plt.savefig('output/aridity_indice_comparison2.png',
            bbox_inches='tight',pad_inches = 0.01, dpi = 200)

plt.close()
