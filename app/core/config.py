import os
from dotenv import load_dotenv

load_dotenv()

# Tarifa cobrada por cada hora o fracción de hora transcurrida
TARIFA_POR_FRACCION = float(os.getenv("TARIFA_POR_FRACCION", "0.50"))
