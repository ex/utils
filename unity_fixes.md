## 2018.4.0

    Android: Added support for supplementary Unicode characters for UnitySendMessage. (1059652)
    
    Android: Fixed Android Screen.safeArea coordinate system to be in screen space. (1148415)
    
    Android: Fixed gradle build failure with Android SDK Build-Tools 29-rc1. (1142929)
    
    Animation: Fixed float values not being animated when PPtr references were also in animated bindings. (1143168)
    
    Animation: Fixed integer values not being animated when PPtr references were also in animated bindings. (1079856)
    
    Asset Import: Fixed .meta files with a "UTF-8" BOM causing the YAML parser to freeze Unity. (1145011)
    
    Asset Import: Fixed issue with blendshape normals being recalculated when the blendshape normal import option is set to 'None'. (1140797)
    
    Audio: Fixed clip preview autoplay in the object selector. (1126745)
    
    Editor: Fixed bug that disabled the availability of having rsp files inside Packages correctly. (1138462)
    
    Editor: Fixed crash when creating Presets of AudioManager settings and then modifying AudioManager. (1141203)
    
    Editor: Fixed incorrect URL being shown in UV overlap warning message. (1124652)
    
    Editor: Fixed the preview pane in the object selector.
    
    Facebook: Fixed Facebook GameRoom sometimes faiing when target is Standalone. (1144847)
    
    GI: Fixed race condition in Enlighten data loading during additive scene loading that leads to a crash in the standalone player. (1141632)
    
    Graphics: Fixed Texture2DMSArray SRV on DX11. (1130212)
    
    IL2CPP: Added support for the MethodImplOptions.NoOptimization C# attribute. (1124061)
    
    IL2CPP: Fixed a build failure that would occur when targeting UWP w/ il2cpp while using a Managed Stripping Level of High. (1137227)
    
    IL2CPP: Fixed an intermittent crash when a managed exception occurs on a back ground thread while the process is shutting down.
    
    IL2CPP: Fixed some assemblies missing symbol files after building with the Medium or High Managed Stripping Level. (1142732)
    
    IL2CPP: Fixed the overwriting of a copy of a generic by ref argument that uses specifically crafted IL bytecode. (1140509)
    
    iOS: Fixed issue where app hangs when synchronously loading asset bundles. (1115979)
    
    iOS: Fixed player crash at decode_alpha_selectors_etc when decoding a crunched ETC texture. (1139387)
    
    iOS: Fixed plugins not being imported correctly on iOS when "Automatically Add Capabilities" is disabled. (1142626)
    
    Mobile: Fixed TargetFPS and vSyncCount has no effect on the actual FPS on Razer phones. (1078663)
    
    PS4: Fixed indirect draws occasionally causing a soft hang. (1148617)
    
    Testing: Fixed TearDown and UnityTearDown getting called on base class first. (1143077)
    
    UI Elements: Fixed script field not editable when script is missing. (1144332)
    
    Windows: Fixed maximized Standalone window going to fullscreen. (1137204)
    
    XR: Fixed a CPU core configuration issue on Oculus Quest that resulted in too many job threads spinning up. (1150332)
    
    XR: Improved performance for WIndows MR by using newer presentation APIs from Microsoft. (1148816)


## 2018.3.14

    2D: Fixed sprites referencing both the original Sprite assets and Sprite Atlas resulting in increased memory usage. (1071494, 1138745)

    Android: Adds the ability to opt-out from stopping gradle daemons upon editor exit. (1098578, 1137237)

    Android: Fixed UI mask on older PowerVR devices. (1106269, 1148371)

    Animation: Fixed crash when state has "too many" scripts attached. (1137055, 1147371)

    Animation: Fixed editor crashing on GfxDevice::ApplyBlendShape when playing animation preview. (1131617, 1134640)

    Audio: Fixed user selection not being respected for dsp buffer size in the audio settings. (1129895, 1147370)

    Editor: Fixed cloth component attached to an object disabling the Transform tools. (962773, 1141582)

    Editor: Fixed NullReferenceException when dragging Reorderable list items. (1146538, 1147489)

    Editor: Fixed the issue with GameView Scale's minimum value being dependent on the windows display scaling factor. (1099270, 1138042)

    Editor: Fixed UnityEngine.RectOffset causing GC.Collect() to be called at regular intervals causing noticeable lag spikes when using. (1130308, 1142535)

    Editor: Removed usage of DescriptionAttribute to change the display name of enum values in the inspector has been removed. (1115381, 1130990)

    Facebook: Fixed gameroom build failing with error. (1087728, 1143521)

    Graphics: Fixed Crash when calling Graphics.ExecuteCommandBuffer() if CommandBuffer.SetShadowSamplingMode() is used before it. (1102773, 1141338)

    Graphics: Fixed shadow lights and shadow casters culling when shadows are disabled. (1072624, 1116345)

    Graphics: Optimizes single-colored ambient probe updates. (1115645, 1136077)

    Linux: Fixed multiple identical webcams on not supported on Linux. (1115884, 1123760)

    Package Manager: Fix Closing the 'Reset Packages to Defaults' confirmation window still resets the Packages. (1134754, 1137061)

    Scripting: Fixed the need for a reference on an assembly. Allow empty assembly definition references. (1130125, 1136095)

    Shaders: Fixed shader include path issues with Collab projects including shaders in packages. (1115287, 1146525)

    Shaders: Introduced UNITY_SETUP_STEREO_RENDERING macro and setupStereoEyeIndex()/getStereoMatrixVP(eyeIndex) helper methods to support various stereo rendering methods in GLSL. (990291, 1149405)

    Shadows/Lights: Fixed shadow culling issue with directional light when the light direction is almost orthogonal to the normal. (1064533, 1142578)

    Terrain: Fixed SplatDatabase::CheckConsistency crash when opening a Gaia Scene. (1132798, 1142742)

    Timeline: Fixed notifications crash when instantiating GameObjects. (1129866, 1139321)

    Video: Fixed overflow of texture release command queue for Apple Metal when running headless (1127529, 1138252)

    XR: Fixed XR Settings SDK list custom options drop down collapsing when the user selects anywhere in the list. (1142001, 1147369)

    XR: Fixed XR wireframe shader not working correctly with OpenGL and DirectX. (1022184, 1136652)

    XR: Fixes grip button on knuckles controller under legacy input. (1143824, 1143826)

    XR: Updated OpenVR to 1.0.14. This fixes an issue on Linux where the player may crash if it is built for OpenVR, but SteamVR is not installed on the machine. (985931, 1117578)

