# Propuesta de mods — Karmaland (Fabric 1.21.1)

> **Estado: propuesta pendiente de revisión. No se ha descargado ningún `.jar`
> ni se ha desplegado nada.** La fuente de verdad es `modpack/modpack.yml`
> (`estado_global: propuesto`); este documento es su explicación legible.

Objetivo: supervivencia multijugador con amigos, estilo Karmaland — mundo vivo,
exploración, aventura, construcción, decoración, magia, tecnología, estructuras,
mobs, progresión y momentos divertidos — con **4 GB en servidor**, **3 GB en cliente**,
estable y ligero.

## Cómo leer las tablas

- **Lado**: `ambos` (cliente y servidor), `cliente`, `servidor`.
- **Impacto** (aprox., con pocos jugadores):
  - 🛡️ *mejora* — reduce RAM o sube rendimiento.
  - 🟢 *despreciable* — < ~30 MB.
  - 🟡 *bajo* — ~30–100 MB.
  - 🟠 *moderado* — ~100–250 MB (ningún mod llega a *alto*).
- **Verif.**: `confirmada` (comprobado en Modrinth para esta propuesta),
  `estandar` (mod ubicuo en packs 1.21.1/Fabric; lo re-verifica `resolver.py`),
  `pendiente` (`resolver.py` debe confirmar slug/build antes de incluir).

## 0. Punto de partida: estructura encontrada

El repo contenía solo el esqueleto: `modpack/modpack.yml` con `mods: []`,
`server/.gitkeep`, un workflow que copiaba `server/` a un artefacto y una copia
anidada duplicada `server/modpack/` (eliminada por confusa). Sobre eso se ha montado:

- Manifiesto único (`modpack/modpack.yml`) con 74 mods core + 18 opcionales.
- `scripts/resolver.py`: verifica compatibilidad 1.21.1/Fabric, lado y dependencias
  contra Modrinth **sin descargar nada**.
- `scripts/construir.py`: descarga y genera `.mrpack` + pack de servidor
  (**bloqueado hasta aprobación**).
- CI que valida y verifica en cada cambio.

## 1. Librerías / dependencias (15)

No aportan contenido; las exigen otros mods. Todas ligeras.

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Fabric API | Base obligatoria de Fabric | ambos | 🟡 | estandar |
| Cloth Config API | Configuraciones (Lootr, otros) | ambos | 🟢 | estandar |
| Balm | Base de Waystones y Comforts | ambos | 🟢 | estandar |
| Moonlight Lib | Base de Supplementaries | ambos | 🟡 | estandar |
| YUNG's API | Base de estructuras YUNG | servidor | 🟢 | estandar |
| BCLib | Base de Better Nether/End | ambos | 🟡 | confirmada |
| RebornCore | Base de Tech Reborn | ambos | 🟡 | estandar |
| Spell Engine | Sistema de hechizos (Wizards/Archers) | ambos | 🟡 | confirmada |
| Runes | Runas del stack RPG | ambos | 🟢 | pendiente |
| Spell Power Attributes | Atributos de poder de hechizo | ambos | 🟢 | pendiente |
| AzureLib Armor | Render de armaduras RPG | ambos | 🟡 | pendiente |
| Structure Pool API | Piezas de las torres de magos | ambos | 🟢 | pendiente |
| GeckoLib | Animaciones del stack RPG | ambos | 🟡 | pendiente |
| playerAnimator | Animaciones de Better Combat | ambos | 🟢 | pendiente |
| Badges Lib | Posible dependencia de WTHIT | cliente | 🟢 | pendiente |

