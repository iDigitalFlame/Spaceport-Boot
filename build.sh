#!/usr/bin/bash
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

UUID_LVM="$1"
UUID_ROOT="$2"
UUID_RESUME="$3"

python3 generate.py \
  --name "Spaceport" \
  --kernel "vmlinuz-linux-zen" \
  --init "initramfs-linux-zen.img" \
  --ucode \
  --lvm $UUID_LVM \
  --group "spaceport" \
  --root $UUID_ROOT \
  --resume $UUID_RESUME > ./spaceport.conf

python3 generate.py \
  --name "Spaceport (LTS)" \
  --kernel "vmlinuz-linux-lts" \
  --init "initramfs-linux-lts.img" \
  --ucode \
  --lvm $UUID_LVM \
  --group "spaceport" \
  --root $UUID_ROOT \
  --resume $UUID_RESUME > ./spaceport-lts.conf

python3 generate.py \
  --name "Spaceport (No Resume)" \
  --kernel "vmlinuz-linux-zen" \
  --init "initramfs-linux-zen.img" \
  --ucode \
  --lvm $UUID_LVM \
  --group "spaceport" \
  --root $UUID_ROOT > ./spaceport-noresume.conf

python3 generate.py \
  --name "Spaceport (Protections)" \
  --kernel "vmlinuz-linux-zen" \
  --init "initramfs-linux-zen.img" \
  --ucode --spectre \
  --lvm $UUID_LVM \
  --group "spaceport" \
  --root $UUID_ROOT \
  --resume $UUID_RESUME > ./spaceport-protections.conf
