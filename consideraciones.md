Resumen de lo que pasó:

El MCP server carga registry.json del disco una sola vez por proceso (el método _load() usa un caché self._data). Cuando edité registry.json directamente con replace_string_in_file, el servidor no vio esos cambios. La siguiente llamada a run_sap_script guardó el estado en memoria del servidor al disco, sobreescribiendo mis cambios manuales.

Esto mismo pasó en las sesiones anteriores (Steps 2-4): las ediciones manuales al JSON se perdieron cuando run_sap_script guardó su versión en memoria. Solo sobrevivían los datos de los últimos register_verified_function llamados después del último run_sap_script.

Para no repetir el problema en Steps futuros: siempre usar register_verified_function para registrar entradas con metadata (nunca editar registry.json directamente), y hacerlo después de todos los run_sap_script del step.