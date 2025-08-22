#!/bin/bash

# Ejecutar todos los scripts de Python en segundo plano
python3 domo_canne_main.py &
python3 alerta_comida.py &
python3 dar_comida.py &
python3 email_server.py &

# Esperar a que todos terminen (opcional, util si no quieres que se cierre el script bash)
wait
