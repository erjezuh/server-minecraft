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

- Manifiesto único (`modpack/modpack.yml`) con 86 mods core + 11 opcionales (revisión 3.2, 3 jugadores).
- `scripts/resolver.py`: verifica compatibilidad 1.21.1/Fabric, lado y dependencias
  contra Modrinth **sin descargar nada**.
- `scripts/construir.py`: descarga y genera `.mrpack` + pack de servidor
  (**bloqueado hasta aprobación**).
- CI que valida y verifica en cada cambio.

## 1. Librerías / dependencias (24)

No aportan contenido; las exigen otros mods. Todas ligeras.

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Fabric API | Base obligatoria de Fabric | ambos | 🟡 | estandar |
| Cloth Config API | Configuraciones (Lootr, otros) | ambos | 🟢 | estandar |
| Balm | Base de Waystones y Comforts | ambos | 🟢 | estandar |
| Moonlight Lib | Base de Supplementaries | ambos | 🟡 | estandar |
| YUNG's API | Base de estructuras YUNG | ambos | 🟢 | confirmada |
| Cristel Lib | Configs de estructuras (Towns and Towers) | servidor | 🟢 | confirmada |
| LibZ | Base de LevelZ | ambos | 🟢 | confirmada |
| WorldWeaver | Base de BCLib/BetterNether/BetterEnd | ambos | 🟡 | confirmada |
| Lithostitched | Worldgen de Terralith | servidor | 🟢 | confirmada |
| YACL | Pantallas de config (Debugify) | cliente | 🟢 | confirmada |
| Bundle API | Base de Runes | ambos | 🟢 | confirmada |
| BCLib | Base de Better Nether/End | ambos | 🟡 | confirmada |
| RebornCore (`reborncore`, sin guion) | Base de Tech Reborn | ambos | 🟡 | confirmada |
| Spell Engine | Sistema de hechizos (Wizards/Archers) | ambos | 🟡 | confirmada |
| Runes | Runas/munición de hechizos (Wizards) | ambos | 🟢 | confirmada |
| Spell Power Attributes | Atributos de poder (Spell Engine) | ambos | 🟢 | confirmada |
| Armor Model API | Túnicas/armaduras RPG vía pipeline vanilla | ambos | 🟡 | confirmada |
| Structure Pool API | Piezas de torres (Wizards/Archers) | ambos | 🟢 | confirmada |
| Ranged Weapon API | Arcos funcionales (Archers) | ambos | 🟢 | confirmada |
| Trinkets | Slots de accesorios (libro de hechizos) | ambos | 🟡 | confirmada |
| Resourceful Lib | Base de Friends and Foes | ambos | 🟡 | confirmada |
| playerAnimator | Animaciones (Spell Engine, Better Combat, Combat Roll) | ambos | 🟢 | confirmada |
| Bad Packets | Red de WTHIT | cliente | 🟢 | confirmada |
| Polymer | Contenido server-side (Universal Graves) | servidor | 🟡 | confirmada |

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

## 4. Mundo, exploración y estructuras (13)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Terralith | +100 biomas y cuevas épicas en el overworld | servidor | 🟠* | confirmada |
| YUNG's Better Dungeons | Mazmorras grandes rediseñadas | servidor | 🟡* | confirmada |
| YUNG's Better Mineshafts | Minas variadas | servidor | 🟡* | estandar |
| YUNG's Better Strongholds | Strongholds épicas (endgame) | servidor | 🟡* | estandar |
| YUNG's Better Nether Fortresses | Fortalezas rediseñadas | servidor | 🟡* | estandar |
| Structory | Estructuras con ambiente y lore ligero | servidor | 🟡* | confirmada |
| Towns and Towers | Aldeas/puestos por bioma + barcos | servidor | 🟡* | confirmada |
| Better End | Reforma total del End (biomas, mobs, rituales) | ambos | 🟠 | confirmada |
| Better Nether | Reforma total del Nether (biomas, mobs, mats.) | ambos | 🟠 | confirmada |
| Waystones | Teletransporte entre piedras; esencial en grupo | ambos | 🟡 | confirmada |
| Nature's Compass | Localiza biomas (vital con Terralith) | ambos | 🟢 | estandar |
| Xaero's Minimap | Minimapa ligero + waypoints | cliente | 🟡 | estandar |
| Xaero's World Map | Mapa de pantalla completa | cliente | 🟡 | confirmada |

