"""
Python model 'document.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import integer
from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 12,
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
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
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
    units="Month",
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
    name="Diferencia cisternas",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cantidad_cisternas_deseados": 1, "cisternas": 1},
)
def diferencia_cisternas():
    return cantidad_cisternas_deseados() - cisternas()


@component.add(name="tasa Venta", comp_type="Constant", comp_subtype="Normal")
def tasa_venta():
    return 0.01


@component.add(
    name="Cisternas",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cisternas": 1},
    other_deps={
        "_integ_cisternas": {
            "initial": {},
            "step": {"compras": 1, "obsolencia": 1, "ventas": 1},
        }
    },
)
def cisternas():
    return _integ_cisternas()


_integ_cisternas = Integ(
    lambda: compras() - obsolencia() - ventas(), lambda: 10, "_integ_cisternas"
)


@component.add(
    name="Cisterna'",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cisternas": 1},
)
def cisterna():
    return integer(cisternas())


@component.add(name="Tasa obsolencia", comp_type="Constant", comp_subtype="Normal")
def tasa_obsolencia():
    return 0.002


@component.add(
    name="Obsolencia",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tasa_obsolencia": 1, "cisternas": 1},
)
def obsolencia():
    return tasa_obsolencia() * cisternas()


@component.add(
    name="Compras",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tasa_compra": 1, "diferencia_cisternas": 1},
)
def compras():
    return tasa_compra() * diferencia_cisternas()


@component.add(
    name="Ventas",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tasa_venta": 1, "cisternas": 1},
)
def ventas():
    return tasa_venta() * cisternas()


@component.add(name="Tasa Compra", comp_type="Constant", comp_subtype="Normal")
def tasa_compra():
    return 0.3


@component.add(
    name="Aumento en desarrollo tecnologico y operativo",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"diferencia_operaciones": 1, "tasa_aumento": 1},
)
def aumento_en_desarrollo_tecnologico_y_operativo():
    return diferencia_operaciones() * tasa_aumento()


@component.add(
    name="Cantidad cisternas deseados",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tasa_cisternas": 1, "demanda_a_la_empresa": 1},
)
def cantidad_cisternas_deseados():
    return tasa_cisternas() * demanda_a_la_empresa()


@component.add(
    name="Captacion por cliente actual", comp_type="Constant", comp_subtype="Normal"
)
def captacion_por_cliente_actual():
    return 0.045


@component.add(
    name="Demanda a la empresa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"clientes": 1, "demanda_por_cliente": 1},
)
def demanda_a_la_empresa():
    return clientes() * demanda_por_cliente()


@component.add(
    name="Clientes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_clientes": 1},
    other_deps={
        "_integ_clientes": {
            "initial": {},
            "step": {"clientes_actuales": 1, "clientes_salientes": 1},
        }
    },
)
def clientes():
    return _integ_clientes()


_integ_clientes = Integ(
    lambda: clientes_actuales() - clientes_salientes(), lambda: 100, "_integ_clientes"
)


@component.add(
    name="Clientes actuales",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "clientes_captados_por_difusion": 1,
        "clientes_captados_por_publicidad_boca_a_boca": 1,
    },
)
def clientes_actuales():
    return integer(
        clientes_captados_por_difusion()
        + clientes_captados_por_publicidad_boca_a_boca()
    )


@component.add(
    name="Clientes captados por difusion",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "clientes_potenciales": 1,
        "efectividad_por_difusion": 1,
        "gastos_por_difusion": 1,
    },
)
def clientes_captados_por_difusion():
    return (
        clientes_potenciales()
        * efectividad_por_difusion()
        * gastos_por_difusion()
        / 100
    )


@component.add(
    name="Clientes captados por publicidad boca a boca",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"captacion_por_cliente_actual": 1, "clientes": 1},
)
def clientes_captados_por_publicidad_boca_a_boca():
    return captacion_por_cliente_actual() * clientes()


@component.add(
    name="Clientes potenciales",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_clientes_potenciales": 1},
    other_deps={
        "_integ_clientes_potenciales": {
            "initial": {},
            "step": {"clientes_salientes": 1, "clientes_actuales": 1},
        }
    },
)
def clientes_potenciales():
    return _integ_clientes_potenciales()


_integ_clientes_potenciales = Integ(
    lambda: clientes_salientes() - clientes_actuales(),
    lambda: 100,
    "_integ_clientes_potenciales",
)


@component.add(
    name="Clientes salientes",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"clientes": 1, "tiempo_de_permanencia_promedio": 1},
)
def clientes_salientes():
    return integer(clientes() * tiempo_de_permanencia_promedio())


@component.add(
    name="Tiempo de permanencia promedio", comp_type="Constant", comp_subtype="Normal"
)
def tiempo_de_permanencia_promedio():
    return 0.069999


@component.add(
    name="Diferencia operaciones",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"control_de_operaciones_deseado": 1, "control_de_operaciones": 1},
)
def diferencia_operaciones():
    return control_de_operaciones_deseado() - control_de_operaciones()


@component.add(
    name="Efectividad por difusion", comp_type="Constant", comp_subtype="Normal"
)
def efectividad_por_difusion():
    return 0.003


@component.add(
    name="Control de operaciones",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"inversion_en_desarrollo_tecnologico_y_operativo": 1},
)
def control_de_operaciones():
    return 1 + inversion_en_desarrollo_tecnologico_y_operativo() / 1000


@component.add(
    name="Control de operaciones deseado", comp_type="Constant", comp_subtype="Normal"
)
def control_de_operaciones_deseado():
    return 200


@component.add(
    name="Ingreso por venta",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ventas": 1},
)
def ingreso_por_venta():
    return 1000 * ventas()


@component.add(name="Demanda por cliente", comp_type="Constant", comp_subtype="Normal")
def demanda_por_cliente():
    return 3


@component.add(name="Tasa aumento", comp_type="Constant", comp_subtype="Normal")
def tasa_aumento():
    return 0.12


@component.add(name="Tasa cisternas", comp_type="Constant", comp_subtype="Normal")
def tasa_cisternas():
    return 0.05


@component.add(
    name="Inversion en desarrollo tecnologico y operativo",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_inversion_en_desarrollo_tecnologico_y_operativo": 1},
    other_deps={
        "_integ_inversion_en_desarrollo_tecnologico_y_operativo": {
            "initial": {},
            "step": {"aumento_en_desarrollo_tecnologico_y_operativo": 1},
        }
    },
)
def inversion_en_desarrollo_tecnologico_y_operativo():
    return _integ_inversion_en_desarrollo_tecnologico_y_operativo()


_integ_inversion_en_desarrollo_tecnologico_y_operativo = Integ(
    lambda: aumento_en_desarrollo_tecnologico_y_operativo(),
    lambda: 1200,
    "_integ_inversion_en_desarrollo_tecnologico_y_operativo",
)


@component.add(name="Gastos por difusion", comp_type="Constant", comp_subtype="Normal")
def gastos_por_difusion():
    return 1000


@component.add(
    name="Presupuesto disponible",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ingreso_por_venta": 1,
        "inversion_total_en_desarrollo_tecnologico_y_operativo": 1,
    },
)
def presupuesto_disponible():
    return ingreso_por_venta() + inversion_total_en_desarrollo_tecnologico_y_operativo()


@component.add(
    name="Inversion total en desarrollo tecnologico y operativo",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aumento_en_desarrollo_tecnologico_y_operativo": 1},
)
def inversion_total_en_desarrollo_tecnologico_y_operativo():
    return aumento_en_desarrollo_tecnologico_y_operativo()
