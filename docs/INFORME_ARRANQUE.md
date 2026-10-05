# Informe de arranque — servidor 1.0.0 (1.21.1 + fabric)

- Fecha (UTC): 2026-10-04 22:23 UTC.
- Entorno limpio (CI): openjdk version "21.0.12.1" 2026-08-18 LTS; installer 1.1.2; loader 0.19.5; JVM -Xms1G -Xmx4G; nogui.
- Resultado: **LISTO ✔**
- Tiempo hasta listo: 50s; parada limpia: sí (exit 0).
- Memoria: pico RSS ≈ 1875 MB con heap limitado a 4G.
- Mods detectados en Fabric Loader: 174 (esperados en servidor: 68).
- Líneas de error únicas: 120; WARN: 20; crash-reports: 0.

## Checks

- ✔ Llegó a listo (`Done (`).
- ✔ Parada limpia con `stop` (exit 0).
- ✔ Sin crash-reports.
- ✔ Ningún .jar de cliente en servidor/ (68 jars auditados).
- ⚠ Modids de cliente en loader: placeholder-api (embebido JiJ: su jar no está instalado)

## Spotlight

| Mod | Estado | Detalle |
| --- | --- | --- |
| betterend | cargado | betterend |
| betternether | cargado | betternether |
| terralith | cargado | terralith |
| wizards | cargado | wizards |
| techreborn | cargado | techreborn |
| universal-graves | cargado | universal-graves |
| polymer | mencionado | en log |
| simple-voice-chat | mencionado | en log |
| yungs-better-dungeons | mencionado | en log |
| yungs-better-mineshafts | mencionado | en log |
| yungs-better-strongholds | mencionado | en log |
| yungs-better-nether-fortresses | mencionado | en log |
| structory | cargado | structory |
| towns-and-towers | SIN SEÑAL | aviso |
| lithostitched | cargado | lithostitched |
| cristel-lib | cargado | cristellib |
| noisium | cargado | noisium |
| bclib | cargado | bclib |
| worldweaver | mencionado | en log |

## Mods cargados (Fabric Loader)