\* Solo consumen en el **servidor** durante la generación; en cliente cuestan ~0.

## 5. Mobs y mundo vivo (2)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Naturalist | 47 animales con comportamientos y drops | ambos | 🟠 | confirmada |
| Friends and Foes | Mobs de las votaciones + mini-jefe Wildfire | ambos | 🟡 | confirmada |

## 6. Magia, RPG y combate (5)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Wizards (RPG Series) | Magia: varitas, hechizos, túnicas, torres con loot | ambos | 🟠 | confirmada |
| Archers (RPG Series) | Arcos y progresión a distancia | ambos | 🟡 | estandar |
| Better Combat | Combate animado estilo Minecraft Dungeons | ambos | 🟡 | confirmada |
| Combat Roll | Esquiva con voltereta (mismo autor; integra) | ambos | 🟡 | estandar |
| LevelZ | Habilidades por niveles; progresión a largo plazo | ambos | 🟡 | confirmada |

Archers comparte casi todas las librerías con Wizards (solo añade Ranged Weapon API): su coste marginal es pequeño.

## 7. Tecnología (1)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Tech Reborn | El mod tech de Fabric en 1.21.1: máquinas, energía, herramientas | ambos | 🟠 | confirmada |

Almacén (sin mod dedicado tras salir Expanded Storage): Tech Reborn aporta
Quantum Chest/Tank para el late game; early game con cofres vanilla + shulkers
(con Shulker Box Tooltip). Suficiente para 3 jugadores.

## 8. Construcción y decoración (5)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Supplementaries | Deco + cacharros vanilla+ (jarras, veletas, relojes, globos...) | ambos | 🟡 | confirmada |
| Another Furniture | Muebles vanilla (sillas, mesas, estanterías), sin deps extra | ambos | 🟡 | confirmada |
| Macaw's Doors | Puertas de todos los estilos | ambos | 🟡 | confirmada |
| Macaw's Windows | Ventanas, cristales, persianas, cortinas | ambos | 🟡 | confirmada |
| Macaw's Roofs | Tejados, canalones y toldos | ambos | 🟡 | confirmada |

Base: Supplementaries (cachivaches) + Another Furniture (muebles) + 3 de Macaw's
(puertas/ventanas/tejados, sin solape con los anteriores). El resto de Macaw's y
Chipped quedan opcionales.

## 9. Comida y agricultura (2)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Farmer's Delight Refabricated | Cocina y cultivos con progresión (compatible EMI) | ambos | 🟡 | confirmada |
| AppleSkin | Hambre/saturación visibles en el HUD | cliente | 🟢 | estandar |

## 10. Multijugador y diversión (5)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Simple Voice Chat | Voz por proximidad (requiere puerto UDP 24454 en servidor) | ambos | 🟡 | confirmada |
| Emotecraft | Emotes/bailes visibles por todos | ambos | 🟡 | confirmada |
| Comforts | Sacos de dormir y hamacas (sin liar spawns) | ambos | 🟢 | estandar |
| Lootr | Loot de cofres instanciado por jugador | ambos | 🟡 | confirmada |
| Universal Graves | Tumbas con tus objetos y XP al morir | servidor | 🟡 | confirmada |

Simple Voice Chat necesita un **puerto UDP abierto** en el servidor (24454 por
defecto): es el requisito principal de despliegue. Además, Universal Graves usa
Polymer AutoHost: los 3 jugadores aceptan el resource pack del servidor al entrar
(un clic, mecanismo vanilla).

