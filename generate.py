#!/usr/bin/python3
################################
### iDigitalFlame  2016-2024 ###
#                              #
#            -/`               #
#            -yy-   :/`        #
#         ./-shho`:so`         #
#    .:- /syhhhh//hhs` `-`     #
#   :ys-:shhhhhhshhhh.:o- `    #
#   /yhsoshhhhhhhhhhhyho`:/.   #
#   `:yhyshhhhhhhhhhhhhh+hd:   #
#     :yssyhhhhhyhhhhhhhhdd:   #
#    .:.oyshhhyyyhhhhhhddd:    #
#    :o+hhhhhyssyhhdddmmd-     #
#     .+yhhhhyssshdmmddo.      #
#       `///yyysshd++`         #
#                              #
########## SPACEPORT ###########
### Spaceport + SMD
## Boot Configuration Generator
#
# Copyright (C) 2016 - 2024 iDigitalFlame
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from sys import stderr
from io import StringIO
from argparse import ArgumentParser

ROOT_FLAGS = [
    "ro",
    "nodev",
    "noatime",
    "compress=zstd",
    "ssd",
    "discard=async",
    "space_cache=v2",
    "subvolid=256",
    "subvol=/base",
]

BOOT_OPTIONS = [
    "module.sig_enforce=1",
    "quiet",
    "loglevel=2",
    "audit=0",
    "rd.systemd.show_status=auto",
    "rd.udev.log_priority=2",
    "nowatchdog",
    "nmi_watchdog=0",
    "intel_pstate=skylake_hwp",
    "i915.disable_display=0",
    "i915.reset=3",
    "i915.modeset=1",
    "i915.memtest=0",
    "i915.fastboot=1",
    "i915.enable_dc=4",
    "i915.enable_dpt=1",
    "i915.enable_fbc=1",
    "i915.enable_gvt=1",
    "i915.enable_guc=3",
    "i915.enable_psr=2",
    "i915.enable_ips=1",
    "i915.enable_sagv=1",
    "i915.enable_dp_mst=1",
    "i915.enable_hangcheck=1",
    "i915.enable_dpcd_backlight=1",
    "i915.enable_psr2_sel_fetch=1",
    "i915.nuclear_pageflip=1",
    "i915.psr_safest_params=0",
    "i915.disable_power_well=1",
    "i915.verbose_state_checks=0",
    "i915.force_reset_modeset_test=0",
    "intel_iommu=on",
    "iwlmvm.power_scheme=3",
    "iwlwifi.led_mode=0",
    "iwlwifi.swcrypto=0",
    "iwlwifi.power_save=1",
    "iwlwifi.uapsd_disable=0",
    "snd_usb_audio.enable=1",
    "snd_hda_intel.enable=1",
    "snd_hda_intel.power_save=1",
    "snd_hda_intel.power_save_controller=1",
    "snd_hda_intel.index=-1",
]

MITIGATION_DISABLE = [
    "nospectre_v1",
    "l1tf=off",
    "mds=off",
    "tsx_async_abort=off",
    "mitigations=off",
]

if __name__ == "__main__":
    args = ArgumentParser(description="Spaceboot Boot File Generator")
    args.add_argument(
        "--name",
        action="store",
        dest="name",
        type=str,
        help="Boot Loader Name",
        default="Spaceport",
        required=False,
    )
    args.add_argument(
        "--kernel",
        action="store",
        dest="kernel",
        type=str,
        help="Kernel Path",
        default="vmlinuz-linux",
        required=False,
    )
    args.add_argument(
        "--init",
        action="store",
        dest="ramdisk",
        type=str,
        help="Ramdisk Path",
        default="initramfs-linux.img",
        required=False,
    )
    args.add_argument(
        "--ucode",
        action="store_true",
        help="Include Intel UCode",
    )
    args.add_argument(
        "--spectre",
        action="store_true",
        help="Don't disable SpectreV2 mitigation",
    )
    args.add_argument(
        "--lvm",
        action="store",
        dest="lvm",
        type=str,
        help="LVM UUID",
        required=True,
    )
    args.add_argument(
        "--group",
        action="store",
        dest="group",
        type=str,
        help="LVM Group Name",
        required=True,
    )
    args.add_argument(
        "--root",
        action="store",
        dest="root",
        type=str,
        help="Root UUID",
        required=True,
    )
    args.add_argument(
        "--resume",
        action="store",
        dest="resume",
        type=str,
        help="Resume UUID",
        required=False,
    )

    p = args.parse_args()
    if p is None:
        print("Invalid arguments!", file=stderr)
        exit(1)

    b = StringIO()
    b.write("title   ")
    b.write(p.name)
    b.write("\nlinux   /")
    b.write(p.kernel)
    b.write("\n")
    if p.ucode:
        b.write("initrd  /intel-ucode.img\n")
    b.write("initrd  /")
    b.write(p.ramdisk)
    b.write("\noptions luks.name=")
    b.write(p.lvm)
    b.write("=")
    b.write(p.group)
    b.write(" luks.options=discard ")
    if isinstance(p.resume, str) and len(p.resume) > 0:
        b.write("resume=UUID=")
        b.write(p.resume)
        b.write(" ")
    b.write("root=UUID=")
    b.write(p.root)
    b.write(" ")
    if len(ROOT_FLAGS) > 0:
        b.write("rootflags=")
        b.write(",".join(ROOT_FLAGS))
    b.write(" ")
    for v in BOOT_OPTIONS:
        b.write(v)
        b.write(" ")
    if not p.spectre:
        for v in MITIGATION_DISABLE:
            b.write(v)
            b.write(" ")
    print(b.getvalue().strip())
    del b
