import xarray as xr
import numpy as np
import pandas as pd
from geopandas import read_file as gpd_read_file
import rioxarray


# shps
shp_peru = gpd_read_file("data/shps/Sudamérica.shp").to_crs({"init": "epsg:4326"}).iloc[11:12]
shp_peru_no_lake = gpd_read_file("data/shps/Peru_no_lake.shp").to_crs({"init": "epsg:4326"})
shp_drainages = gpd_read_file("data/shps/vertientes.shp").to_crs({"init": "epsg:4326"})
shp_dep = gpd_read_file("data/shps/DEPARTAMENTOS.shp").to_crs({"init": "epsg:4326"})
shp_SA = gpd_read_file("data/shps/Sudamérica.shp").to_crs({"init": "epsg:4326"})
shp_lks = gpd_read_file("data/shps/lago_titicaca_sideteva_puno.shp").to_crs({"init": "epsg:4326"})

id_dep_order = ["TUMBES", "PIURA", "AMAZONAS", "CAJAMARCA", "HUANUCO", "PASCO", "CUSCO",
                "LAMBAYEQUE", "LA LIBERTAD", "ANCASH", "LIMA", "ICA", "AREQUIPA", "MOQUEGUA",
                "TACNA", "SAN MARTIN", "JUNIN", "AYACUCHO", "HUANCAVELICA","APURIMAC", "PUNO",
                "LORETO", "UCAYALI", "MADRE DE DIOS"]

# grid
ra_present = xr.open_rasterio("data/ARIDEZ_ACTUAL/ARIDEZ_REGIMEN.tif")
ra_present = ra_present.where(ra_present > 0)
ra_present = np.abs(ra_present - 10)
ra_present = ra_present.rio.set_crs("epsg:4326")

ra_future = xr.open_rasterio("data/ARIDEZ_FUTURO/ARIDEZ_REG_PM.tif")
ra_future = ra_future.where(ra_future > 0)
ra_future = np.abs(ra_future - 10)
ra_future = ra_future.rio.set_crs("epsg:4326")

# aridity by departamento and subtype

index = pd.MultiIndex.from_product([['Xerico', 'Hiper Arido', "Arido",
                                     "Semiarido", "Subhumedo", "Humedo",
                                     "Hiper Humedo", "Hidrico", "Hiper Hidrico"], ['km2', '%']])
present_df = []
future_df = []
difference_df = []
for shp in id_dep_order:

    shp = shp_dep[shp_dep.DEPARTAMEN == shp]

    # present
    grid_value = ra_present.rio.clip(shp.geometry, drop=False)
    grid_value = grid_value.values.flatten()
    grid_value = grid_value[~np.isnan(grid_value)]

    data_subtype = [[np.round(grid_value.tolist().count(i)/1000, 1),
                     np.round(100*grid_value.tolist().count(i)/len(grid_value), 1)] for i in np.arange(1, 10)]
    data_subtype = [item for sublist in data_subtype for item in sublist]

    present_df.append(pd.DataFrame([data_subtype], columns=index, index=[shp.DEPARTAMEN.values[0].capitalize()]))

    # future
    grid_value_fut = ra_future.rio.clip(shp.geometry, drop=False)
    grid_value_fut = grid_value_fut.values.flatten()
    grid_value_fut = grid_value_fut[~np.isnan(grid_value_fut)]

    data_subtype_fut = [[np.round(grid_value_fut.tolist().count(i)/1000, 1),
                         np.round(100*grid_value_fut.tolist().count(i)/len(grid_value_fut), 1)] for i in np.arange(1, 10)]
    data_subtype_fut = [item for sublist in data_subtype_fut for item in sublist]

    future_df.append(pd.DataFrame([data_subtype_fut], columns=index, index=[shp.DEPARTAMEN.values[0].capitalize()]))

    # difference
    grid_value_diff = [np.round(i - j, 1) for i, j in zip(data_subtype_fut, data_subtype)]
    difference_df.append(pd.DataFrame([grid_value_diff], columns=index, index=[shp.DEPARTAMEN.values[0].capitalize()]))

pd.concat(present_df, axis=0).to_csv("output/ra_data_present.csv")
pd.concat(future_df, axis=0).to_csv("output/ra_data_future.csv")
pd.concat(difference_df, axis=0).to_csv("output/ra_data_difference.csv")

# aridity (5 subtypes) by departamento

ra_present_len = ra_present.values.flatten()
ra_present_len = ra_present_len[~np.isnan(ra_present_len)]
ra_present_size = len(ra_present_len)
ra_present_ZA_size = np.sum([ra_present_len.tolist().count(i) for i in np.arange(1, 6)])