#### Improvements

    XR: Update Vuforia to version 8.1.7

## 2018.3.13

    Android: Fixed an issue on Mali GPUs where font textures would occupy 4 times more memory than on other GPUs. (1132219, 1134227)

    Android: Fixed crash when AndroidJavaProxy is invoked while app is in background. (1126040, 1140959)

    Android: Fixed GPU skinning on Mali GPUs. (1131452, 1131525)

    Android: Fixed Managed Stripping Level when used with Android and mono backend. (1111490, 1137052)

    Android: Touch and mouse position's y value will be inverted in the native backend instead of managed code in the new input system.

    Animation: Fixed Animator.keepAnimatorControllerStateOnDisable not keeping default values when disabling and re-enabling a GameObject. (1076483, 1137982)

    Asset Bundles: Fixed a case where Progressive Lightmapper data was being lost when building Asset Bundles with Scriptable Build Pipeline. (1123968, 1124315)

    Asset Import: Fixed import of Blender files with Blender 2.80. (1115353, 1140790)

    Audio: Fixed AudioClips not supported in Packages. (1069085, 1139247)

    Build Pipeline: Fixed an issue with Scriptable Build Pipeline not building multiple SpriteAtlas texture pages. (1139343, 1140331)

    Editor: Fixed issue related to label control not showing full script file names in Search Execution Order editor. (1122059, 1130263)

    Editor: Restricted Editor debugging to clients on same machine. (1131839, 1140291)

    Graphics: Fixed crash when using shader with Error and enabling SRP batcher + Async loading new scenes. (1132280, 1143390)

    Graphics: Fixed tessellation shader codegen. (1120434, 1127872)

    IL2CPP: Fixed default current culture not being detected correctly on macOS and iOS instead of the invariant culture. (1133961, 1135065)

    IL2CPP: Fixed SocketException not thrown when a socket attempts to bind to an address and port that is already in use by another socket on Windows. (1133587, 1134332)

    IL2CPP: Improved the performance of Socket Poll operations on iOS. (1136660, 1139296)

    IL2CPP: Improved the performance of WaitAny on non-Windows platforms. (1111339, 1122745)

    iOS: Fixed Gamepad.startButton not working correctly. Note: on iOS startButton (or Menu button) only reports down event, there's no up event, that's why we're simulating up event right after down event to simulate a click.

    iOS: Fixed occasional crash when destroying WebCamTexture. (1090053, 1108709)

    iOS: Fixed return Pen.tilt values not being correctly returned in the new input system.

    iOS: Fixed SendMessage not working on iOS/tvOS simulator. (1138257, 1139344)

    Mobile: Fixed Application.Unload crashing on il2cpp. (1135018, 1140281)

    Mobile: Fixed rare race condition when warming up shaders. (1115274, 1134733)

    Mono: Prevented a TypeLoadException which can occur in the player at run time when the Medium or High managed stripping level is used with the Mono scripting backend. (1121958, 1135047)

    Particles: Fixed an issue where 1 particle of each mesh type would be rendered, when a system did not actually have any particles using that mesh, when using GPU Instancing. (1139308, 1140353)

    Particles: Fixed crash when resetting Particle System component via the cog wheel in the Editor. (1131320, 1140344)

    Particles: Fixed FrameDebugger corruption when using Particle Systems. (1136275, 1140341)

    Particles: Fixed particles not being removed from the system when using SetParticles with zero remaining lifetime. (1130703, 1140343)

    Particles: Fixed per-particle sorting work when using GPU Instanced particles. (1139313, 1140350)

    Particles: Fixed texture property issue with Trails texture and Sprite mode being used together. (1127679, 1140346)

    Scene Management: Fixed API and UI incorrectly reporting added/removed object overrides on disconnected Prefab instances. (1115758, 1134971)

    Scene Management: Fixed driven properties causing RectTransform to temporarily show up in Overrides dropdown after reverting or applying anything in the Comparison view. (1131854, 1135007)

    Scene Management: Fixed Prefab instances with driven properties showing Apply All and Revert All buttons in Overrides dropdown even when there are no overrides. (1131854, 1135007)

    SceneManager: Ensure nested Canvases are always treated as nested Canvases in Prefab Mode too. Root World Space Canvases can get treated as nested Canvases in Prefab Mode too due to lacking information, but this will still have fewer downsides than if nested Canvases got treated as Root Canvases. (1132706, 1139184)

    SceneManager: Fixed RectTransform properties of nested Canvas getting incorrectly modified upon entering Prefab Mode. (1132796, 1144694)

    Scripting: Improved performance when calling GameObject.AddComponent for a nested MonoBehaviour class inside a namespace. (1085304, 1118037)

    Shaders: Fixed broken shaders referencing editor only passes with UsePass. (1135888, 1139214)

    Shaders: Fixed regression on SRP subshader fallback. (1127390, 1139213)

    Shaders: Fixed shader warnings on standalone build. (1107819, 1136075)

    Timeline: Fixed errors that popup in editor when loading a timeline with exposedreferences from a instanced prefab loaded from an assetbundle. (1120186, 1129365)