## 11. Calidad de vida e inmersión en cliente (10)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| EMI | Visor de recetas (más ligero que REI) | cliente | 🟡 | estandar |
| EMI Loot | Loot de cofres/mobs dentro de EMI | cliente | 🟢 | estandar |
| WTHIT | Info del bloque al mirar (alt. Fabric de Jade) | cliente | 🟢 | estandar |
| Shulker Box Tooltip | Ver dentro de shulkers sin abrirlas | cliente | 🟢 | estandar |
| Mouse Tweaks | Arrastrar/mover objetos con el ratón | cliente | 🟢 | estandar |
| Mod Menu | Lista de mods y sus configs | cliente | 🟢 | estandar |
| Chat Heads | Avatares en el chat | cliente | 🟢 | estandar |
| Sound Physics Remastered | Reverberación/oclusión; integra el chat de voz | cliente | 🟡 | confirmada |
| Presence Footsteps | Pasos según superficie (se oyen los de otros) | cliente | 🟡 | confirmada |
| Eating Animation | Comida/bebida animada, visible para los demás | cliente | 🟢 | confirmada |

## 12. Calidad de vida en supervivencia (3)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| FallingTree | Talar árboles enteros de golpe | ambos | 🟡 | estandar |
| Simple Harvest | Cosecha y replanta con clic derecho | servidor | 🟢 | confirmada |
| Leaves Be Gone | Hojas que caen rápido al talar | servidor | 🟢 | estandar |

## 13. Administración del servidor (3)

| Mod | Para qué sirve | Lado | Impacto | Verif. |
| --- | --- | --- | --- | --- |
| Chunky | Pre-genera el mundo (evita lag al explorar) | servidor | 🟢 | estandar |
| Spark | Profiler de TPS/lag para diagnosticar | servidor | 🟢 | estandar |
| Ledger | Registro + rollback de bloques (antigriefing) | servidor | 🟡 | estandar |

## 14. Dependencias (resumen de verificación)

Cada dependencia `required` se comprobó por ID de proyecto en la API de Modrinth
(revisión 3); no se confía en listados de terceros:

- Fabric API ← todo el pack.
- Cloth Config ← Lootr, Spell Engine, Combat Roll.
- Balm ← Waystones, Comforts. · Moonlight ← Supplementaries. · BCLib ← Better Nether/End.
- `reborncore` (sin guion) ← Tech Reborn. · YUNG's API ← YUNG's ×4. · Cristel Lib ← Towns and Towers. · LibZ ← LevelZ. · WorldWeaver ← BCLib/BetterNether/BetterEnd. · Lithostitched ← Terralith. · YACL ← Debugify. · Bundle API ← Runes.
- Wizards ← {Spell Engine, Runes, Armor Model API, Structure Pool API, Fabric API}.
- Archers ← {Spell Engine, Ranged Weapon API, Armor Model API, Structure Pool API, Fabric API}.
- Spell Engine ← {Spell Power, Trinkets, Cloth Config, playerAnimator, Fabric API}.
- Friends and Foes ← {Resourceful Lib, Fabric API}. · Naturalist ← {Fabric API}.
- Better Combat ← {Fabric API, playerAnimator}; Combat Roll ← {Fabric API, Cloth Config, playerAnimator}.
- WTHIT ← {Fabric API, Bad Packets} (cliente). · Emotecraft ← {Fabric API} (+playerAnimator embebido).
- Universal Graves ← {Polymer} (servidor). · Macaw's ×3 ← {Fabric API}. · Xaero's World Map ← {Fabric API (+Minimapa opcional)}. · Sound Physics ← {todo opcional}. · Presence Footsteps, Eating Animation ← {sin dependencias}.
- El resto: solo Fabric API. `resolver.py` re-verifica **todo** en CI antes de fijar versiones.

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
- **Armor Model API**: el stack RPG 3.x dibuja túnicas por el pipeline vanilla
  (compatible con Sodium/Iris por diseño); no hacen falta GeckoLib ni AzureLib.
- **Towns and Towers solo-servidor**: Modrinth lo marca servidor-requerido y
  cliente-opcional; moverlo al servidor ahorra megas en clientes de 3 GB.
- **Bad Packets**: librería de red exigida por WTHIT; viaja solo en cliente con él.
- **Trinkets**: exigido por Spell Engine (slot del libro de hechizos); estándar
  de Fabric con versión 1.21.1.
- **Universal Graves + Polymer**: 100% servidor (coste 0 en cliente); AutoHost sirve
  el resource pack (aceptar al entrar). Sustituye a Corpse, que no tiene Fabric.
