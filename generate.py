#!/usr/bin/python3
#
# Copyright (C) 2021 - 2022 iDigitalFlame
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
    "rootflags=subvol=/base",
    "ssd",
    "compress=zstd",
    "noatime",
    "space_cache=v2",
    "subvolid=256",
    "subvol=/base",
]

BOOT_OPTIONS = [
    "module.sig_enforce=1",
    "quiet",
    "loglevel=2",
    "rd.systemd.show_status=auto",
    "rd.udev.log_priority=2",
    "nowatchdog",
    "nmi_watchdog=0",
    "pcie_aspm=force",
    "intel_pstate=skylake_hwp",
    "i915.modeset=1",
    "i915.enable_dc=2",
    "i915.enable_fbc=1",
    "i915.reset=3",
    "i915.enable_hangcheck=Y",
    "i915.enable_psr=1",
    "i915.psr_safest_params=N",
    "i915.enable_psr2_sel_fetch=Y",
    "i915.disable_power_well=1",
    "i915.enable_ips=1",
    "i915.fastboot=1",
    "i915.disable_display=N",
    "i915.nuclear_pageflip=Y",
    "i915.enable_guc=3",
    "i915.enable_dp_mst=Y",
    "i915.enable_dpcd_backlight=1",
    "i915.enable_gvt=N",
    "intel_iommu=on",
    "iwlwifi.led_mode=0",
    "iwlwifi.swcrypto=0",
    "iwlwifi.power_save=1",
    "iwlwifi.uapsd_disable=0",
    "iwldvm.force_cam=0",
    "snd_hda_intel.power_save=1",
    "snd_hda_intel.power_save_controller=Y",
    "atkbd.reset=1",
    "i8042.reset=1",
]

MITIGATION_DISABLE = [
    "noibrs",
    "noibpb",
    "nopti",
    "nospectre_v2",
    "nospectre_v1",
    "l1tf=off",
    "nospec_store_bypass_disable",
    "no_stf_barrier",
    "mds=off",
    "tsx=on",
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
    b.write(" ")
    if isinstance(p.resume, str) and len(p.resume) > 0:
        b.write("resume=UUID=")
        b.write(p.resume)
        b.write(" ")
    b.write("root=UUID=")
    b.write(p.root)
    b.write(" ")
    for v in ROOT_FLAGS:
        b.write(v)
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
