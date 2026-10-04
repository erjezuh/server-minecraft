# Servidor Minecraft — Modpack Fabric 1.21.1

Proyecto automatizado para crear y mantener un modpack de **Minecraft 1.21.1 + Fabric**,
pensado para supervivencia multijugador con amigos (estilo series tipo Karmaland):
exploración, aventura, construcción, magia, tecnología, estructuras, mobs y progresión.

> **Estado actual: FASE DE PROPUESTA.**
> Hay una selección de mods propuesta en `modpack/modpack.yml` y documentada en
> [`docs/PROPUESTA_MODS.md`](docs/PROPUESTA_MODS.md), pero **todavía no se ha aprobado**,
> **no se ha descargado ningún `.jar`** y **no se ha desplegado nada**.

## Restricciones del proyecto

- Servidor: **4 GB de RAM**.
- Clientes: **3 GB de RAM** asignados.
- Modpack **ligero y estable**: nada de mods pesados, nada duplicado, nada de relleno.
- Todo compatible con **Minecraft 1.21.1 + Fabric**, con dependencias verificadas.
- Separación estricta: mods de **cliente**, de **servidor** y de **ambos**.

## Estructura

```text
.
├── modpack/
│   └── modpack.yml          # Manifiesto: ÚNICA fuente de verdad (mods, lado, estado)
├── scripts/
│   ├── resolver.py          # Verifica mods contra la API de Modrinth (sin descargar)
│   ├── construir.py         # Descarga .jar y genera packs de cliente y servidor (requiere aprobación)
│   └── requirements.txt     # Dependencias de los scripts (pyyaml)
├── docs/
│   └── PROPUESTA_MODS.md    # Propuesta: lista, para qué sirve cada mod, lado, impacto, descartes
├── client/
│   └── README.md            # Cómo instalarán el pack los jugadores (tras la aprobación)
├── server/
│   └── README.md            # Contendrá el pack de servidor generado (despliegue pendiente)
├── build/                   # Artefactos generados (ignorado por git)
└── .github/workflows/
    └── build.yml            # CI: valida el manifiesto y verifica los mods en cada cambio
```

## Flujo de trabajo

1. **Propuesta** (estamos aquí): se edita `modpack/modpack.yml` con `estado: propuesto`.
   La CI verifica sintaxis y existencia de los mods en Modrinth. No se descarga nada.
2. **Aprobación**: el dueño revisa `docs/PROPUESTA_MODS.md` y cambia el estado a `aprobado`.
3. **Resolución**: `resolver.py` fija versiones exactas de Modrinth para 1.21.1/Fabric
   y genera `build/resolucion.json`.
4. **Construcción**: `construir.py` descarga los `.jar`, separa cliente/servidor y genera:
   - `Karmaland-1.0.0.mrpack` (para Modrinth App / Prism Launcher / MultiMC), y
   - `servidor.zip` con `mods/` + archivos de configuración.
5. **Despliegue** (pendiente, solo cuando se pida explícitamente).

```bash
# 1. Validar el manifiesto (sin red, siempre funciona)
python3 scripts/resolver.py --solo-esquema

# 2. Verificar mods contra Modrinth (requiere internet; NO descarga .jar)
python3 scripts/resolver.py --informe build/informe-verificacion.md

# 3. Fijar versiones exactas (requiere estado "aprobado")
python3 scripts/resolver.py --guardar build/resolucion.json

# 4. Construir packs de cliente y servidor (requiere "aprobado" + resolucion.json)
python3 scripts/construir.py --resolucion build/resolucion.json --salida build/
```

## Reglas

- Los `.jar` **nunca** se suben al repo: siempre se descargan de Modrinth de forma reproducible.
- Cada mod del manifiesto declara su **lado** (`cliente` / `servidor` / `ambos`).
- Nada se despliega en ningún servidor sin aprobación explícita.