## 2018.3.12

    Analytics: Fixed the time of exit from Play mode increasing several times when using newer Unity version. (1117209, 1142432)

    Android: Fixed accessibility warning when publishing to Google Play. (1094743, 1111141)

    Animation: Fixed an issue where unloading a controller in an asset bundle could lead to a crash. (1114534, 1135845)

    Asset Import: Fixed Multi-Scene Lighting is lost when building AssetBundles with Scriptable Build Pipeline. (1105486, 1105515)

    Editor: Fixed an issue where Editor notification text's last word is cut off at certain window sizes. (1098575, 1133366)

    Editor: Fixed dragging component with required component to bottom area of inspector of prefab instance. (1097140)

    Editor: Fixed Invalid AssetDatabase path warning for files that are not in unity project folder. (934940, 1137156)

    Global Illumination: Fixed baked shadow angle not being into account for indirect bounce. (1132238, 1133437)

    Graphics: Fixed crashes caused by reflection probes when entering Play mode with a camera selected. (1109892, 1130931)

    Graphics: Fixed Enabled GPU skinning for blend shapes. (1133813, 1134299)

    Graphics: Fixed normal calculation in compute skinning with one bone per vertex (1124697, 1133827)

    Graphics: In Deferred Reflections set the ambient probe SH constants before calling BeforeReflections Command Buffer to give consistency between graphics jobs enabled/disabled. (1130942, 1135303)

    Particles: Fixed newly emitted particle sizes not being updated when using Simulate and the restart flag is true. (1104199, 1123850)

    Particles: Fixed Simulate not updating sub-emitters particles when restart flag was false. (1104199, 1123850)

    Physics: Fixed a crash when destroying Colliders at the same time as raycast batches were being ran. (1123313, 1137303)

    Prefabs: SaveAsPrefabAsset[AndConnect] will now automatically do namebased replace to retain references if a prefab is being overwritten. (1139245, 1139583)

    SceneManager: Ensure nested Canvases are always treated as nested Canvases in Prefab Mode too. Root World Space Canvases can get treated as nested Canvases in Prefab Mode too due to lacking information, but this will still have fewer downsides than if nested Canvases got treated as Root Canvases. (1132706, 1139184)

    SceneManager: Fixed a Race condition in TransformAccessArray. (1132255, 1133799)

    Scripting: Fixed a crash related to calling CaptureScreenshotAsTexture at the wrong moment. (1053476, 1135737)

    Scripting: Fixed actions outside of tests not handling exceptions correctly (1120353, 1140238)

    Scripting: Fixed crash when a MonoBehaviour contains any serializable string attribute that contains malformed utf16. (1126689, 1134365)

    Scripting Upgrade: Fixed ReflectionTypeLoadException when accessing types from Accessibility assembly. (1138120, 1138740)

    Shaders: Fixed broken shaders referencing editor only passes with UsePass. (1135888, 1139214)

    Shaders: Fixed regression on SRP subshader fallback. (1127390, 1139213)

    Shaders: Fixed shader warnings on standalone build. (1107819, 1136075)

    Timeline: Fixed changes to Timeline in prefab editor not being saved. (1109279, 1133938)

    Timeline: Fixed the current position of Animation Window linked with Timelines animation being wrong when trimmed and sped up. (930909, 1133941)

    Timeline: Fixed Timeline AW link losing clip selection context (and rec mode) when selecting a different GameObject. (1123119, 1133950)

    Timeline: Fixed Timeline EaseInOut feature and shortcut for clips. (1116053, 1120473)

    Timeline: Fixed timeline in-line curves not adjusting horizontal zoom when using A & F on selected keys. (1126623, 1133957)

    Windows: Fixed some dialog buttons text being cutoff in high dpi mode. (1028835, 1137085)

## 2018.3.11

    Animation: Fixed integer values not being animated when PPtr references were also in animated bindings. (1079856, 1137005)

    Animation: Fixed preview of sprite changes on a simple animation when controller is missing. (1122246)

    Animation: Fixed tangent mode set on new keyframe when double-clicking to add a keyframe in curve editor. (1123100, 1125126)

    Animation: Fixed use of Ctrl-A/Cmd-A shortcut in the Animation Window. (1119191, 1124380)

    Asset Bundles: Fixed non-deterministic data in asset bundle when using Prebake Collision Mesh. (1116173, 1133368)

    Asset Import: Fixed a regression when switching ModelImporter Rig to Humanoid that did not enforce the T-pose in the skeleton anymore. (1103231, 1131109)

    Asset Import: Fixed Multi-Scene Lighting is lost when building AssetBundles with Scriptable Build Pipeline. (1105486, 1105515)

    Build Pipeline: Added a call to clean up high memory usage in BuildPipeline.BuildAssetBundles to avoid a crash due to out of memory. (1124274, 1129898)

    Build Pipeline: Fixed splash screen background not being included when building with nographics argument (1047042, 1122687)

    Collab: Fixed incorrect exit code for YAMLMerge when passing an empty file. (1094380, 1117860)

    Editor: Fixed an issue where Editor notification text's last word is cut off at certain window sizes. (1098575, 1133366)

    Editor: Fixed an issue where folder loses focus after renaming it in the Project Window. (1114527, 1127041)

    Editor: Fixed crash when calling virtual method on missing abstract MonoBehaviour/ScriptableObject serialized reference. (1118688, 1132155)

    Editor: Fixed dragging component with required component to bottom area of inspector of prefab instance. (1097140)

    Editor: Fixed Editor crash when illegal position is introduced to graphics engine. (1115965, 1137218)

    Editor: Fixed for MediaPlayer framework in plugin importer moved to rare group. (1124821, 1131722)

    Editor: Fixed Invalid AssetDatabase path warning for files that are not in unity project folder. (934940, 1137156)

    Editor: Fixed issue where the editor windows go blank under certain circumstances with D3D11. (1111604, 1136274)

    Editor: Fixed issue where Unity would log an error when de-serializeing older serialized data when it's intentional. (1106120, 1140228)

    Editor: Fixed issue with Assembly Definition File assemblies using "Define Constraints" getting deleted in Library/ScriptAssemblies in some cases when recompiling scripts. (1128015, 1132122)

    Editor: Fixed OS locale being used for Editor windows. (930798, 1116416)

    Editor: Fixed that the text field caret indicator cannot be placed on a specific text area in Light Explorer. (979015, 1134974)

    Global Illumination: Fixed baked shadow angle not being into account for indirect bounce. (1132238, 1133437)

    Graphics: Fixed an issue where Quad Tessellation would not work in OpenGL and Vulkan. (1131397)

    Graphics: Fixed crashes caused by reflection probes when entering Play mode with a camera selected. (1109892, 1130931)

    Graphics: Fixed Enabled GPU skinning for blend shapes. (1133813, 1134299)

    Graphics: Fixed normal calculation in compute skinning with one bone per vertex (1124697, 1133827)

    Graphics: In Deferred Reflections set the ambient probe SH constants before calling BeforeReflections Command Buffer to give consistency between graphics jobs enabled/disabled. (1130942, 1135303)

    Mobile: Fixed Application.Unload crash on Android P devices. (1120794, 1126393)

    Mobile: Fixed escape PlayerSettings.productName when composing installPath. (1113179, 1134466)

    Mobile: Fixed issue with detecting latest installed build tools version. (1094262, 1132184)

    Mobile: Fixed [Android] "Render outside safe area" setting doesn't work with Portrait or Landscape Orientation. (1125222, 1133428)

    Mobile: Fixed [Android] Visual artifacts in the skybox when using more than one camera in a scene on Adreno 330 devices. (1122358, 1133427)

    Mobile: Fixed [Android] [LTSRP] Pressing the square "recent apps" button when the app is using Vulkan API gives blurry/gloving transition. (1024522, 1133429)

    Mobile: Fixed [Android] [LTSRP] Pressing the square "recent apps" button when the app is using Vulkan API gives blurry/gloving transition. (1104092, 1133426)

    Package Manager: Fixed missing Editor folder in PackageManager directory if installed through DownloadAssistant. (1133409, 1138012)

    Particles: Fixed opening a legacy Prefab with a ParticleSystem in Prefab Mode: ParticleSystemRenderer component not being correctly hidden in the Inspector.

    Particles: Fixed opening a Particle System Prefab in Play mode breaks the Hierarchy when Stop Action is set to Destroy. (1111578, 1134976)

    Particles: Fixed Simulate not updating sub-emitters particles when restart flag was false. Fixed newly emitted particle sizes not being updated when using Simulate and the restart flag is true. (1104199, 1123850)

    Prefabs: Fixed losing selection of Prefab root in Prefab Mode after draggging script to Inspector.

    Prefabs: For broken prefabs use the root that the PrefabImporter has chosen when opening the prefab file in Prefab Mode, other dangling roots are deleted.

    Prefabs: Improved error handling when the GameObject root in PrefabMode is deleted or moved out of its prefab scene. (1123424, 1134975)

    Prefabs: SaveAsPrefabAsset[AndConnect] will now automatically do namebased replace to retain references if a prefab is being overwritten. (1139245, 1139583)

    Scene/Game View: Fixed ControlID getting out of sync for layout and repaint evengs when transitioning from 2D to 3D. (1126865, 1130151)

    SceneManager: Fixed a Race condition in TransformAccessArray. (1132255, 1133799)

    SceneManager: Fixed issue LoadSceneAsync not updating isLoaded to false for scene unloaded. (1125003, 1126524)

    Scripting Upgrade: Fixed breakpoint resolution for methods in partial classes. (1118285, 1135008)

    Scripting Upgrade: Fixed TargetParameterCountException when using Substance. (1093274, 1135337)

    Serialization: Fixed issues with the serialization when using a non-US locale. (1065595, 1127019)

    Shaders: Fixed UNITY_VERSION shader macro generation for double digit major/minor versions. (1113175, 1122980)

    UI: Fixed API inconsistency with no support of uv2 and uv3 inside the VertexHelper class. (1117237, 1132490)

    UI: Fixed scroll jitter when the scroll view component has Elastic movement type. (1129915, 1135071)

