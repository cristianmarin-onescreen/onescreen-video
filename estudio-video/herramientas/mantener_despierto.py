"""Evita que Windows se suspenda por inactividad mientras corre (SetThreadExecutionState; no cambia ningun ajuste del sistema).
No evita la suspension manual ni cerrar la tapa. Uso: python mantener_despierto.py HH:MM   (hasta esa hora; por defecto 06:30)"""
import ctypes, datetime as dt, sys, time

ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
hh, mm = (sys.argv[1] if len(sys.argv) > 1 else "06:30").split(":")
meta = dt.datetime.now().replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)
if meta <= dt.datetime.now():
    meta += dt.timedelta(days=1)
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
print("despierto hasta", meta, flush=True)
try:
    while dt.datetime.now() < meta:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)   # se renueva cada minuto
        time.sleep(60)
finally:
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