- **Macaw's ×3**: sin solape (Supplementaries/Another Furniture no hacen
  puertas/ventanas/tejados); cada uno solo pide Fabric API.
- **Sound Physics + SVC**: integración oficial voz↔reverberación; si la build alpha
  diera guerra, se retira sin tocar el servidor (es solo cliente).
- **Almacén sin mod dedicado**: TR Quantum + vanilla; cero riesgo de abandonos.

## 16. Estimación de RAM y veredicto de carga (revisión 3.2)

Tamaños de `.jar` verificados (los más grandes): Naturalist 11,3 MB · Tech Reborn
6,4 MB · Simple Voice Chat 6,3 MB · Presence Footsteps 5,7 MB (sonidos) ·
Friends and Foes 5,1 MB · Spell Engine 4,7 MB · Wizards 4,5 MB · Farmer's Delight
2,9 MB · Terralith 2,8 MB · Another Furniture 2,3 MB · Macaw's ×3 ≈ 4,2 MB ·
Xaero's World Map 1,5 MB · Universal Graves 1,7 MB* (*solo servidor) ·
WorldWeaver 2,4 MB · YACL 1,1 MB · Lithostitched 0,9 MB*. Total por
cliente ≈ 80–95 MB (una sola vez).

- **Cliente (3 GB)**: base 1.21.1/Fabric ≈ 1,2–1,5 GB + contenido ≈ 0,8–1,1 GB −
  ahorro de FerriteCore/Sodium. **Veredicto: CABE con margen** (~2–2,6 GB en juego
  normal). Los 6 únicos 🟠 (Terralith*, Better Nether/End, Naturalist, Wizards,
  Tech Reborn) no pican a la vez: *Terralith solo trabaja en servidor. Condición:
  sin shaders ni packs HD (Iris queda opcional).
- **Servidor (4 GB)**: base ≈ 1 GB + worldgen y entidades (3 jugadores: tú, Rafa y Dani) ≈
  1,5–2,5 GB. **Veredicto: CABE** con pre-generación Chunky (radio 3k–4k, de sobra para 3),
  `view-distance` 6–8, `simulation-distance` 4–6 y flags G1GC/Aikar. El combo
  Terralith + YUNG's ×4 + Structory + T&T es viable: las estructuras solo cuestan
  al generar el chunk (checks baratos + eventos raros); Terralith es el único coste
  por chunk y Better Nether/End solo consumen dentro de su dimensión.
- Costes singulares revisados: **Naturalist** (11,3 MB de assets, 🟠) aporta 47
  animales dentro de los mob caps vanilla — variedad, no cantidad —; **Wizards**
  (4,5 MB + stack compartido ≈ 12–14 MB en total, 🟠) es la única magia seria en
  Fabric 1.21.1; **Tech Reborn** (6,4 MB, 🟠) es el único tech en Fabric 1.21.1 con
  red de energía propia y sin conflictos. Los tres se quedan: pilar de contenido.
- Cuello de botella esperado: **generación de chunks al explorar** (Chunky +
  Noisium lo mitigan), no la RAM en reposo.

## 17. Opcionales (11, no incluidos salvo petición)

| Mod | Lado | Por qué es opcional |
| --- | --- | --- |
| Iris Shaders | cliente | Shaders con 3 GB solo para GPUs potentes; cada jugador decide |
| Litematica + Malilib | cliente | Nicho de constructores; añadible por cada uno |
| Not Enough Animations | cliente | Solo tu propia vista; añadible por cada uno |
| Tectonic | servidor | Más épico, pero arriesga los 4 GB; Terralith basta |
| Chipped (+ Architectury) | ambos | Miles de variantes (14,3 MB); Macaw's cubre deco con ~4 MB |
| LuckPerms | servidor | Solo si hacen falta rangos más allá de OP |
| No Chat Reports | ambos | Quita reportes a Mojang (servidor privado) |
| ServerCore | servidor | Solo si Lithium no bastara; solapa parcial |
| EMI Trades Reborn | cliente | Fork 1.21.1 de EMI Trades; solo 282 descargas, sin verificar a fondo |

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
| EMI Trades | Sin build 1.21.1 (llega a 1.20.4); slug inexistente. Fork Reborn en opcionales |
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
| Enchanting Infuser | Pide Puzzles Lib + Forge Config API Port para un lujo menor |
| GeckoLib | Nada del pack la requiere (verificado por IDs) |
| AzureLib Armor | El stack RPG usa Armor Model API |
| Reap (`reap`) | Slug erróneo: es otro mod (solo MC 26.2) → Simple Harvest |
| Badges Lib (`badges-lib`) | Slug inexistente (404) → Bad Packets |
| DeathLog | Sin build 1.21.1; las tumbas las cubre Universal Graves |
| Expanded Storage | Archivado/abandonado (decisión del usuario); almacén via TR + vanilla |
| Corpse | Sin versión Fabric (forge+neoforge); sustituido por Universal Graves |
| Villager Names | Sin build 1.21.1 (abandonado en 2024); capricho menor |
| Nature's Compass (`nature-s-compass`) | Slug inexistente (404) → `natures-compass` |

