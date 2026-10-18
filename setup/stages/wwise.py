#!/usr/bin/env python3
"""Stage wwise: install the Wwise Unity Integration 2019.2.5.1831 files from the user's own Launcher integration (author D-S2:
Audiokinetic's files are not shipped with this repository).

Source = the Unity project the Audiokinetic Launcher integrated Wwise 2019.2.5 into (config key `wwise`). Copied into Assets/Wwise:
every file this repository has a .meta for (the .meta files are OURS and are never replaced: the game's assets reference the Wwise
components by these GUIDs, while the Launcher's install gets random new ones). Kept as ours: ScriptableObjects/*.asset (the project's
Wwise settings), LauncherInfo.json. Skipped: files we have no .meta for (plugin .pdb files, the optional Extensions folder), the
editor cache Editor/ProjectData. Then the shipped game's two public methods: AkInitializer.LateUpdate and AkGameObj.SetPosition
(2019.2.5 made them private; shipped game code calls them).

  python -I setup/stages/wwise.py [--source <Unity project with Assets/Wwise>]
"""
import argparse
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib"))
import paths  # noqa: E402

OURS = ("ScriptableObjects/", "LauncherInfo.json", "InstallConfig.json", "Editor/ProjectData/")
PATCHES = [("Deployment/Components/AkInitializer.cs", "private void LateUpdate()", "public void LateUpdate()"),
           ("Deployment/Components/AkGameObj.cs", "private void SetPosition()", "public void SetPosition()")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=paths.CFG.get("wwise"))
    a = ap.parse_args()
    if not a.source:
        sys.exit("no Wwise source project configured (setup.py --wwise <project the Launcher integrated Wwise into>)")
    src = os.path.join(a.source, "Assets", "Wwise")
    dst = os.path.join(paths.ASSETS, "Wwise")
    ver = open(os.path.join(src, "Version.txt"), encoding="utf-8", errors="replace").read()
    if "2019.2.5 Build 7349" not in ver:
        sys.exit("the source integration is not Wwise 2019.2.5 Build 7349")
    copied = same = skipped = 0
    skipped_list = []
    for dp, dn, fn in os.walk(src):
        for f in fn:
            if f.endswith(".meta"):
                continue
            rel = os.path.relpath(os.path.join(dp, f), src).replace("\\", "/")
            if rel.startswith(OURS):
                continue
            if not os.path.exists(os.path.join(dst, rel + ".meta")):
                skipped += 1
                skipped_list.append(rel)
                continue
            s, d = os.path.join(dp, f), os.path.join(dst, rel)
            if os.path.exists(d) and open(s, "rb").read() == open(d, "rb").read():
                same += 1
                continue
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copyfile(s, d)
            copied += 1
    print("copied %d, already identical %d, skipped (no .meta of ours) %d: %s" % (
        copied, same, skipped, ", ".join(sorted(set(os.path.splitext(x)[1] or x for x in skipped_list)))))
    # every Wwise file / folder we have a .meta for must now exist. Folders the integration fills only at edit time
    # (Editor/ProjectData) are created empty; InstallConfig.json is the Launcher's own record, empty in this project.
    missing = []
    for dp, dn, fn in os.walk(dst):
        for f in fn:
            if f.endswith(".meta"):
                target = os.path.join(dp, f[:-5])
                if os.path.exists(target):
                    continue
                rel = os.path.relpath(target, dst).replace("\\", "/")
                if "folderAsset: yes" in open(os.path.join(dp, f), encoding="utf-8", errors="replace").read():
                    os.makedirs(target, exist_ok=True)
                elif rel == "InstallConfig.json":
                    open(target, "wb").close()
                else:
                    missing.append(rel)
    if missing:
        for m in missing[:20]:
            print("  missing: " + m)
        sys.exit("%d Wwise files are missing after the copy - is the Launcher integration complete (Windows + macOS)?"
                 % len(missing))
    for rel, old, new in PATCHES:
        p = os.path.join(dst, rel)
        text = open(p, encoding="utf-8-sig", newline="").read()
        bom = open(p, "rb").read(3) == b"\xef\xbb\xbf"
        if text.count(new) == 1 and old not in text:
            print("patch already applied: %s" % rel)
            continue
        if text.count(old) != 1:
            sys.exit("cannot patch %s: '%s' found %d times" % (rel, old, text.count(old)))
        with open(p, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
            f.write(text.replace(old, new))
        print("patched %s: %s" % (rel, new))
    print("wwise OK")


if __name__ == "__main__":
    main()
