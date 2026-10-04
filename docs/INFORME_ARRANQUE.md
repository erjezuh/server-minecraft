# Informe de arranque — servidor 1.0.0 (1.21.1 + fabric)

- Fecha (UTC): 2026-10-04 21:56 UTC.
- Entorno limpio (CI): openjdk version "21.0.12.1" 2026-08-18 LTS; installer 1.1.2; loader 0.19.5; JVM -Xms1G -Xmx4G; nogui.
- Resultado: **LISTO ✔**
- Tiempo hasta listo: 50s; parada limpia: sí (exit 0).
- Memoria: pico RSS ≈ 2391 MB con heap limitado a 4G.
- Mods detectados en Fabric Loader: 5 (esperados en servidor: 68).
- Líneas de error únicas: 117; WARN: 19; crash-reports: 0.

## Checks

- ✔ Llegó a listo (`Done (`).
- ✔ Parada limpia con `stop` (exit 0).
- ✔ Sin crash-reports.
- ✔ Ningún mod de cliente cargado (0 de 23).

## Spotlight

| Mod | Estado | Detalle |
| --- | --- | --- |
| betterend | mencionado | en log |
| betternether | mencionado | en log |
| terralith | mencionado | en log |
| wizards | mencionado | en log |
| techreborn | mencionado | en log |
| universal-graves | mencionado | en log |
| polymer | mencionado | en log |
| simple-voice-chat | mencionado | en log |
| yungs-better-dungeons | mencionado | en log |
| yungs-better-mineshafts | mencionado | en log |
| yungs-better-strongholds | mencionado | en log |
| yungs-better-nether-fortresses | mencionado | en log |
| structory | mencionado | en log |
| towns-and-towers | SIN SEÑAL | aviso |
| lithostitched | mencionado | en log |
| cristel-lib | mencionado | en log |
| noisium | mencionado | en log |
| bclib | mencionado | en log |
| worldweaver | mencionado | en log |

## Mods cargados (Fabric Loader)

- `alternate-current` 1.9.0
- `another_furniture` 4.0.2
- `archers` 3.1.3+1.21.1
- `armor_model_api` 1.1.0+1.21.1
- `balm` 21.0.66

## Líneas de error únicas (117)

- `- Mod 'Forge Config API Port' (forgeconfigapiport) 21.1.6 recommends any version of modmenu, which is missing!`
- `- Mod 'Friends&Foes' (friendsandfoes) 4.0.27 recommends any version of yet_another_config_lib_v3, which is missing!`
- `- Mod 'Friends&Foes' (friendsandfoes) 4.0.27 recommends any version of modmenu, which is missing!`
- `|-- fabric-crash-report-info-v1 0.2.29+0af3f5a719`
- `[21:54:43] [main/WARN]: Error loading class: traben/entity_model_features/models/animation/EMFAnimationEntityContext (java.lang.ClassNotFoundException: traben/entity_model_features/models/animation/EMFAnimationEntityCont`
- `[21:54:43] [main/WARN]: Error loading class: com/electronwill/nightconfig/core/io/IoUtils (java.lang.ClassNotFoundException: com/electronwill/nightconfig/core/io/IoUtils)`
- `[21:54:43] [main/WARN]: Error loading class: com/simibubi/create/content/schematics/SchematicPrinter (java.lang.ClassNotFoundException: com/simibubi/create/content/schematics/SchematicPrinter)`
- `[21:54:43] [main/WARN]: Error loading class: net/minecraft/class_525 (java.lang.ClassNotFoundException: net/minecraft/class_525)`
- `[21:54:43] [main/WARN]: Error loading class: net/caffeinemc/mods/sodium/client/render/chunk/compile/pipeline/DefaultFluidRenderer (java.lang.ClassNotFoundException: net/caffeinemc/mods/sodium/client/render/chunk/compile/`
- `[21:54:44] [main/WARN]: Error loading class: com/simibubi/create/content/kinetics/base/BlockBreakingKineticBlockEntity (java.lang.ClassNotFoundException: com/simibubi/create/content/kinetics/base/BlockBreakingKineticBloc`
- `[21:54:51] [main/ERROR]: No data fixer registered for spirit_wolf`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:alligator`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:ant`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:anglerfish`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:ray`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:blobfish`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:piranha`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:bass`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:bear`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:black_bear`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:bird`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:boar`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:butterfly`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:capybara`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:caterpillar`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:catfish`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:clam`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:crab`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:deer`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:dragonfly`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:duck`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:duck_egg`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:dirt_trail`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:carried_food`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:elephant`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:firefly`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:giant_isopod`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:giraffe`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:great_white_shark`
- `[21:54:55] [main/ERROR]: No data fixer registered for naturalist:hedgehog`

## Warnings (19 total, top 15 únicos)

