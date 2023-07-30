[Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) dockerized for Ubuntu 20.04 and GeForce GTX 1080.

Based off [siutin/stable-diffusion-webui-docker](https://github.com/siutin/stable-diffusion-webui-docker/blob/9275d812653da52c91a7fd3694a7408ac85196b4/Dockerfile.cuda).

## CUDA compatibility
- [stackoverflow](https://stackoverflow.com/questions/60987997/why-torch-cuda-is-available-returns-false-even-after-installing-pytorch-with)
- [wikipedia](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)
    - [local GPU to compute capability version](./gpu_to_compute_capability_version.html)
    - [local compute capability version to CUDA version](./compute_capability_version_to_cuda_version.html)

## Some more details:

```
$ apt list --installed | grep nvidia

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

libnvidia-cfg1-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
libnvidia-common-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 all [installed,automatic]
libnvidia-compute-418/focal,now 430.50-0ubuntu3 amd64 [installed,automatic]
libnvidia-compute-430/focal-updates,focal-security,now 440.100-0ubuntu0.20.04.1 amd64 [installed,automatic]
libnvidia-compute-440/focal-updates,focal-security,now 450.119.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
libnvidia-compute-450/focal-updates,focal-security,now 460.91.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
libnvidia-compute-460/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
libnvidia-compute-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
libnvidia-container-tools/bionic,now 1.14.0~rc.2-1 amd64 [installed,automatic]
libnvidia-container1/bionic,now 1.14.0~rc.2-1 amd64 [installed,automatic]
libnvidia-decode-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
libnvidia-encode-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
libnvidia-extra-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
libnvidia-fbc1-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
libnvidia-gl-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
libnvidia-ifr1-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
nvidia-compute-utils-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
nvidia-container-toolkit-base/bionic,now 1.14.0~rc.2-1 amd64 [installed,automatic]
nvidia-container-toolkit/bionic,now 1.14.0~rc.2-1 amd64 [installed]
nvidia-dkms-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
nvidia-driver-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed]
nvidia-kernel-common-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
nvidia-kernel-source-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
nvidia-prime/focal-updates,now 0.8.16~0.20.04.2 all [installed,automatic]
nvidia-settings/focal-updates,now 470.57.01-0ubuntu0.20.04.3 amd64 [installed,automatic]
nvidia-utils-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
xserver-xorg-video-nvidia-470/focal-updates,focal-security,now 470.199.02-0ubuntu0.20.04.1 amd64 [installed,automatic]
```