## 2018.3.10

    Android: Fixed accessibility warning when publishing to Google Play. (1094743, 1111141)

    Android: Fixed binary shaders not being cached on Android devices with Adreno GPUs. (1129357, 1132083)

    Animation: Fixed root motion evaluation for an optimized game object used in a timeline. (1115966, 1126619)

    Build Pipeline: Removed unnecessary files packaged with the Unity installer. (1124267, 1131022)

    Editor: Added icon for the particle system force field in the scene view. (1107479, 1107480)

    Editor: Fixed editor freezing when importing/reimporting script that contains unicode characters. (1111740, 1115725)

    Editor: Fixed issue with compile errors not always being cleared correctly when moving the .cs file from one .asmdef folder to another .asmdef folder. (1121925, 1122012)

    Editor: Fixed issue with compile errors not being cleared correctly in some cases when moving and removing .asmdef files. (1120835, 1122014)

    Editor: Fixed issue with EditorUtility.scriptCompilationFailed being false when .asmdef assemblies failed to compile on editor startup. (1106450, 1132162)

    Editor: Fixed issue with predefined assemblies (Assembly-CSharp.dll and friends) getting recompiled when modifying a Assembly Definition File assembly with "Auto Reference" disabled. (1124266, 1124273)

    Editor: Fixed issue with predefined assemblies (Assembly-CSharp.dll and friends) getting recompiled when modifying a Assembly Definition File assembly with "Test Assemblies" enabled. (1082290, 1124511)

    Editor: Fixed MaterialEditor inspector becoming increasingly laggy the more managed types you have. (1099071)

    Editor: Fixed null reference in Rider toolbox discovery. (1126936)

    Editor: Fixed user32.dll SetCursorPos function always moves the Cursor to the center of the screen when CursorLockMode is set to None. (1096406, 1131232)

    Graphics: Fixed crash when loading 2018.2 Compressed Mesh data in 2018.3. (1117664, 1120492)

    Graphics: Optimised cluster rendering by reducing network packet send latency. (965251, 1131274)

    IL2CPP: Allow embedded resources to be loaded from assemblies without a public key set. (1131451, 1133590)

    IL2CPP: Avoided an error when IL2CPP encounters a ref readonly property. (1131673, 1133644)

    IL2CPP: Fixed build failing if delegate has an 'in' parameter. (1128665, 1130326)

    IL2CPP: Fixed difference between macOS and Linux not properly detected when the /proc directory exists on macOS. (1126262, 1131000)

    IL2CPP: Fixed Environment.TickCount on Android 8 and later. (1108927, 1131808)

    IL2CPP: Fixed Monitor.IsEntered method not implemented properly. (1117372, 1129123)

    Linux: Fixed cursor not being confined to the game window when using CursorLockMode.Confined on Linux standalone player. (1105204, 1115744)

    OSX: Fixed issue where on macOS in the Editor sometimes floating windows would end up in front of other apps. (1115348, 1125395)

    Particles: Fixed "Internal: JobTempAlloc has allocations that are more than 4 frames old" error message (1125073, 1127765)

    Particles: Fixed crash in GenerateParticleGeometry when a Particle System with Sprites Texture Sheet and FPS Mode has Infinite Start Lifetime. (1119163, 1134987)

    Particles: Fixed particle scale on GPU Instanced particles. (1117798, 1134991)

    Particles: Fixed sprite texture sheet animation getting the wrong UV's when packed in a Sprite Atlas Variant with scale less than 1. (1115470, 1134993)

    Physics: Fixed a crash that happened when re-activating Rigidbody that had a parent Rigidbody and was reparented while being inactive. (1121720, 1134278)

    Physics: Fixed a crash when Physics.OverlapSphereNonAlloc was called wiith an infinite sphere radius. (1113683, 1132285)

    Physics: Fixed convex meshes being extra bouncy when falling on top of very thin (~contactOffset) objects. (1109477, 1136851)

    Profiler: Fixed charts no longer scaling based on highest peak. (1136260, 1136918)

    Profiler: Fixed charts not rescaling after disabling/enabling a category. (1134368, 1136924)

    Profiler: Fixed the "Others" chart category displaying behind the rest of the charts and not stacking. (1136769, 1136921)

    Shaders: Fixed potential crash if there is an infinite dependency loop between "UsePass" and "Fallback". (1068293, 1115947)

    Shaders: Fixed shader compiler emitting "//null" on GLES2 as a parameter to one of the functions emulating arithmentic operations on integers using float math. (1124159, 1132531)

    Shaders: Fixed shader compiler emitting the same struct definition each time it sees it, regardless of whether it was emitted already or not. (1099165, 1132525)

    UI: Driven properties (for example driven by UI layout) now don't get a blue margin in the Inspector and don't show up independently in the Overrides drop-down. (1115499, 1119360)

    UI Elements: Fixed graphView badges text layout on zoom. (1097162)

    UnityLinker: Prevented In correct removal of fields on a type used as a generic argument in a field used by a MonoBehaviour or ScriptableObject. This is often exposed as a crash during deserialization. (1125427, 1130995)

    Video: Fixed issue Non–360 3D video is rendering with glitches (vertical colour bands). (1098079, 1128908)

    WebGL: Fixed WebGL linker error when native plugins are used. (1129621, 1129624)

    XR: Fixed performance degradation over time for Virtual Reality applications. (1112790, 1130392)