## 19. Decisiones que necesito de ti

1. **Aprobar / recortar / cambiar** esta selección (86 core + 11 opcionales, rev 3.2).
2. **Simple Voice Chat**: ✅ se queda; documentado requisito UDP 24454.
3. **Expanded Storage**: ✅ eliminado por archivado; almacén via TR + vanilla.
4. **Opcionales**: ✅ triage hecho — promocionan World Map, Sound Physics,
   Footsteps, Eating Animation y Macaw's ×3; el resto fuera (ver §17).
5. **Dificultad**: LevelZ + Better Combat asumen progresión suave. ¿Quieres más
   desafío (más hostiles/jefes) o así está bien para empezar?

## 20. Siguientes pasos (tras tu revisión)

1. Ajustar `modpack/modpack.yml` según tu respuesta.
2. Cambiar `estado_global` a `aprobado`.
3. `resolver.py --guardar` fija versiones exactas (CI lo verifica antes).
4. `construir.py` genera `.mrpack` + `servidor.zip`.
5. Probar en local, y **solo entonces** hablar de despliegue.

## 21. Historial de revisiones

- **Rev 1**: propuesta inicial (74 core + 18 opcionales).
- **Rev 2**: revisión de rendimiento/estabilidad. Verificados todos los slugs y
  dependencias `required` por ID en la API de Modrinth. Eliminados: Enchanting
  Infuser, GeckoLib, AzureLib Armor, Reap, Badges Lib, DeathLog. Añadidos:
  Armor Model API, Ranged Weapon API, Trinkets, Resourceful Lib, Bad Packets,
  Simple Harvest. Corregidos: `reborncore` (slug), Towns and Towers → solo
  servidor. Resultado: 75 core + 17 opcionales, 0 pendientes en core.
- **Rev 3**: decisiones de usuario (3 jugadores) + triage de opcionales. Eliminados:
  Expanded Storage, Corpse (sin Fabric), Villager Names (sin 1.21.1). Promocionan
  a core: Xaero's World Map, Sound Physics, Footsteps, Eating Animation,
  Macaw's ×3. Nuevos: Universal Graves + Polymer (sustituyen a Corpse, 100%
  servidor). Corregido slug `natures-compass`. SVC confirmado con UDP 24454.
  Resultado: 81 core + 10 opcionales, 0 pendientes en core.
- **Rev 3.1**: fix CI + dependencia descubierta. Entrecomillados valores YAML
  con dos puntos (rompían el parseo), `resolver.py` usa el entorno del proyecto
  (+ flag `lado_verificado_manual`) y añadida Cristel Lib (`required` por
  Towns and Towers). Anotaciones `::error::` para depurar el CI sin logs.
- **Rev 3.2**: dependencias que pedía el CI. Nuevas: LibZ (← LevelZ),
  WorldWeaver (← BCLib/BetterNether/BetterEnd, solo hay alpha para 1.21.1),
  Lithostitched (← Terralith), YACL (← Debugify), Bundle API (← Runes).
  Lados corregidos: Noisium → servidor, YUNG's API → ambos. EMI Trades sale
  del core (sin build 1.21.1; el slug no existe) y su fork Reborn pasa a
  opcionales. Resultado: 86 core + 11 opcionales, 0 pendientes en core.
