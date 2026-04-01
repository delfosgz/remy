from fastmcp import FastMCP
 
mcp = FastMCP("Cocina_Tools")
 
@mcp.tool()
def get_ingredientes_temporada(temporada: str) -> str:
    """Retorna los mejores ingredientes frescos disponibles según la temporada del año.
    Úsala cuando el usuario pregunte qué cocinar según la época o quiera ingredientes de temporada."""
    catalogo = {
        "primavera": "espárragos, chícharos, alcachofas, fresas, rábanos, epazote",
        "verano":    "jitomate, chile serrano, calabaza, elote, aguacate, cilantro, durazno",
        "otoño":     "calabaza de castilla, hongos, huitlacoche, granada, higo, camote",
        "invierno":  "coles, betabel, naranja, mandarina, coliflor, nopales",
    }
    key = temporada.lower().strip()
    return catalogo.get(key, "Temporada no reconocida. Usa: primavera, verano, otoño o invierno.")
 
 
@mcp.tool()
def get_tiempo_coccion(ingrediente: str) -> str:
    """Retorna el tiempo estimado de cocción para un ingrediente.
    Úsala cuando el usuario pregunte cuánto tiempo cocinar algo."""
    tiempos = {
        "pollo":     "30-45 min a fuego medio",
        "res":       "1-2 horas según el corte",
        "cerdo":     "45-60 min",
        "pasta":     "8-12 min en agua hirviendo",
        "arroz":     "18-20 min a fuego bajo",
        "papa":      "20-30 min",
        "zanahoria": "10-15 min",
        "frijoles":  "1.5-2 horas (o 30 min en olla express)",
        "nopales":   "10-15 min",
        "elote":     "15-20 min",
    }
    key = ingrediente.lower().strip()
    return tiempos.get(key, f"No tengo el tiempo para '{ingrediente}', consulta una receta específica.")
 
 
if __name__ == "__main__":
    print("🍳 Iniciando MCP Server en http://localhost:8000/sse")
    mcp.run(transport="stdio", host="0.0.0.0", port=8000)