import xarray as xr
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.family"] = "Arial"
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.25, rc={"lines.linewidth": 2})

# data
ia = xr.open_rasterio("data/ARIDEZ_ACTUAL/ARIDEZ_INDICE.tif")
ia = ia.reindex(y=np.arange(-0.039, -18.347, -0.01),
                x=np.arange(-81.327, -68.653, 0.01), method="nearest")
ia = ia.where(ia > 0)

ra = xr.open_rasterio("data/ARIDEZ_ACTUAL/ARIDEZ_REGIMEN.tif")
ra = ra.reindex(y=np.arange(-0.039, -18.347, -0.01),
                x=np.arange(-81.327, -68.653, 0.01), method="nearest")
ra = ra.where(ra > 0)

ia_m = np.ravel(ia.values)
ra_m = np.ravel(ra.values)

ra_labels = ["Xerico", "Hiper\nÁrido", "Árido", "Semi\nÁrido", "Sub-\nHúmedo", "Húmedo", "Hiper\nHúmedo", "Hídrico", "Hiper\nHídrico"]
ia_labels = ["Hiper-\narido", "Árido", "Semi-\nárido", "Subhúmedo\nseco", "Subhúmedo\nhúmedo", "Húmedo"]

# figure
fig, ax = plt.subplots(figsize = (8, 5), dpi = 300)
ax.scatter(x = ra_m, y = ia_m)
ax.set_xlim(9.25, 0.75)
ax.set_xticks(range(1, 10))
ax.set_yticks(range(1, 7))
ax.set_xticklabels(list(reversed(ra_labels)), family='Arial',size = 9)
ax.set_yticklabels(ia_labels, family='Arial',size = 9)
ax.set_ylabel("Índice de Aridez",family='Arial', size = 10)
ax.set_xlabel("Régimen de Aridez", family='Arial', size = 10)
ax.grid(True, linestyle='--', color = "black", alpha = 0.1)

plt.savefig('output/aridity_indice_comparison.png',
            bbox_inches='tight',dpi = 300)
plt.close()