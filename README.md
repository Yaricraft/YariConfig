YariConfig
==========

Customised config files for Minecraft servers and tools for patching.


Installation
---------

Use "apply_patches.py -p packfolder -c configfolder -m minecraftfolder" to update your config options.

Use "update_patches.py -p packfolder -c configfolder" to create patches.

Pack folders are located in the root folder. Config folders are location inside the pack folders. A config folder named "original" must be located in the pack folder to update patches. "apply_patches.py" will call "update_patches" if no patches exist.
