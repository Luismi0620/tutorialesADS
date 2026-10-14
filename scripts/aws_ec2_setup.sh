#!/bin/sh
set -eu

# Tutorial 04 - Amazon Linux 2023.
sudo dnf update -y
sudo dnf install git docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

echo "Docker instalado. Cierre la sesión con 'exit' y vuelva a conectarse."
