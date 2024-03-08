# The Spaceport Project

## ARCHIVED

I've moved to unified kernel images. Check the [spaceport](https://github.com/iDigitalFlame/Spaceport) to have a look!
For more info on unified kernel images, check this [ArchWiki Entry](https://wiki.archlinux.org/title/Unified_kernel_image).

### Bootloader Entries

Systemd-boot Bootloader entries
For systemd-boot (The bestest boot manager!)

Replaced all the config files with a new generator script file.
This can be used to generate the files from a simple config.

```[text]
Located In: /boot/loader/entries/
```

Enables all the good powersaving features and has LTS fallback incase of kernel issues. (I'm paranoid ok?)