## 2. Optimización servidor y lógica (5)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Lithium | Optimiza lógica (TPS); imprescindible | ambos | 🛡️ | estandar |
| Krypton | Optimiza red y paquetes de chunks | ambos | 🛡️ | estandar |
| FerriteCore | Reduce RAM en ambos lados; clave para 3/4 GB | ambos | 🛡️ | estandar |
| Noisium | Acelera generación de mundo (Terralith/YUNG's) | ambos | 🛡️ | estandar |
| Alternate Current | Redstone eficiente | servidor | 🛡️ | estandar |

## 3. Optimización cliente / FPS (8)

Combinación estándar tipo “Fabulously Optimized”. Sin esto, 3 GB no lucen.

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Sodium | Motor de render; multiplica FPS | cliente | 🛡️ | estandar |
| Indium | Compat. Sodium ↔ mods con rendering propio | cliente | 🟢 | estandar |
| Sodium Extra | Toggles extra (niebla, partículas, animaciones) | cliente | 🛡️ | estandar |
| Entity Culling | No dibuja entidades ocultas | cliente | 🛡️ | estandar |
| ImmediatelyFast | Acelera entidades e interfaces | cliente | 🛡️ | estandar |
| MoreCulling | Descarta caras no visibles | cliente | 🛡️ | estandar |
| Dynamic FPS | Baja FPS en 2.º plano/minimizado | cliente | 🛡️ | estandar |
| Debugify | Corrige bugs vanilla que dan tirones | cliente | 🟢 | estandar |

## 4. Mundo, exploración y estructuras (12)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Terralith | +100 biomas y cuevas épicas en el overworld | servidor | 🟠* | confirmada |
| YUNG's Better Dungeons | Mazmorras grandes rediseñadas | servidor | 🟡* | confirmada |
| YUNG's Better Mineshafts | Minas variadas | servidor | 🟡* | estandar |
| YUNG's Better Strongholds | Strongholds épicas (endgame) | servidor | 🟡* | estandar |
| YUNG's Better Nether Fortresses | Fortalezas rediseñadas | servidor | 🟡* | estandar |
| Structory | Estructuras con ambiente y lore ligero | servidor | 🟡* | confirmada |
| Towns and Towers | Aldeas/puestos por bioma + barcos | ambos† | 🟡* | confirmada |
| Better End | Reforma total del End (biomas, mobs, rituales) | ambos | 🟠 | confirmada |
| Better Nether | Reforma total del Nether (biomas, mobs, mats.) | ambos | 🟠 | confirmada |
| Waystones | Teletransporte entre piedras; esencial en grupo | ambos | 🟡 | confirmada |
| Nature's Compass | Localiza biomas (vital con Terralith) | ambos | 🟢 | estandar |
| Xaero's Minimap | Minimapa ligero + waypoints | cliente | 🟡 | estandar |

\* Solo consumen en el **servidor** durante la generación; en cliente cuestan ~0.
† Towns and Towers va en ambos pero su worldgen solo trabaja en el servidor.

## 5. Mobs y mundo vivo (4)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Naturalist | 47 animales con comportamientos y drops | ambos | 🟠 | confirmada |
| Friends and Foes | Mobs de las votaciones + mini-jefe Wildfire | ambos | 🟡 | confirmada |
| Corpse | Cadáver con tus objetos al morir | ambos | 🟢 | estandar |
| Villager Names | Aldeanos con nombre; da vida al mundo | servidor | 🟢 | estandar |

## 6. Magia, RPG y combate (6)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Wizards (RPG Series) | Magia: varitas, hechizos, túnicas, torres con loot | ambos | 🟠 | confirmada |
| Archers (RPG Series) | Arcos y progresión a distancia | ambos | 🟡 | estandar |
| Better Combat | Combate animado estilo Minecraft Dungeons | ambos | 🟡 | confirmada |
| Combat Roll | Esquiva con voltereta (mismo autor; integra) | ambos | 🟡 | estandar |
| LevelZ | Habilidades por niveles; progresión a largo plazo | ambos | 🟡 | confirmada |
| Enchanting Infuser | Elige encantamientos pagando XP | ambos | 🟢 | pendiente |

Archers comparte todas las librerías con Wizards: su coste marginal es pequeño.

## 7. Tecnología y almacenamiento (2)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Tech Reborn | El mod tech de Fabric en 1.21.1: máquinas, energía, herramientas | ambos | 🟠 | confirmada |
| Expanded Storage | Cofres/barriles por niveles, estilo vanilla | ambos | 🟡 | confirmada |

⚠️ Expanded Storage está **archivado por su autor** (sin más updates), pero su build
1.21.1 es estable. Al fijar versión exacta el riesgo es bajo; alternativa si se
quiere cero riesgo: solo Tech Reborn + shulkers vanilla.

## 8. Construcción y decoración (2)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Supplementaries | Deco + cacharros vanilla+ (jarras, veletas, relojes, globos...) | ambos | 🟡 | confirmada |
| Another Furniture | Muebles vanilla (sillas, mesas, estanterías), sin deps extra | ambos | 🟡 | confirmada |

Se eligieron **dos** mods complementarios (cachivaches vs muebles) en vez del set de
Macaw's (una docena de ficheros con solapes parciales).

## 9. Comida y agricultura (2)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Farmer's Delight Refabricated | Cocina y cultivos con progresión (compatible EMI) | ambos | 🟡 | confirmada |
| AppleSkin | Hambre/saturación visibles en el HUD | cliente | 🟢 | estandar |

## 10. Multijugador y diversión (4)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Simple Voice Chat | Voz por proximidad dentro del juego | ambos | 🟡 | confirmada |
| Emotecraft | Emotes/bailes visibles por todos | ambos | 🟡 | confirmada |
| Comforts | Sacos de dormir y hamacas (sin liar spawns) | ambos | 🟢 | estandar |
| Lootr | Loot de cofres instanciado por jugador | ambos | 🟡 | confirmada |

Simple Voice Chat necesita un **puerto UDP abierto** en el servidor (típ. 24454):
es el único requisito especial de despliegue de todo el pack.

## 11. Calidad de vida en cliente (8)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| EMI | Visor de recetas (más ligero que REI) | cliente | 🟡 | estandar |
| EMI Loot | Loot de cofres/mobs dentro de EMI | cliente | 🟢 | estandar |
| EMI Trades | Tradeos de aldeanos dentro de EMI | cliente | 🟢 | estandar |
| WTHIT | Info del bloque al mirar (alt. Fabric de Jade) | cliente | 🟢 | estandar |
| Shulker Box Tooltip | Ver dentro de shulkers sin abrirlas | cliente | 🟢 | estandar |
| Mouse Tweaks | Arrastrar/mover objetos con el ratón | cliente | 🟢 | estandar |
| Mod Menu | Lista de mods y sus configs | cliente | 🟢 | estandar |
| Chat Heads | Avatares en el chat | cliente | 🟢 | estandar |

## 12. Calidad de vida en supervivencia (3)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| FallingTree | Talar árboles enteros de golpe | ambos | 🟡 | estandar |
| Cosecha con clic derecho | Cosechar sin replantar a mano | ambos | 🟢 | pendiente |
| Leaves Be Gone | Hojas que caen rápido al talar | servidor | 🟢 | estandar |

## 13. Administración del servidor (3)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Chunky | Pre-genera el mundo (evita lag al explorar) | servidor | 🟢 | estandar |
| Spark | Profiler de TPS/lag para diagnosticar | servidor | 🟢 | estandar |
| Ledger | Registro + rollback de bloques (antigriefing) | servidor | 🟡 | estandar |

## 14. Dependencias (resumen de verificación)

Verificadas contra Modrinth en esta propuesta: Supplementaries→{Moonlight, Fabric API};
Farmer's Delight→{Fabric API (+EMI opcional)}; Better Nether/End→{BCLib, Fabric API};
Wizards→{Spell Engine, Runes, AzureLib Armor, Structure Pool API, Spell Power,
GeckoLib, Fabric API}; Better Combat→{Fabric API, playerAnimator};
Emotecraft→{Fabric API} (+playerAnimator embebido); Waystones→{Balm};
Lootr→{Cloth Config, Fabric API}; LevelZ→{Fabric API}. El resto son estándar
(solo Fabric API). `resolver.py` re-verifica **todo** automáticamente, incluyendo
que no falte ninguna dependencia `required`, antes de fijar versiones.

## 15. Compatibilidad entre mods (puntos revisados)

- **Sodium + Indium**: Indium es obligatorio porque Supplementaries/Farmer's Delight
  usan Fabric Renderer API; sin Indium se verían mal. Sodium Extra, Entity Culling,
  ImmediatelyFast y MoreCulling son la combinación estándar probada.
- **Terralith + YUNG's + Structory + Towns and Towers**: estructuras compatibles con
  Terralith (documentado por sus autores); Better Nether/End tocan otras dimensiones,
  sin conflicto con el overworld. YUNG's Nether Fortresses + Better Nether conviven
  (combinación habitual en la comunidad).
- **Lootr + mazmorras**: Lootr intercepta contenedores vanilla con loot tables, por lo
  que funciona con el loot de YUNG's/Structory/vanilla. Loot por jugador en grupo. ✔
- **Stack RPG**: Wizards + Archers + Better Combat + Combat Roll son del mismo autor
  y están diseñados para integrarse (animaciones y mecánicas).
- **Emotecraft + Better Combat**: Emotecraft embebe playerAnimator; Better Combat lo
  pide externo. Combinación habitual sin conflictos conocidos.
- **Ledger + Lootr/Corpse**: Ledger registra bloques vanilla; los inventarios
  virtuales de Lootr/Corpse no interfieren.
- **Simple Voice Chat**: independiente del resto; su único requisito es red (UDP).
- **Tech Reborn + optimización**: compatible con Lithium/FerriteCore; su red de
  energía es propia y no choca con nada del pack (no hay otros mods tech).
- **Expanded Storage (archivado)**: riesgo bajo con versión fijada; si preocupa, se
  retira y queda Tech Reborn + vanilla (ver §7).

## 16. Estimación de RAM (aprox., orientativa)

- **Cliente (3 GB)**: base 1.21.1/Fabric ≈ 1,2–1,5 GB + contenido ≈ 0,8–1,1 GB −
  ahorro de FerriteCore/Sodium. **Cabe en 3 GB** con margen si no se añaden shaders
  ni packs de texturas pesados. El mayor coste cliente: Better Nether/End, Naturalist,
  Tech Reborn, Wizards y EMI (caché de recetas).
- **Servidor (4 GB)**: base ≈ 1 GB + worldgen (Terralith/YUNG's) y entidades con
  4–6 jugadores ≈ 1,5–2,5 GB. **Cabe en 4 GB** con: pre-generación (Chunky, radio
  3k–5k), `view-distance` 6–8, `simulation-distance` 4–6 y flags G1GC/Aikar.
- Cuello de botella esperado: **generación de chunks al explorar** (se mitiga con
  Chunky + Noisium), no la RAM en reposo.

## 17. Opcionales (18, no incluidos salvo petición)

| Mod | Lado | Por qué es opcional |
| --- | --- | --- |
| Iris Shaders | cliente | Shaders con 3 GB solo para GPUs potentes; cada jugador decide |
| Xaero's World Map | cliente | Mapa completo: más RAM/disco que el minimapa |
| Litematica + Malilib | cliente | Solo para constructores (planos) |
| Sound Physics Remastered | cliente | Reverberación; combina con el chat de voz |
| Presence Footsteps | cliente | Pasos según superficie; atmósfera gratis |
| Not Enough Animations | cliente | Animaciones en 1.ª persona |
| Eating Animation | cliente | Animación al comer (pendiente de verificar) |
| Tectonic | servidor | Terreno aún más épico, pero sube coste de generación |
| Chipped (+ Architectury) | ambos | Miles de variantes; pesa en cliente (texturas) |
| Macaw's Doors/Windows/Roofs | ambos | Más deco si se quiere variedad extra |
| LuckPerms | servidor | Solo si hacen falta rangos más allá de OP |
| No Chat Reports | ambos | Quita reportes a Mojang (servidor privado) |
| DeathLog | servidor | Historial de muertes (pendiente de verificar) |
| ServerCore | servidor | Solo si Lithium no bastara; solapa parcial |

Los opcionales de **cliente** no rompen la paridad: cada jugador puede añadirlos
o no por su cuenta.

## 18. Descartados y por qué

| Mod descartado | Motivo |
| --- | --- |
| Create | Sin Fabric para 1.21.1 (oficialmente NeoForge; port retirado) |
| Modern Industrialization | Desde 1.20.4 solo NeoForge; en Fabric se quedó en 1.20.1 → Tech Reborn |
| Industrial Revolution | Sin 1.21.1 confirmado → Tech Reborn |
| Mekanism / RS / AE2 / Powah / Pipez | Solo Forge/NeoForge |
| Iron's Spells / Ars Nouveau | Solo Forge/NeoForge → Wizards |
| Botania | Pesado + soporte Fabric dudoso; solapa con Wizards |
| Biomes O' Plenty / BYG | Sin Fabric 1.21.1 fiable → Terralith |
| Epic Fight | Solo Forge/NeoForge → Better Combat + Combat Roll |
| Jade | En Fabric se usa WTHIT |
| REI | Duplica a EMI siendo más pesado (pide Architectury) |
| JourneyMap | Mucho más pesado que Xaero's |
| Drawers / Sophisticated / Tom's | Forge/NeoForge o sin port → Expanded Storage |
| Functional Storage | Sin Fabric oficial 1.21.1; port no oficial diminuto y arriesgado |
| FramedBlocks | Solo Forge/NeoForge |
| Explorer's Compass | Duplica parcialmente a Nature's Compass |
| When Dungeons Arise / Born in Chaos | Estructuras pesadas; YUNG's+Structory+T&T cubren el hueco |
| Guard Villagers | Sin build 1.21.1/Fabric confirmada |
| C2ME | Inestabilidad conocida con worldgen; riesgo inaceptable |
| ModernFix | Riesgo de conflictos; Lithium+Krypton+FerriteCore bastan |
| VMP | Para cientos de jugadores; overkill |
| Architectury (core) | Nadie del core la pide; no añadir peso muerto |
| Essential Mod | Servicio externo cerrado; no encaja con servidor propio |

## 19. Decisiones que necesito de ti

1. **Aprobar / recortar / cambiar** esta selección (74 core + 18 opcionales).
2. **Simple Voice Chat**: ¿OK abrir un puerto UDP en el servidor? (Si no, se quita.)
3. **Expanded Storage**: ¿aceptas el mod archivado (v1.21.1 estable fijada) o lo
   quitamos y queda Tech Reborn + vanilla?
4. **Opcionales**: ¿alguno pasa a core? (p. ej. Xaero's World Map, Tectonic, Chipped).
5. **Dificultad**: LevelZ + Better Combat asumen progresión suave. ¿Quieres más
   desafío (más hostiles/jefes) o así está bien para empezar?

## 20. Siguientes pasos (tras tu revisión)

1. Ajustar `modpack/modpack.yml` según tu respuesta.
2. Cambiar `estado_global` a `aprobado`.
3. `resolver.py --guardar` fija versiones exactas (CI lo verifica antes).
4. `construir.py` genera `.mrpack` + `servidor.zip`.
5. Probar en local, y **solo entonces** hablar de despliegue.