- `alternate-current` 1.9.0
- `another_furniture` 4.0.2
- `apollib` 1.2.0
- `archers` 3.1.3+1.21.1
- `armor_model_api` 1.1.0+1.21.1
- `balm` 21.0.66
- `bclib` 21.0.13
- `bettercombat` 2.4.0+1.21.1
- `betterdungeons` 1.21.1-Fabric-5.1.4
- `betterend` 21.0.11
- `betterfortresses` 1.21.1-Fabric-3.1.5
- `bettermineshafts` 1.21.1-Fabric-5.1.1
- `betternether` 21.0.11
- `betterstrongholds` 1.21.1-Fabric-5.1.3
- `blue_endless_jankson` 1.2.3
- `bundleapi` 1.1.0
- `cardinal-components-base` 6.1.2
- `cardinal-components-entity` 6.1.2
- `chunky` 1.4.23
- `cloth-basic-math` 0.6.1
- `cloth-config` 15.0.140
- `codecui` 1.21.1-1.4.5
- `com_electronwill_night-config_core` 3.8.0
- `com_electronwill_night-config_toml` 3.8.0
- `com_teamresourceful_bytecodecs` 1.1.2
- `com_teamresourceful_yabn` 1.0.3
- `com_velocitypowered_velocity-native` 3.3.0-SNAPSHOT
- `combat_roll` 2.0.6+1.21.1
- `comforts` 9.0.5+1.21.1
- `common-protection-api` 1.0.0
- `cristellib` 3.1.7
- `de_marhali_json5-java` 3.0.0
- `emi_loot` 0.7.9+1.21+fabric
- `emotecraft` 2.4.12
- `fabric-api` 0.116.17+1.21.1
- `fabric-api-base` 0.4.42+6573ed8c19
- `fabric-api-lookup-api-v1` 1.6.72+7b3d111d19
- `fabric-biome-api-v1` 13.0.31+d527f9fd19
- `fabric-block-api-v1` 1.1.0+0bc3503219
- `fabric-block-view-api-v2` 1.0.11+ebb2264e19
- `fabric-command-api-v1` 1.2.49+f71b366f19
- `fabric-command-api-v2` 2.2.28+6ced4dd919
- `fabric-commands-v0` 0.2.66+df3654b319
- `fabric-content-registries-v0` 8.0.19+b559734419
- `fabric-convention-tags-v1` 2.1.7+7f945d5b19
- `fabric-convention-tags-v2` 2.12.0+c3656daa19
- `fabric-crash-report-info-v1` 0.2.29+0af3f5a719
- `fabric-data-attachment-api-v1` 1.4.7+5b36e0f719
- `fabric-data-generation-api-v1` 20.3.0+1eb36c0719
- `fabric-dimensions-v1` 4.0.1+65213ef819
- `fabric-entity-events-v1` 1.8.0+2b27e0a419
- `fabric-events-interaction-v0` 0.7.14+ba9dae0619
- `fabric-game-rule-api-v1` 1.0.53+6ced4dd919
- `fabric-item-api-v1` 11.3.0+467044f319
- `fabric-item-group-api-v1` 4.1.7+def88e3a19
- `fabric-language-kotlin` 1.14.1+kotlin.2.4.20
- `fabric-lifecycle-events-v1` 2.6.0+0865547519
- `fabric-loot-api-v2` 3.0.15+3f89f5a519
- `fabric-loot-api-v3` 1.0.3+3f89f5a519
- `fabric-message-api-v1` 6.0.14+8aaf3aca19
- `fabric-networking-api-v1` 4.3.1+d30f6a7919
- `fabric-object-builder-api-v1` 15.2.1+40875a9319
- `fabric-particles-v1` 4.0.2+6573ed8c19
- `fabric-permissions-api-v0` 0.3.1
- `fabric-recipe-api-v1` 5.0.16+2475392c19
- `fabric-registry-sync-v0` 5.3.2+e3eddc2119
- `fabric-rendering-data-attachment-v1` 0.3.49+73761d2e19
- `fabric-rendering-fluids-v1` 3.1.6+1daea21519
- `fabric-resource-conditions-api-v1` 4.3.0+8dc279b119
- `fabric-resource-loader-v0` 1.3.1+5b5275af19
- `fabric-screen-handler-api-v1` 1.3.91+b559734419
- `fabric-tag-api-v1` 1.3.0+1eb36c0719
- `fabric-transfer-api-v1` 5.4.4+7b3d111d19
- `fabric-transitive-access-wideners-v1` 6.2.0+45b9699719
- `fabricloader` 0.19.5
- `fallingtree` 1.21.1.11
- `farmersdelight` 1.21.1-3.3.6+refabricated
- `ferritecore` 7.0.3
- `forgeconfigapiport` 21.1.6
- `friendsandfoes` 4.0.27
- `fzzy_config` 0.7.7+1.21
- `java` 21
- `krypton` 0.2.8
- `kuma_api` 21.0.8
- `leavesbegone` 21.1.1
- `ledger` 1.3.5
- `levelz` 2.0.11
- `libz` 1.1.0
- `lithium` 0.15.4+mc1.21.1
- `lithostitched` 1.8.0
- `lootr` 1.21.1-1.11.38.127
- `mcwdoors` 1.1.5
- `mcwroofs` 2.3.2
- `mcwwindows` 2.4.2
- `minecraft` 1.21.1
- `mixinextras` 0.5.5
- `mixinsquared` 0.1.1
- `moonlight` 1.21.1-3.7.0
- `naturalist` 2.0.5
- `naturescompass` 1.21.1-2.6.0-fabric
- `net_peanuuutz_tomlkt_tomlkt-jvm` 0.3.7
- `noisium` 2.3.0+mc1.21-1.21.1
- `org_javassist_javassist` 3.29.2-GA
- `org_jetbrains_kotlin_kotlin-reflect` 2.4.20
- `org_jetbrains_kotlin_kotlin-stdlib` 2.4.20
- `org_jetbrains_kotlin_kotlin-stdlib-jdk7` 2.4.20
- `org_jetbrains_kotlin_kotlin-stdlib-jdk8` 2.4.20
- `org_jetbrains_kotlinx_atomicfu-jvm` 0.33.0
- `org_jetbrains_kotlinx_kotlinx-coroutines-core-jvm` 1.11.0
- `org_jetbrains_kotlinx_kotlinx-coroutines-jdk8` 1.11.0
- `org_jetbrains_kotlinx_kotlinx-datetime-jvm` 0.8.0
- `org_jetbrains_kotlinx_kotlinx-io-bytestring-jvm` 0.9.1
- `org_jetbrains_kotlinx_kotlinx-io-core-jvm` 0.9.1
- `org_jetbrains_kotlinx_kotlinx-serialization-cbor-jvm` 1.11.0
- `org_jetbrains_kotlinx_kotlinx-serialization-core-jvm` 1.11.0
- `org_jetbrains_kotlinx_kotlinx-serialization-json-jvm` 1.11.0
- `org_reflections_reflections` 0.10.2
- `packet_tweaker` 0.5.6+1.21
- `placeholder-api` 2.4.1+1.21
- `playeranimator` 2.0.4+1.21.1
- `polymer-autohost` 0.9.19+1.21.1
- `polymer-blocks` 0.9.19+1.21.1
- `polymer-bundled` 0.9.19+1.21.1
- `polymer-common` 0.9.19+1.21.1
- `polymer-core` 0.9.19+1.21.1
- `polymer-resource-pack` 0.9.19+1.21.1
- `polymer-virtual-entity` 0.9.19+1.21.1
- `predicate-api` 0.5.1+1.21
- `puzzleslib` 21.1.62
- `ranged_weapon_api` 3.0.0+1.21.1
- `reborncore` 5.11.19
- `resourcefullib` 3.0.12
- `right_click_harvest` 1.0.0-1.21.x
- `runes` 1.3.2+1.21.1
- `sablecompanion` 1.6.0
- `server_translations_api` 2.3.1+1.21-pre2
- `sgui` 1.6.0+1.21
- `spark` 1.10.109
- `spectrelib` 0.17.2+1.21
- `spell_engine` 1.10.9+1.21.1
- `spell_power` 1.6.0+1.21.1
- `structory` 1.3.17
- `structure_pool_api` 1.2.1+1.21.1
- `supplementaries` 1.21.1-3.9.9
- `t_and_t` 1.13.11
- `team_reborn_energy` 4.1.0
- `techreborn` 5.11.19
- `terralith` 2.6.2
- `tiny_config` 3.1.0
- `trinkets` 3.10.0
- `universal-graves` 3.4.4+1.21
- `voicechat` 1.21.1-2.6.22
- `voicechat_api` 2.6.20
- `waystones` 21.1.46
- `wizards` 3.1.3+1.21.1
- `wover` 21.0.13
- `wover-biome` 21.0.13
- `wover-block` 21.0.13
- `wover-common` 21.0.13
- `wover-core` 21.0.13
- `wover-datagen` 21.0.13
- `wover-events` 21.0.13
- `wover-feature` 21.0.13
- `wover-generator` 21.0.13
- `wover-item` 21.0.13
- `wover-math` 21.0.13
- `wover-preset` 21.0.13
- `wover-recipe` 21.0.13
- `wover-structure` 21.0.13
- `wover-surface` 21.0.13
- `wover-tag` 21.0.13
- `wover-ui` 21.0.13
- `wunderlib` 21.0.8
- `yungsapi` 1.21.1-Fabric-5.1.9