#### Improvements

    Scripting: Improved assembly file definitions slowing down the editor in general.

## 2018.3.9

    2D: Fixed SVG sprites are constanly re-imported when added into prefabs. (1125015)

    Android: Fixed binary shaders not being cached on Android devices with Adreno GPUs. (1129357)

    Animation: Fixed an issue where AnimationPlayable.iKOnFeet didn't propagate properly when multiple AnimationOutputs are connected to the same Animator. (1115086)

    Animation: Fixed an issue where trying to add a key to a curve would crash. (1101703)

    Animation: Fixed crash when changing Animator.playbackTime with a controller using synced layers. (1109439)

    Editor: Added icon for the particle system force field in the scene view. (1107479)

    Editor: Fixed certain shortcuts not executing when in paused play mode. (1129380)

    Editor: Fixed editor freezing when importing/reimporting script that contains unicode characters. (1111740)

    Editor: Fixed issue with compile errors not always being cleared correctly when moving the .cs file from one .asmdef folder to another .asmdef folder. (1121925)

    Editor: Fixed issue with compile errors not being cleared correctly in some cases when moving and removing .asmdef files. (1120835)

    Editor: Fixed issue with EditorUtility.scriptCompilationFailed being false when .asmdef assemblies failed to compile on editor startup. (1106450)

    Editor: Fixed issue with predefined assemblies (Assembly-CSharp.dll and friends) getting recompiled when modifying a Assembly Definition File assembly with "Auto Reference" disabled. (1124266)

    Editor: Fixed issue with predefined assemblies (Assembly-CSharp.dll and friends) getting recompiled when modifying a Assembly Definition File assembly with "Test Assemblies" enabled. (1082290)

    Editor: Fixed MaterialEditor inspector becoming increasingly laggy the more managed types you have. (1099071)

    Editor: Fixed the issue with the order of items in the Edit Menu on OSX. (1110914)

    Editor: Fixed user32.dll SetCursorPos function always moves the Cursor to the center of the screen when CursorLockMode is set to None. (1096406)

    GI: Fixed crash on application exit when GPU lightmapper openCL context is lost.

    Graphics: Fixed Assets with serializedVersion: 6 meshes are not rendered. (1079076, 1130112)

    Graphics: Fixed crash when loading 2018.2 Compressed Mesh data in 2018.3. (1120492)

    Graphics: Fixed particles are not rendered in XBOX One from VSE with HDRP. (1126333)

    Graphics: Fixed Set rendertarget before setting viewport in GrabIntoRenderTexture. (1126248)

    Graphics: Optimised cluster rendering by reducing network packet send latency. (965251, 1131274)

    iOS: Added 'Automatically add capabilities' checkbox to player settings. (1131078)

    iOS: Fixed Crash when using R8 and RG16 Metal texture formats.

    OSX: Fixed issue where on macOS in the Editor sometimes floating windows would end up in front of other apps. (1115348)

    Package Manager: Fixed package manager for different CultureInfos. (1117469)

    Particles: Fixed "Internal: JobTempAlloc has allocations that are more than 4 frames old" error message (1125073)

    Particles: Fixed crash in GenerateParticleGeometry when a Particle System with Sprites Texture Sheet and FPS Mode has Infinite Start Lifetime. (1119163)

    Particles: Fixed particle scale on GPU Instanced particles. (1117798)

    Particles: Fixed sprite texture sheet animatio getting the wrong UV's when packed in a Sprite Atlas Variant with scale less than 1. (1115470)

    Physics: Disallow zero bounds being passed to Physics.RebuildBroadphaseRegions. (1051407)

    Physics: Fixed a crash that happened when re-activating Rigidbody that had a parent Rigidbody and was reparented while being inactive. (1121720)

    Physics: Fixed a crash when Physics.OverlapSphereNonAlloc was called wiith an infinite sphere radius. (1113683)

    Physics: Fixed a GJK issue that returned incorrect normals when a primitive's centre was so close to the surface of a convex (affected Physics.ComputePenetration). (1115449)

    Physics: Fixed convex meshes being extra bouncy when falling on top of very thin (~contactOffset) objects. (1109477)

    Physics: Fixed MeshCollider not following the changes to a mesh after it produced an empty geometry. (996035)

    Physics: Fixed the force limits of ConfigurableJoint's drives being expressed in incorrect units actually. (1116513)

    Physics: Fixed the reset editor button actually not resetting the Collider's trigger property. (1093243)

    Profiler: Fixed UI module chart not showing data. (1110630)

    Scripting Upgrade: Fixed issue where an async Task throwing an exception would log errors to console repeatedly. (1126231)

    Scripting Upgrade: Fixed issue where an async Task throwing an exception would stop all other Tasks. (1130295)

    Shaders: Fixed shader compiler emitting "//null" on GLES2 as a parameter to one of the functions emulating arithmentic operations on integers using float math. (1124159)

    Shaders: Fixed shader compiler emitting the same struct definition each time it sees it, regardless of whether it was emitted already or not. (1099165)

    Shaders: Unity could crash if infinite dependency loop between "UsePass" and "Fallback". (1068293, 1115947)

    Terrain: Fixed normalization issue when blending 5 or more materials on Terrain. (1129582)

    UI: Driven properties (for example driven by UI layout) now don't get a blue margin in the Inspector and don't show up independently in the Overrides drop-down. (1115499)

    UI: Fixed issue where canvas elements positions are set to NAN when the camera orthographic size is set to 0 and do not reset to valid positions when the orthographic size is changed again. (1125401)

    Vulkan: Vulkan: Fixed crash if the scene does not contain any cameras. (1067621)

    WebGL: FIxed audio not working Safari after Apple added auto-play restrictions (requires clicking on content to enable audio). (1089060)

    XR: Fixed performance degradation over time for Virtual Reality applications. (1130392)

