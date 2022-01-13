#!/bin/bash

chmod 775 ./*/DEBIAN
chmod 775 ./*/DEBIAN/*

compilationNumber=$(cat ./rpiMinecraftServer/DEBIAN/control | grep Version | awk '{print $2}')
newNumber=$(echo $compilationNumber | tr "." " " | awk '{print $1 "." $2 "." (($3+1))}')

sed -i "s/$compilationNumber/$newNumber/" "./rpiMinecraftServer/DEBIAN/control"

echo "##########################################################################"
echo "###################### Building new version ($newNumber) ######################"
echo "##########################################################################"
echo
echo "## Deleting old packages..."
rm ./*.deb
echo
echo "## Creating rpiminecraftserver package..."
dpkg-deb --build --root-owner-group ./rpiMinecraftServer
echo
echo "## Done"