## Jars en servidor/mods (68)

- `Chunky-Fabric-1.4.23.jar`
- `FallingTree-1.21.1-1.21.1.11.jar`
- `FarmersDelight-1.21.1-3.3.6+refabricated.jar`
- `ForgeConfigAPIPort-v21.1.6-1.21.1-Fabric.jar`
- `LeavesBeGone-v21.1.1-1.21.1-Fabric.jar`
- `NaturesCompass-1.21.1-2.6.0-fabric.jar`
- `RebornCore-5.11.19.jar`
- `Structory_26.2_v1.3.7.jar`
- `TechReborn-5.11.19.jar`
- `Terralith_1.21.x_v2.6.2.jar`
- `YungsApi-1.21.1-Fabric-5.1.9.jar`
- `YungsBetterDungeons-1.21.1-Fabric-5.1.4.jar`
- `YungsBetterMineshafts-1.21.1-Fabric-5.1.1.jar`
- `YungsBetterNetherFortresses-1.21.1-Fabric-3.1.5.jar`
- `YungsBetterStrongholds-1.21.1-Fabric-5.1.3.jar`
- `alternate-current-mc1.21-1.9.0.jar`
- `another_furniture-fabric-4.0.2.jar`
- `archers-fabric-3.1.3+1.21.1.jar`
- `armor_model_api-fabric-1.1.0+1.21.1.jar`
- `balm-fabric-1.21.1-21.0.66.jar`
- `bclib-21.0.13.jar`
- `better-end-21.0.11.jar`
- `better-nether-21.0.11.jar`
- `bettercombat-fabric-2.4.0+1.21.1.jar`
- `bundle-api-fabric-1.1.0.jar`
- `cloth-config-15.0.140-fabric.jar`
- `combat_roll-fabric-2.0.6+1.21.1.jar`
- `comforts-fabric-9.0.5+1.21.1.jar`
- `cristellib-fabric-1.21.1-3.1.7.jar`
- `emi_loot-0.7.9+1.21+fabric.jar`
- `emotecraft-for-MC1.21.1-2.4.12-fabric.jar`
- `fabric-api-0.116.17+1.21.1.jar`
- `fabric-language-kotlin-1.14.1+kotlin.2.4.20.jar`
- `ferritecore-7.0.3-fabric.jar`
- `friendsandfoes-fabric-4.0.27+mc1.21.1.jar`
- `fzzy_config-0.7.7+1.21.jar`
- `graves-3.4.4+1.21.jar`
- `krypton-0.2.8.jar`
- `ledger-1.3.5.jar`
- `levelz-2.0.11.jar`
- `libz-1.1.0.jar`
- `lithium-fabric-0.15.4+mc1.21.1.jar`
- `lithostitched-1.8.0-fabric-21.1.jar`
- `lootr-fabric-1.21.1-1.11.38.127.jar`
- `mcw-doors-1.1.5-mc1.21.1fabric.jar`
- `mcw-mcwwindows-2.4.2-mc1.21.1fabric.jar`
- `mcw-roofs-2.3.2-mc1.21.1fabric.jar`
- `moonlight-1.21.1-3.7.0-fabric.jar`
- `naturalist-2.0.5-fabric-1.21.1.jar`
- `noisium-fabric-2.3.0+mc1.21-1.21.1.jar`
- `player-animation-lib-fabric-2.0.4+1.21.1.jar`
- `polymer-bundled-0.9.19+1.21.1.jar`
- `puzzleslib-v21.1.62-mc1.21.1+fabric.jar`
- `ranged_weapon_api-fabric-3.0.0+1.21.1.jar`
- `resourcefullib-fabric-1.21-3.0.12.jar`
- `right-click-harvest-mc1.21-1.0.0-1.21.x.jar`
- `runes-fabric-1.3.2+1.21.1.jar`
- `spark-1.10.109-fabric.jar`
- `spell_engine-fabric-1.10.9+1.21.1.jar`
- `spell_power-fabric-1.6.0+1.21.1.jar`
- `structure_pool_api-fabric-1.2.1+1.21.1.jar`
- `supplementaries-1.21.1-3.9.9-fabric.jar`
- `t_and_t-fabric-neoforge-1.13.11.jar`
- `trinkets-3.10.0.jar`
- `voicechat-fabric-1.21.1-2.6.22.jar`
- `waystones-fabric-1.21.1-21.1.46.jar`
- `wizards-fabric-3.1.3+1.21.1.jar`
- `worldweaver-21.0.13.jar`

