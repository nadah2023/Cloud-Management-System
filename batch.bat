@echo off
qemu-img create -f qcow2 Image.img 10G
qemu-system-x86_64 -name vm1 -accel whpx,kernel-irqchip=off -cdrom ubuntu-22.04.3-desktop-amd64.iso -boot menu=on -drive file=Image.img -m 2G
