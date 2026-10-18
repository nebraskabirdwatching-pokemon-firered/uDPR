# Third-party software

## Included in this repository

| What | Where | Licence |
|---|---|---|
| DOTween 1.2.335 (Demigiant) - verbatim copies of the release files | `Assets/Plugins/DOTween/` | DOTween licence: free use; verbatim copies may be redistributed with the readme and attributions (`Assets/Plugins/DOTween/readme.txt`, http://dotween.demigiant.com/license.php). Copyright (c) Daniele Giardini - Demigiant |
| crunch, Unity Technologies' fork (commit 8708900e) - the decoder header + our small `crn_levels` program and its static build | `setup/bin/crunch_src/`, `setup/bin/crn_levels.exe` | zlib licence (see the end of `crn_decomp.h`). Copyright (c) 2010-2016 Richard Geldreich, Jr. and Binomial LLC |

## Downloaded by the setup (not redistributed here)

| What | Licence |
|---|---|
| Python 3.13.12 (python.org's NuGet package) | Python Software Foundation License |
| UnityPy, numpy, Pillow, texture2ddecoder and their dependencies (`setup/requirements.lock`, from PyPI) | each package's own licence (MIT / BSD / HPND / ...) |
| AssetRipper 1.3.14 (free edition, GitHub release) | GPL-3.0 |

## Installed by you

| What | Licence |
|---|---|
| Unity 2019.4.27f1 | Unity's terms |
| Audiokinetic Wwise 2019.2.5 + its Unity Integration (not included here; the setup copies it from your own Launcher install - the repository keeps only the integration's `.meta` files, i.e. the Unity GUIDs the game's assets reference, and this project's Wwise settings) | Audiokinetic's end-user licence |

## Used while making this project (not included)

| What | Licence |
|---|---|
| Il2CppDumper | MIT |
| Ghidra | Apache-2.0 |

The game's own assets are never in this repository: the setup exports them from your dump. This project's own work is under the
MIT License (`LICENSE`).