- `[21:54:42] [main/WARN]: Warnings were found!`
- `[21:54:42] [main/WARN]: Reference map 'balm.refmap.json' for balm.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[21:54:42] [main/WARN]: Reference map 'balm.refmap.json' for balm.fabric.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[21:54:42] [main/WARN]: Reference map 'forgeconfigapiport.common.refmap.json' for forgeconfigapiport.common.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[21:54:42] [main/WARN]: Reference map 'leavesbegone.fabric.refmap.json' for leavesbegone.fabric.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[21:54:42] [main/WARN]: Mod 'supplementaries' attempted to override option 'mixins.block.moving_block_shapes', which doesn't exist, ignoring`
- `[21:54:42] [main/WARN]: Reference map 'tiny_config-common-common-refmap.json' for tiny_config.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[21:54:42] [main/WARN]: Reference map 'waystones.refmap.json' for waystones.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[21:54:42] [main/WARN]: Reference map 'waystones.refmap.json' for waystones.fabric.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[21:54:43] [main/WARN]: Error loading class: traben/entity_model_features/models/animation/EMFAnimationEntityContext (java.lang.ClassNotFoundException: traben/entity_model_features/models/animation/EMFAnimationEntityCont`
- `[21:54:43] [main/WARN]: Error loading class: com/electronwill/nightconfig/core/io/IoUtils (java.lang.ClassNotFoundException: com/electronwill/nightconfig/core/io/IoUtils)`
- `[21:54:43] [main/WARN]: Error loading class: com/simibubi/create/content/schematics/SchematicPrinter (java.lang.ClassNotFoundException: com/simibubi/create/content/schematics/SchematicPrinter)`
- `[21:54:43] [main/WARN]: Error loading class: net/minecraft/class_525 (java.lang.ClassNotFoundException: net/minecraft/class_525)`
- `[21:54:43] [main/WARN]: @Mixin target net.minecraft.class_525 was not found moonlight.mixins.json:CreateWorldScreenMixin from mod moonlight`
- `[21:54:43] [main/WARN]: Error loading class: net/caffeinemc/mods/sodium/client/render/chunk/compile/pipeline/DefaultFluidRenderer (java.lang.ClassNotFoundException: net/caffeinemc/mods/sodium/client/render/chunk/compile/`

## Cola del log (últimas 30 líneas)

```
[21:55:21] [Worker-Main-2/INFO]: Preparing spawn area: 51%
[21:55:21] [Worker-Main-2/INFO]: Preparing spawn area: 51%
[21:55:21] [Worker-Main-1/INFO]: Preparing spawn area: 51%
[21:55:22] [Worker-Main-3/INFO]: Preparing spawn area: 51%
[21:55:22] [Worker-Main-1/INFO]: Preparing spawn area: 51%
[21:55:23] [Worker-Main-3/INFO]: Preparing spawn area: 51%
[21:55:23] [Worker-Main-2/INFO]: Preparing spawn area: 75%
[21:55:23] [Server thread/INFO]: Time elapsed: 9095 ms
[21:55:23] [Server thread/INFO]: Done (18.415s)! For help, type "help"
[21:55:24] [Server thread/INFO]: Added 2 Biomes
[21:55:24] [Server thread/INFO]:  - minecraft:end_midlands, subbiomes=1
[21:55:24] [Server thread/INFO]:  - minecraft:end_barrens, subbiomes=1
[21:55:24] [Server thread/INFO]: Added 2 Biomes
[21:55:24] [Server thread/INFO]:  - minecraft:end_midlands, subbiomes=1
[21:55:24] [Server thread/INFO]:  - minecraft:end_barrens, subbiomes=1
[21:55:24] [VoiceChatServerThread/INFO]: [voicechat] Voice chat server started at port 24454
[21:55:40] [Server thread/INFO]: Stopping the server
[21:55:40] [Server thread/INFO]: Stopping server
[21:55:40] [Server thread/INFO]: Saving players
[21:55:40] [Server thread/INFO]: Saving worlds
[21:55:41] [Server thread/INFO]: saving Alternate Current config
[21:55:41] [Server thread/INFO]: Saving chunks for level 'ServerLevel[world]'/minecraft:overworld
[21:55:41] [Server thread/INFO]: Saving chunks for level 'ServerLevel[world]'/minecraft:the_nether
[21:55:41] [Server thread/INFO]: Saving chunks for level 'ServerLevel[world]'/minecraft:the_end
[21:55:41] [Server thread/INFO]: ThreadedAnvilChunkStorage (world): All chunks are saved
[21:55:41] [Server thread/INFO]: ThreadedAnvilChunkStorage (DIM-1): All chunks are saved
[21:55:41] [Server thread/INFO]: ThreadedAnvilChunkStorage (DIM1): All chunks are saved
[21:55:41] [Server thread/INFO]: ThreadedAnvilChunkStorage: All dimensions are saved
[21:55:41] [Server thread/INFO]: Successfully drained database queue
[21:55:41] [Server thread/INFO]: Dispatching unloading event for config leavesbegone-server.toml
```

## Reproducir

```bash
pip install -r scripts/requirements.txt
python3 scripts/construir.py --resolucion modpack/resolucion.json --salida build/
mkdir -p prueba/servidor && cd prueba/servidor && \
  unzip -o ../../build/servidor.zip && \
  java -jar /tmp/fabric-installer.jar server -mcversion 1.21.1 -loader 0.19.5 -downloadMinecraft && echo eula=true > eula.txt && cd ../..
python3 scripts/probar_servidor.py --dir prueba/servidor \
    --resolucion modpack/resolucion.json --informe docs/INFORME_ARRANQUE.md
```