## Líneas de error únicas (120)

- `- Mod 'Forge Config API Port' (forgeconfigapiport) 21.1.6 recommends any version of modmenu, which is missing!`
- `- Mod 'Friends&Foes' (friendsandfoes) 4.0.27 recommends any version of yet_another_config_lib_v3, which is missing!`
- `- Mod 'Friends&Foes' (friendsandfoes) 4.0.27 recommends any version of modmenu, which is missing!`
- `|-- fabric-crash-report-info-v1 0.2.29+0af3f5a719`
- `[22:22:12] [main/WARN]: Error loading class: traben/entity_model_features/models/animation/EMFAnimationEntityContext (java.lang.ClassNotFoundException: traben/entity_model_features/models/animation/EMFAnimationEntityCont`
- `[22:22:12] [main/WARN]: Error loading class: com/electronwill/nightconfig/core/io/IoUtils (java.lang.ClassNotFoundException: com/electronwill/nightconfig/core/io/IoUtils)`
- `[22:22:12] [main/WARN]: Error loading class: com/simibubi/create/content/schematics/SchematicPrinter (java.lang.ClassNotFoundException: com/simibubi/create/content/schematics/SchematicPrinter)`
- `[22:22:12] [main/WARN]: Error loading class: net/minecraft/class_525 (java.lang.ClassNotFoundException: net/minecraft/class_525)`
- `[22:22:12] [main/WARN]: Error loading class: net/caffeinemc/mods/sodium/client/render/chunk/compile/pipeline/DefaultFluidRenderer (java.lang.ClassNotFoundException: net/caffeinemc/mods/sodium/client/render/chunk/compile/`
- `[22:22:12] [main/WARN]: Error loading class: com/simibubi/create/content/kinetics/base/BlockBreakingKineticBlockEntity (java.lang.ClassNotFoundException: com/simibubi/create/content/kinetics/base/BlockBreakingKineticBloc`
- `[22:22:21] [main/ERROR]: No data fixer registered for spirit_wolf`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:alligator`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:ant`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:anglerfish`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:ray`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:blobfish`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:piranha`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:bass`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:bear`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:black_bear`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:bird`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:boar`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:butterfly`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:capybara`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:caterpillar`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:catfish`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:clam`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:crab`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:deer`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:dragonfly`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:duck`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:duck_egg`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:dirt_trail`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:carried_food`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:elephant`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:firefly`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:giant_isopod`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:giraffe`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:great_white_shark`
- `[22:22:24] [main/ERROR]: No data fixer registered for naturalist:hedgehog`