#### Improvements

    Editor: Add option to Plugin Inspector to disable validation of managed assembly references. Disables the check that emits "Assembly '' will not be loaded due to errors: Unable to resolve reference ''. Is the assembly missing or incompatible with the current platform?". (1126737)

    XR: Enabled depth buffer sharing on Windows MR by default.

## 2018.3.8

    2D: Fixed case of Editor crashing on WorldContactFilter2D::ShouldCollide when trying to destroy Tilemap. (1126791)

    2D: Fixed case of Tile Animation showing a wrong Sprite when Tilemap is deactivated and reactivated. (1126772)

    2D: Fixed issue where Tilemap Collider Physics Shape/s were not updating when a single Tile was removed. (1126789)

    2D: Fixed to clean up Preview Tiles when painting on a Tilemap when an asset is saved. (1126776)

    2D: Fixed NullReferenceException when painting with a Tile Palette without a valid Tilemap component. (1120310, 1126781)

    2D: We now use Grid Cell Layout instead of Tile Orientation for doing Grid Cell picking when painting on a Tilemap. (1126779)

    Android: Fixed null exception on GC when Java class is not found. (1128659)

    Android: UnityWebRequest: Relaxed format requirements for jar:file uris. (1117525, 1128887)

    Asset Import: Fixed crash when reading a meta file with a "Byte Order Mark". (1128853)

    Editor: Fixed Instability in IConnectionStateInternal_HasAtLeastTheDefaultAmountOfAvailableConnections . (1103431)

    GI: Fixed an issue were newly loaded scenes with bounce count 3 would not bake any indirect light. (1129335)

    Graphics: Fixed for [ASAN] Memory use after free in GpuProgramMetal::ApplyGpuProgram. (1127838)

    Graphics: Fixed issue where "GetGfxDevice() should only be called from main thread" errors are thrown and crashes in Play Mode later on. (1124135)

    Graphics: Fixed memory leak in batchmode when rendering on desktop platforms . (1093649, 1102280)

    Graphics: Vulkan: Fixed a crash when draw call was made without an active GPU program. (1126841)

    IL2CPP: Fixed correct flow control code not generated for try/catch/finally handling with async methods in C#. (1122868)

    IL2CPP: Fixed step-into debugging for some generic methods. (1124177)

    IL2CPP: Improved the performance of WaitOne, WaitAny, and WaitAll on Windows platforms. (1111339)

    IMGUI: Maximizing the player in the windowed mode sets it to Maximized Window mode. (1085673, 1127910)

    iOS: Fixed background audio stopping when startin an Unity app on iOS. (1115948)

    iOS: Fixed issue where an App won't be automatically deployed to Device when building project via Build and Run. (1114541)

    Linux: Fixed editor UI breaking with Screen.SetResolution is called. (1057513, 1128667)

    Mobile: Fixed il2cpp player build when engine stripping is enable and AssetImporter log is not empty. (1115957)

    Multiplayer: Fixed memory leak in TLS connections, affecting Windows/Linux/Mac/UWP. (1121523)

    OSX: Fixed an issue where older Macs could incorrectly report that they support GPU instancing. (1126530)

    OSX: Fixed the fullscreen menu item in the standalone player. (1120105)

    Package Manager: Fixed incorrect build settings on Project Templates in packages. (1114141)

    Prefabs: Fixed crashes when instantiating prefab with certain user scripts. (1113205, 1125019)

    Prefabs: Fixed drag and drop not unpacking the Prefab instance under some circumstances. (1117374)

    Prefabs: Fixed object IDs changing when saving a prefab after building a player. (1106345)

    Profiler: Fixed an issue where chart data would be inconsistent from hierarchy data. (1080435)

    Scripting: Fixed MissingMethodException when calling bindings methods in VRModule on XBox One. (1109347)

    Scripting: Removed allocation in every frame from ScriptableRuntimeReflectionSystemWrapper.TickRealtimeProbes. (1097039)

    Scripting Upgrade: Fixed an issue where some C# class libaries would fail to load. (1116475)

    Scripting Upgrade: Fixed ReflectionTypeLoadException when getting types from assembly. (1127900)

    Services: Fixed crash when an unhandled exception occurs on a background thread with Cloud Diagnostics enabled. (1114571, 1122097)

    Shaders: Fixed out-of-memory when trying to compile shader that uses self-referencing macro. (1119490)

    Timeline: Fixed issue where a timeline would not play on AOT platforms using Mono and .NET 3.5 (1129165)

    UI: Fixed issue with CanvasGroup.Alpha not affecting nested Canvas's UI elements. (1127613)

    Unity Test Runner: Fixed Exception not handled properly in PlayTests when a custom Enumerator is used as a Coroutine and throws an Exception. (1120096)

    Universal Windows Platform: Fixed incorrect mouse position for NewInput. (1091493)

    Universal Windows Platform: Fixed rapid triggering of OnClick() events in UI when multiple Xbox controllers connected. (1099111)

    Universal Windows Platform: Prevented an error from the reference rewriter about the missing method 'ConfigurationElement::get_Item' when the EntityFramework.dll assembly is used. (1124092)

    Video: Fixed a crash on quit, and on end of playmode, when using a VideoPlayer in a prefab. (1126578)

    Video: Fixed Android Video doesn't start to play in the application when Android OS is 4.1 or 4.2. (1124979)

    Web: UnityWebRequest: Better document SetRequestHeader regarding cookie. (1128889)

    Windows: Fixed Multidisplay always reverting to native resolution on primary display. (1040726)

