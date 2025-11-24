"""
Python model 'document.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import integer
from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.10.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 1,
    "final_time": lambda: 20,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Año", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Año", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Año",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Año",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="motos",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_motos": 1},
    other_deps={"_integ_motos": {"initial": {}, "step": {"ingm": 1, "egrm": 1}}},
)
def motos():
    return _integ_motos()


_integ_motos = Integ(lambda: ingm() - egrm(), lambda: 100, "_integ_motos")


@component.add(
    name="Discrep",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"obj": 1, "motos": 1},
)
def discrep():
    return obj() - motos()


@component.add(
    name="ingM",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discrep": 1, "tim": 1},
)
def ingm():
    return discrep() * tim()


@component.add(
    name="EgrM",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tem": 1, "motos": 1},
)
def egrm():
    return tem() * motos()


@component.add(
    name="Tasa total salidas",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tasaegtax": 1, "tsalia": 1, "tem": 1},
)
def tasa_total_salidas():
    return tasaegtax() + tsalia() + tem()


@component.add(name="TeM", comp_type="Constant", comp_subtype="Normal")
def tem():
    return 0.2


@component.add(name="TiM", comp_type="Constant", comp_subtype="Normal")
def tim():
    return 0.4


@component.add(name="Obj", comp_type="Constant", comp_subtype="Normal")
def obj():
    return 200


@component.add(
    name="total",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tasaingom": 1, "tasaingtax": 1, "tim": 1},
)
def total():
    return tasaingom() + tasaingtax() + tim()


@component.add(
    name="transporte",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_transporte": 1},
    other_deps={
        "_integ_transporte": {"initial": {}, "step": {"entradas": 1, "salidas": 1}}
    },
)
def transporte():
    return _integ_transporte()


_integ_transporte = Integ(
    lambda: entradas() - salidas(), lambda: 1000, "_integ_transporte"
)


@component.add(
    name="Salidas",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"transporte": 1, "tasa_total_salidas": 1},
)
def salidas():
    return transporte() * tasa_total_salidas()


@component.add(
    name="entradas",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total": 1, "transporte": 1},
)
def entradas():
    return total() * transporte()


@component.add(
    name="salidaomnibus",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tsalia": 1, "omnibus": 1},
)
def salidaomnibus():
    """
    5
    """
    return tsalia() * omnibus()


@component.add(
    name="EgrsoTaxis",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tasaegtax": 1, "taxis": 1},
)
def egrsotaxis():
    return tasaegtax() * taxis()


@component.add(name="tasaIngTax", comp_type="Constant", comp_subtype="Normal")
def tasaingtax():
    return 0.2


@component.add(
    name="IngTaxis",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tasaingtax": 1, "taxis": 1},
)
def ingtaxis():
    return tasaingtax() * taxis()


@component.add(
    name="ingromnibus",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"omnibus": 1, "tasaingom": 1},
)
def ingromnibus():
    return omnibus() * tasaingom()


@component.add(name="tsalia", comp_type="Constant", comp_subtype="Normal")
def tsalia():
    return 0.1


@component.add(name="tasaegTax", comp_type="Constant", comp_subtype="Normal")
def tasaegtax():
    return 0.1


@component.add(name="tasaIngOm", comp_type="Constant", comp_subtype="Normal")
def tasaingom():
    return 0.2


@component.add(
    name="taxis",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_taxis": 1},
    other_deps={
        "_integ_taxis": {"initial": {}, "step": {"ingtaxis": 1, "egrsotaxis": 1}}
    },
)
def taxis():
    return _integ_taxis()


_integ_taxis = Integ(lambda: ingtaxis() - egrsotaxis(), lambda: 100, "_integ_taxis")


@component.add(
    name="omnibus",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_omnibus": 1},
    other_deps={
        "_integ_omnibus": {
            "initial": {},
            "step": {"ingromnibus": 1, "salidaomnibus": 1},
        }
    },
)
def omnibus():
    return _integ_omnibus()


_integ_omnibus = Integ(
    lambda: integer(ingromnibus() - salidaomnibus()), lambda: 500, "_integ_omnibus"
)