## Warnings (20 total, top 15 únicos)

- `[22:22:11] [main/WARN]: Warnings were found!`
- `[22:22:11] [main/WARN]: Reference map 'balm.refmap.json' for balm.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[22:22:11] [main/WARN]: Reference map 'balm.refmap.json' for balm.fabric.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[22:22:11] [main/WARN]: Reference map 'forgeconfigapiport.common.refmap.json' for forgeconfigapiport.common.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[22:22:11] [main/WARN]: Reference map 'leavesbegone.fabric.refmap.json' for leavesbegone.fabric.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[22:22:11] [main/WARN]: Mod 'supplementaries' attempted to override option 'mixins.block.moving_block_shapes', which doesn't exist, ignoring`
- `[22:22:12] [main/WARN]: Reference map 'tiny_config-common-common-refmap.json' for tiny_config.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[22:22:12] [main/WARN]: Reference map 'waystones.refmap.json' for waystones.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[22:22:12] [main/WARN]: Reference map 'waystones.refmap.json' for waystones.fabric.mixins.json could not be read. If this is a development environment you can ignore this message`
- `[22:22:12] [main/WARN]: Error loading class: traben/entity_model_features/models/animation/EMFAnimationEntityContext (java.lang.ClassNotFoundException: traben/entity_model_features/models/animation/EMFAnimationEntityCont`
- `[22:22:12] [main/WARN]: Error loading class: com/electronwill/nightconfig/core/io/IoUtils (java.lang.ClassNotFoundException: com/electronwill/nightconfig/core/io/IoUtils)`
- `[22:22:12] [main/WARN]: Error loading class: com/simibubi/create/content/schematics/SchematicPrinter (java.lang.ClassNotFoundException: com/simibubi/create/content/schematics/SchematicPrinter)`
- `[22:22:12] [main/WARN]: Error loading class: net/minecraft/class_525 (java.lang.ClassNotFoundException: net/minecraft/class_525)`
- `[22:22:12] [main/WARN]: @Mixin target net.minecraft.class_525 was not found moonlight.mixins.json:CreateWorldScreenMixin from mod moonlight`
- `[22:22:12] [main/WARN]: Error loading class: net/caffeinemc/mods/sodium/client/render/chunk/compile/pipeline/DefaultFluidRenderer (java.lang.ClassNotFoundException: net/caffeinemc/mods/sodium/client/render/chunk/compile/`

