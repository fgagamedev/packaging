# !/bin/bash
#
# Generate the game executable for Linux platform.
#
# Author: Edson Alves - edsonalves@unb.br
# Date: 09/03/2017

# System
SYSTEM=linux

# Directories
BIN_DIR=bin
SRC_DIR=src
LIB_DIR=lib
BUILD_DIR=build

SYSTEM_BIN_DIR=$BIN_DIR/$SYSTEM
SYSTEM_LIB_DIR=$LIB_DIR/$SYSTEM
SYSTEM_BIN_LIB_DIR=$SYSTEM_BIN_DIR/lib
SYSTEM_BUILD_DIR=$BUILD_DIR/$SYSTEM

SDL_DIR=$SYSTEM_LIB_DIR/SDL-1.2
SDL_LIB_DIR=$SDL_DIR/lib

FREETYPE_DIR=$SYSTEM_LIB_DIR/FreeType-2.4
FREETYPE_LIB_DIR=$FREETYPE_DIR/lib

mkdir -p $BUILD_DIR/$SYSTEM $BIN_DIR/$SYSTEM/lib
cd $BUILD_DIR/$SYSTEM
pwd
cmake ../.. -DCMAKE_TOOLCHAIN_FILE=../../linux/Linux.cmake
make
cd ../..
cp $SYSTEM_BUILD_DIR/$SRC_DIR/ninjasiege $SYSTEM_BIN_DIR
cp $SDL_LIB_DIR/libSDL-1.2.so.0 $SYSTEM_BIN_LIB_DIR
cp $SDL_LIB_DIR/libSDL_image-1.2.so.0 $SYSTEM_BIN_LIB_DIR
cp $SDL_LIB_DIR/libSDL_mixer-1.2.so.0 $SYSTEM_BIN_LIB_DIR
cp $SDL_LIB_DIR/libSDL_ttf-2.0.so.0 $SYSTEM_BIN_LIB_DIR
cp $FREETYPE_LIB_DIR/libfreetype.so.6.5.0 $SYSTEM_BIN_LIB_DIR
