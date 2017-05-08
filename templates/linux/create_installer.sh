# !/bin/bash
#
# Generate the game installer for Linux platform.
#
# Author: Edson Alves - edsonalves@unb.br
# Date: 12/03/2017

# Variables
SYSTEM=linux
CUR_DIR=`pwd`
BUILD_DIR=build/$SYSTEM
BIN_DIR=bin/$SYSTEM
DIST_DIR=dist/$SYSTEM
DIST_BIN_DIR=$DIST_DIR/bin

# Generates Debin package (.deb)
function debian_package
{
    echo "Building .deb package..."
    cd $BUILD_DIR
    pwd
    cpack
    cd $CUR_DIR
    mkdir -p $DIST_BIN_DIR
    mv $BUILD_DIR/*.deb $DIST_BIN_DIR/
    echo "Done"
}

# Generates a Qt installer (user friendly)
QT_PACKAGE_DATA_DIR=dist/$SYSTEM/packages/ninja/data
function qt_package
{
    echo "Building Qt package..."
    mkdir -p $QT_PACKAGE_DATA_DIR
    rm -f $QT_PACKAGE_DATA_DIR/*.7z
    echo $BIN_DIR
    Qt/QtIFW2.0.5/bin/archivegen data.7z $BIN_DIR media
    mv data.7z $QT_PACKAGE_DATA_DIR
    cd $DIST_DIR
    ../../Qt/QtIFW2.0.5/bin/binarycreator -c config/config.xml -p packages ninjasiegeSetup.sh
    cd $CUR_DIR
    mv $DIST_DIR/*.sh $DIST_BIN_DIR
    echo "Done"
}

# Main
case $1 in
    "all")
        echo "All"
        debian_package
        qt_package
        ;;

    "deb")
        echo "Deb"
        debian_package
        ;;

    "qt")
        echo "Qt"
        qt_package
        ;;

    *)
        echo "Usage: create_installer.sh [all|qt|deb]"
        exit 1
esac

