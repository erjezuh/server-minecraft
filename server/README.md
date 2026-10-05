# Servidor

Aquí vivirá el pack de servidor generado (`mods/` + configuración) **cuando la
selección de mods esté aprobada**.

> **No desplegar nada todavía.** Pendiente de revisión de
> [`docs/PROPUESTA_MODS.md`](../docs/PROPUESTA_MODS.md) y aprobación explícita.

Plan previsto:

- `scripts/construir.py` generará aquí el contenido del servidor (solo mods `servidor`
  y `ambos`, nunca mods exclusivos de cliente).
- Recursos objetivo: **4 GB de RAM**, flags G1GC/Aikar, pre-generación del mundo con Chunky.
- 3 jugadores (tú, Rafa y Dani).

## Requisitos de despliegue (anotados para el futuro)

- **Red**: Simple Voice Chat necesita el **puerto UDP 24454** abierto (TCP aparte
  para el juego, 25565 por defecto).
- **Resource pack**: Universal Graves usa Polymer AutoHost; los 3 jugadores deberán
  aceptar el pack del servidor al entrar (un clic, mecanismo vanilla).
- **Gamerule sugerida**: `playersSleepingPercentage` bajo (p. ej. 34) para no exigir
  que los 3 duerman a la vez.
- **Mundo**: pre-generar con Chunky (radio 3k–4k), `view-distance` 6–8,
  `simulation-distance` 4–6.

Este directorio incluye un `.gitkeep` para que exista en git mientras no hay contenido real.