## 2018.3.7

    Fixed security vulnerability. (CVE-2019-9197).

    Analytics: Fixed issue: usage statistics will no longer be sent when editor analytics is disabled.

    2D: Fixed "Invalid SortingGroup index set in Renderer" warning from occurring after removing Sorting Group component on an object with nested Sorting Groups. (1106381)

    2D: Fixed Sprites randomly flipping when moving/zooming camera (1117333)

    Android: Fixed hang at exit if submitting AndroidJavaProxy/Runnable to UI thread. (1113139, 1124900)

    Android: Fixed an out of memory issue happening on Adreno devices on GLES. (1111097)

    Asset Bundles: Fixed error when loading an object from an asset bundle on the first frame of a scene load operation under certain conditions. (1094045)

    Build Pipeline: Removed unnecessary files from mac standalone build, reducing the size by about 500kb. (1111649)

    Editor: Fixed error in ScriptExecutionOrder Editor when exiting play mode. (1119209)

    Editor: Fixed issue where EditorPrefs wouldn't be saved on editor close when using Rider as an external script editor (1110859)

    Editor: Fixed issue where if the user cancels a non scripts only build it will cache an incomplete form of the player data cache which on a subsequent scripts only build will cause the build to fail and then crash the editor. Canceled builds will now clean up the cache and an additional check was added to VerifyBuildSetup to fail the build properly if there is no cached player data. (1114580, 1123801)

    Graphics: OpenGL & Vulkan: Fixed shader code generation for InterlockedMax(). (1124926)

    Graphics: Vulkan: "Attempting to draw with missing bindings" is now a warning instead of an error. (1100647)

    Graphics: Vulkan: Fixed restoring a fullscreen window from minimized state on Windows (1090059)

    Graphics: Vulkan: Improved async readback performance. (1123745)

    iOS: Stretching image across the entire screen when resolution is set to one that does not match the aspect ratio of the screen. (1077959, 1103189)

    Mobile: Fixed Screen.width and Screen.height don't update at the same time as Screen.orientation (1013176, 1094317)

    Mono: Fixed "DllNotFoundException: MonoPosixHelper" exception being thrown when MonoPosixHelper APIs are used (1045644, 1122898)

    Prefabs: Fixed crash when passing invalid paths to PrefabUtility.LoadPrefabContents. (1116603)

    Prefabs: Fixed crash when entering play mode while having a locked inspector on a GameObject with AudioSource. (1114376)

    Prefabs: Updated RectTransforms to correctly position and parent on creation. (1124325)

    Shaders: Fixed a missing interpolator in GL shader outputs. (1122033)

    Terrain: Fixed issue where control key and mouse wheel does not adjust the Stamp Height value for the Stamp Terrain brush (1108352)

    UI: UI: PhysicsRaycaster and Physics2DRaycaster now support multiple-displays. (1027701)