ra_future_len = ra_future.values.flatten()
ra_future_len = ra_future_len[~np.isnan(ra_future_len)]
ra_future_size = len(ra_future_len)
ra_future_ZA_size = np.sum([ra_future_len.tolist().count(i) for i in np.arange(1, 6)])


zonas_aridas_data = []
for shp in id_dep_order:

    shp = shp_dep[shp_dep.DEPARTAMEN == shp]

    # present
    grid_value = ra_present.rio.clip(shp.geometry, drop=False)
    grid_value = grid_value.values.flatten()
    grid_value = grid_value[~np.isnan(grid_value)]
    grid_value = np.sum([grid_value.tolist().count(i) for i in np.arange(1, 6)])
    grid_value = [100*grid_value/ra_present_size, 100*grid_value/ra_present_ZA_size, grid_value]
    grid_value = [np.round(i, 1) for i in grid_value]

    # future
    grid_value_fut = ra_future.rio.clip(shp.geometry, drop=False)
    grid_value_fut = grid_value_fut.values.flatten()
    grid_value_fut = grid_value_fut[~np.isnan(grid_value_fut)]
    grid_value_fut = np.sum([grid_value_fut.tolist().count(i) for i in np.arange(1, 6)])
    grid_value_fut = [100*grid_value_fut/ra_future_size, 100*grid_value_fut/ra_future_ZA_size, grid_value_fut]
    grid_value_fut = [np.round(i, 1) for i in grid_value_fut]

    zonas_aridas_data.append(
        pd.DataFrame([grid_value + grid_value_fut],
                     columns=["%ZA by dep f(Peru)", "%ZA by dep f(ZA de Peru) ", "Sup",
                              "%ZA by dep f(Peru) future", "%ZA by dep f(ZA de Peru) future", "Sup fut"],
                     index=[shp.DEPARTAMEN.values[0].capitalize()])
    )


zonas_aridas_data = pd.concat(zonas_aridas_data, axis=0)
zonas_aridas_data.to_csv("output/za_present_future.csv")

# aridity (RA) subtype in percent in Peru
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.family"] = "Arial"
sns.set_style("whitegrid", {'xtick.bottom':True,})
sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 1})


ra_present_len = ra_present.values.flatten()
ra_present_len = ra_present_len[~np.isnan(ra_present_len)]
RApre = [np.round(100*ra_present_len.tolist().count(i)/len(ra_present_len),1) for i in np.arange(1, 10)]

ra_future_len = ra_future.values.flatten()
ra_future_len = ra_future_len[~np.isnan(ra_future_len)]
RAfut = [np.round(100*ra_future_len.tolist().count(i)/len(ra_future_len),1) for i in np.arange(1, 10)]

ra_labels = ["Xerico", "Hiper\nÁrido", "Árido", "Semi\nÁrido", "Sub-\nHúmedo", "Húmedo", "Hiper\nHúmedo", "Hídrico", "Hiper\nHídrico"]

x = np.arange(9)  # the label locations
width = 0.45  # the width of the bars

fig, ax = plt.subplots(dpi=200, figsize=(9, 4))
rects1 = ax.bar(x - width/2, RApre, width, label='1981-2010',color="lightgrey")
rects2 = ax.bar(x + width/2, RAfut, width, label='2035-2065',color="slategrey")

ax.set_ylabel('%')
ax.set_xticks(x)
ax.set_xticklabels(ra_labels, size=9,ha="center")
ax.legend()
ax.grid(True, linestyle='--', color = "black", alpha = 0.1)

plt.savefig('output/RA_changes.png',
            bbox_inches='tight',pad_inches = 0.01, dpi = 200)

plt.close()

# ZA by departamento
ZApre = zonas_aridas_data.iloc[:,1].values
ZAfut = zonas_aridas_data.iloc[:,4].values

x = np.arange(len(id_dep_order))  # the label locations
width = 0.45  # the width of the bars

fig, ax = plt.subplots(dpi=140, figsize=(9, 4))
rects1 = ax.bar(x - width/2, ZApre, width, label='1981-2010',color="lightgrey")
rects2 = ax.bar(x + width/2, ZAfut, width, label='2035-2065',color="slategrey")

ax.set_ylabel('%')
ax.set_xticks(x)
labels = ax.set_xticklabels(zonas_aridas_data.index, size=7,ha="center")
for i, label in enumerate(labels):
    label.set_y(label.get_position()[1] - (i % 2) * 0.035)
ax.legend()
ax.grid(True, linestyle='--', color = "black", alpha = 0.1)

plt.savefig('output/ZA_changes.png',
            bbox_inches='tight',pad_inches = 0.01, dpi = 140)

plt.close()

