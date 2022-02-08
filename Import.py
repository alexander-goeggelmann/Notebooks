import os
import sys
import importlib
import matplotlib
import bokeh
import scipy

import matplotlib.pyplot as plt
import pandas as pd
import holoviews as hv
import numpy as np

from scipy.optimize import curve_fit
from holoviews.operation.datashader import datashade, dynspread

if sys.platform.startswith('linux'):
    ROOT_PATH = "/media/alexander/Code/PhytonScripts"
    SEAGATE_PATH = "/media/alexander/Seagate/ECHoData"
    DATA_L_PATH = "/media/alexander/ECHoData"

else:
    ROOT_PATH = os.path.join("C:\\Users\\alexa\\OneDrive\\Documents\\Uni\\Code\\PhytonScripts")
    SEAGATE_PATH = os.path.join("K:\ECHoData")
    DATA_L_PATH = "I:"

SIM_PATH = os.path.join(DATA_L_PATH, "Simulations")
CRESST_PATH = os.path.join(DATA_L_PATH, "CresstSimulations")
SCREENING_PATH = os.path.join(DATA_L_PATH, "ScreeningSimulations")
RUN_24_ASY_PATH = os.path.join(SEAGATE_PATH, "Run24-Asymmetric")
RUN_24_COIN_PATH = os.path.join(SEAGATE_PATH, "Run24-Coincidences")
OLD_RUN_PATH = os.path.join(SEAGATE_PATH, "NoncompressedData")

sys.path.append(os.path.join(ROOT_PATH, "Read_Simulation"))
sys.path.append(os.path.join(ROOT_PATH, "Plotting"))
sys.path.append(os.path.join(ROOT_PATH, "Theory"))
sys.path.append(os.path.join(ROOT_PATH, "Read_Data"))
sys.path.append(os.path.join(ROOT_PATH, "PulseSimulation"))
sys.path.append(os.path.join(ROOT_PATH, "Screening"))

import LoadData
import Columns
import Interpreter
import ReadSimulation as rs
import LoadVeto as lv

import PlottingTool as ptool
import Formatter as fmat

import calibration_generator as cg
import ellipse_generator as elg
import event_generator as eg
import global_parameters as gl
import pixel_day_generator as pdg
import pulse_generator as pg

from TexToUni import tex_to_uni

import LandauDistribution as ld

import noise_generator as ng

import Screening

importlib.reload(LoadData)
importlib.reload(Columns)
importlib.reload(Interpreter)
importlib.reload(ng)
importlib.reload(Screening)
importlib.reload(rs)
importlib.reload(lv)

importlib.reload(ptool)
importlib.reload(fmat)

importlib.reload(cg)
importlib.reload(elg)
importlib.reload(eg)
importlib.reload(gl)
importlib.reload(pdg)
importlib.reload(pg)

importlib.reload(ld)

def set_matplotlib_rc(mpl_rcParams):
	mpl_rcParams['font.size'] = 25 # 25
	mpl_rcParams['figure.figsize'] = [9.0 * 1.57, 6.36 * 1.57]
	mpl_rcParams['text.usetex'] = False
	mpl_rcParams['axes.grid'] = True
	mpl_rcParams['grid.alpha'] = 1.0
	mpl_rcParams['font.weight'] = 'normal'
	mpl_rcParams['figure.facecolor'] = (1, 1, 1, 1)
	mpl_rcParams['lines.linewidth'] = 3.
	mpl_rcParams['axes.labelpad'] = 15.

HV_FONTSIZE = {'legend': 18, 'labels': 20., 'ticks': 18.}
HV_HEIGHT = 636
HV_WIDTH = 900
HV_GRID = {'grid_line_color': 'black', 'grid_line_width': 1.5,
           'minor_xgrid_line_color': 'lightgray',
           'minor_ygrid_line_color': 'lightgray',
           'grid_line_alpha': 0.3, 'minor_ygrid_line_alpha': 0.5}
HV_YFORMATT = fmat.log_formatter
HV_XFORMATT = fmat.formatter

def set_datashade(xdata, ydata, label=None):
    my_palette = [(0, 0, 0)]
    for i in bokeh.palettes.Spectral11:
        my_palette.append(matplotlib.colors.hex2color(i))
    my_palette = my_palette[1:]
    my_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
            "", my_palette)
    return dynspread(datashade(
            hv.Points((xdata, ydata), label=label), cmap=my_cmap))

def plot_hv(hv_obj, xlabel=None, ylabel=None):
    out = hv_obj.opts(
            xformatter=HV_XFORMATT, yformatter=HV_YFORMATT,
            width=HV_WIDTH, height=HV_HEIGHT, fontsize=HV_FONTSIZE)

    if xlabel is not None:
        out = out.redim.label(x=xlabel)
    if ylabel is not None:
        out = out.redim.label(y=ylabel)
    return out
