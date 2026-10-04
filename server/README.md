# Servidor

Aquí vivirá el pack de servidor generado (`mods/` + configuración) **cuando la
selección de mods esté aprobada**.

> **No desplegar nada todavía.** Pendiente de revisión de
> [`docs/PROPUESTA_MODS.md`](../docs/PROPUESTA_MODS.md) y aprobación explícita.

Plan previsto:

- `scripts/construir.py` generará aquí el contenido del servidor (solo mods `servidor`
  y `ambos`, nunca mods exclusivos de cliente).
- Recursos objetivo: **4 GB de RAM**, flags G1GC/Aikar, pre-generación del mundo con Chunky.
- Simple Voice Chat necesitará un **puerto UDP** abierto (típicamente 24454).

Este directorio incluye un `.gitkeep` para que exista en git mientras no hay contenido real.