## 2018.3.6

    2D: Fixed crash on when passing array of nulls to SpriteAtlas.Add. (1089125, 1120906)

    Animation: Fixed a crash when parenting an GameObject during an AnimationEvent. (1115423)

    Asset Pipeline: Optional parameter added to SceneManager.UnloadScene function allowing to unload assets embedded in a scene without calling UnloadUnusedAssets. (998958, 1111167)

    Build Pipeline: Fixed rare data corruption when building asset bundles with LZMA compression. (1118331)

    DX12: Fixed a crash when switching to exclusive fullscreen.

    Editor: Fixed an issue where text flickers when displaying a button or label using the IMGUI that has a long text with wordwrap enabled. (1106201)

    Editor: Fixed crash and validation errors when opening editor windows. (1085277)

    Graphics: Disabled GPU skinning in the Editor when Graphics Emulation is enabled. (1107282)

    Graphics: Fixed an issue where Light Probe Proxy Volumes did not function correctly with Vulkan as the graphics API. (988476)

    Graphics: Improved terrain painting that produces quantization when using OpenGL API. (1114680)

    Graphics: Vulkan: Various stability, performance and correctness fixes.

    Graphics: Vulkan: Various stability, performance and correctness fixes.

    Graphics: [ShaderGraph] Fixed Transparent preview not clearing framebuffer. (1068062)

    IL2CPP: Add support for marshaling fields which are arrays of structs which in turn have arrays as fields. (1106047)

    IL2CPP: Added protocol support for IPv6 on Windows. (1099133)

    IL2CPP: Correctly indicate that IPv6 is not supported on non-IPv6 platforms. (1108823)

    IL2CPP: Emit proper C++ code when type names include characters that are not valid for C++ source code. (1108435)

    IL2CPP: Fixed a crash when using the Environment.MachineName property on some machines when targeting UWP and make it return results consistent with the Standalone Player. (1093953)

    IL2CPP: Fixed an intermittent crash in the native linker on Android. (1108960)

    IL2CPP: Fixed InvalidCastException that can sometimes happen when passing managed object that derives from a native Windows Runtime class to native code. For instance, this happens when deriving from Windows.UI.Xaml.Control.ContentDialog and trying to show it. (1104540)

    IL2CPP: Generate proper C++ code for an out parameter used as SizeParamIndex. (1115412)

    IL2CPP: Handle null explicitly casted to an array and indexed. (1115145)

    IL2CPP: Loaded field addresses via unsigned native integer types properly. (1104370)

    IL2CPP: Prevent a compilation error in generated C++ code when the ldtoken opcode is used in some cases. (1108435)

    IL2CPP: Prevent an compilation error in generated C++ code when an enum field is marshaled. (1104889)

    IL2CPP: Prevent an exception during IL2CPP code conversion that can happen with Trace statements in some cases. (1120880)

    IL2CPP: Prevented a crash at runtime with the .NET 4.x equivalent scripting runtime that can occcur when an enum is nested in a generic type. (1113091)

    IL2CPP: Properly generate code using the in modifier for parameters on abstract methods in a generic type. (1103142)

    Package Manager: Fixed moving files in the editor project view (drag and drop) not working in local packages. (1114391, 1117976)

    Particles: Fixed erroneous Particle System error message: "Sub-emitters must be children of the system that spawns them". (949522, 1089804)

    Particles: Fixed Frame Debugger failing to show draw call information for Particle Systems. (1107382)

    Particles: Fixed incorrect curve evaluation when using the Limit Velocity over Lifetime module with a micture of optimized and non-optimzied curves. (1096701)

    Particles: Fixed particle bounds when using Sprites in the Texture Sheet Animation Module. (1107722)

    Particles: Fixed particle trails could being culled incorrectly when using the World Space trails option. (1089679)

    Particles: Fixed regression bug where offscreen Particle Systems failed to play. (1114729)

    Particles: Fixed scaling regression bugs with Particle Systems. (1112937, 1116160)

    Particles: Fixed Velocity Module Speed Modfiier not applied to the initial simulation step of newly spawned particles. (1111134)

    Particles: Update particle bounce light immediately when the multiplier is changed on the Light. (1102543)

    Physics: Ensure that ContactPoint2D and Collision2D types do not get stripped causing a crash. (1121995)

    Prefabs: Fixed references to Prefabs from scene getting lost if prefab is modified. (1116476)

    Prefabs: Updated Undo to return Prefab instances with missing assets to previous state correctly. (1056446, 1120322)

    Scripting Upgrade: Fixed crash in ScriptUpdater.exe when code contains qualified references to methods of type that were statically imported (#using static). (1081267)

    Shaders: Fixed incorrect shader code generation with tessellation shaders when using the Vulkan API. (1092160)

    Universal Windows Platform: Fixed IL2CPP crashing when using certain new types (like Windows.Foundation.GuidHelper.Equals) in Windows SDK 17763 or newer.

    Universal Windows Platform: Fixed memory leaks on .NET backend when calling Mesh.SetVertices(), Mesh.SetUVs(), Mesh.SetTriangles() methods. (1042218)

    Windows: Fixed setting refresh rate in exclusive fullscreen mode having no effect on D3D11 and D3D12. (975924)

    XR: XR devices in new input system package are now all Y-up is away from the user. (1091918)

## 2018.3.5

    AI: Fixed issue with NavMeshAgent getting stuck wobbling when an obstacle carves a hole in the NavMesh near its path. (1039002)

    Android: Fixed "Gradle prewarm failed" error not giving any meaningful information. (1114985, 1115479)

    Android: Fixed issue where Unity logo in splash screen was shown as a black rectangle on Android 4.4 devices. (1104471)

    Android: Fixed problem with opening keyboard on Android 9. (1102448, 1115490)

    Android: Fixed redundant render pass switches when using Vulkan.

    Android: Fixed sporadic crash during startup in development builds. (1116047)

    Android: Fixed system resolution on Android. (1090830, 1118761)

    Asset Import: Fixed issue where asset database incorrectly assumes it has imported assets when switching target platform with a clean library folder. (1123035)

    Editor: Fixed AdvancedDropdown not selecting the first element of the list when searching. (1119474)

    Editor: Fixed an issue where compilation would not start correctly and would emit "Assembly for Assembly Definition File '.asmdef' will not be compiled, because it has no scripts associated with it." when updating both C# source files and Assembly Definition Files (asmdef). (1115384)

    Editor: Fixed editor throwing errors when connected to an android device with usb debugging disabled. (1090834)

    Editor: Fixed empty context menu being popped. (1118300)

    Editor: Fixed first option isn't selected by default when using "Add Component". (1116399)

    Editor: Fixed issue with MonoBehaviours in assemblies (.dlls) not loading correctly in scenes from AssetBundles when loading the assembly through reflection with Assembly.Load or similar. (1082571)

    Editor: Fixed Unwrapping.GenerateSecondaryUVSet not working with meshes having 32bit indices . (1096058, 1103502)

    Graphics: Fixed "CPU fence is invalid or very old!" error message. (1122971)

    Graphics: Fixed async readback when using Vulkan. (1018472)

    IL2CPP: Fixed crash during managed code stripping when user has Turkish language. May have happened for other non-english languages as well. (1083122)

    IL2CPP: Fixed the throwing of exceptions in attribute constructors. (1101440)

    Package Manager: Disabled delete and rename menu items for all package root folders in the Project window. (1101384)

    Particles: Fixed particle systems causing graphical glitches and error messages. (1099125, 1116662)

    Physics: Fixed incorrect collision detection between CapsuleCollider2D and CircleCollider2D when the capsule is orientated towards the center of the circle. (1119018)

    Physics: Fixed multithreaded joint constraints not working when there are no contacts in the contact island. (1109272)

    ps4: Fixed crash duing dynamicaly changing meshes. (1117853)

    ps4: Fixed crash when viewing information on large shaders (like ones from ShaderGraph). (1110680)

    ps4: Fixed functionality in .net 4 relating the network features.

    ps4: Fixed regression when running native graphics jobs. (1117621)

    Scripting Upgrade: Fixed crash when Debug.Log is called in finally block. (1093869)

    Scripting Upgrade: Fixed NotImplementedException when calling XmlSerializationReader. (1106236)

    Scripting Upgrade: Fixed TimeZoneNotFoundException on some Windows machines. (1076679)

    Timeline: Added Apply Foot IK option to animation clips to allow users to turn off Foot IK on humanoid animation clips in Timeline. (1115652)

    Timeline: Fixed animated object in timeline popping for a single frame when switching Timelines (1109118)

    Timeline: Fixed Animation Clips with Root Curves not properly putting Transforms into Preview Mode (1116007)

    Timeline: Fixed Scene position getting updated with Timeline in Preview Mode when changing offsets (1116297)

    VR: Improved XR Trace, now logs at Errors, Asserts, Warnings, Log Messages, Exceptions and Debug level. (1115640)

    VR: Performance fixes for viewport scaling for performance on tiled renderers. (1014390, 1105278)

    XR: Fixed a hang on iOS when using the ARKit XR Plugin package. (1068999)

    XR: Fixed Oculus Quest controllers not working with native input. (1118025)