## Cola del log (últimas 30 líneas)

```
[22:22:50] [Worker-Main-3/INFO]: Preparing spawn area: 18%
[22:22:50] [Worker-Main-3/INFO]: Preparing spawn area: 18%
[22:22:51] [Worker-Main-1/INFO]: Preparing spawn area: 51%
[22:22:51] [Worker-Main-3/INFO]: Preparing spawn area: 51%
[22:22:52] [Worker-Main-2/INFO]: Preparing spawn area: 51%
[22:22:52] [Worker-Main-3/INFO]: Preparing spawn area: 53%
[22:22:52] [Server thread/INFO]: Time elapsed: 6166 ms
[22:22:52] [Server thread/INFO]: Done (17.378s)! For help, type "help"
[22:22:52] [Server thread/WARN]: WARNING: block Block{minecraft:iron_ore} added to BlockStateRandomizer exceeds max probabiltiy of 1!
[22:22:52] [Server thread/INFO]: Added 2 Biomes
[22:22:52] [Server thread/INFO]:  - minecraft:end_midlands, subbiomes=1
[22:22:52] [Server thread/INFO]:  - minecraft:end_barrens, subbiomes=1
[22:22:53] [Server thread/INFO]: Added 2 Biomes
[22:22:53] [Server thread/INFO]:  - minecraft:end_midlands, subbiomes=1
[22:22:53] [Server thread/INFO]:  - minecraft:end_barrens, subbiomes=1
[22:22:53] [VoiceChatServerThread/INFO]: [voicechat] Voice chat server started at port 24454
[22:23:08] [Server thread/INFO]: Stopping the server
[22:23:08] [Server thread/INFO]: Stopping server
[22:23:08] [Server thread/INFO]: Saving players
[22:23:08] [Server thread/INFO]: Saving worlds
[22:23:09] [Server thread/INFO]: saving Alternate Current config
[22:23:09] [Server thread/INFO]: Saving chunks for level 'ServerLevel[world]'/minecraft:overworld
[22:23:09] [Server thread/INFO]: Saving chunks for level 'ServerLevel[world]'/minecraft:the_nether
[22:23:09] [Server thread/INFO]: Saving chunks for level 'ServerLevel[world]'/minecraft:the_end
[22:23:09] [Server thread/INFO]: ThreadedAnvilChunkStorage (world): All chunks are saved
[22:23:09] [Server thread/INFO]: ThreadedAnvilChunkStorage (DIM-1): All chunks are saved
[22:23:09] [Server thread/INFO]: ThreadedAnvilChunkStorage (DIM1): All chunks are saved
[22:23:09] [Server thread/INFO]: ThreadedAnvilChunkStorage: All dimensions are saved
[22:23:09] [Server thread/INFO]: Successfully drained database queue
[22:23:09] [Server thread/INFO]: Dispatching unloading event for config leavesbegone-server.toml
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
