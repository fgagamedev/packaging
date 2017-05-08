cmake_minimum_required(VERSION 2.6)

set(SYSTEM linux)

# External libraries configure options
set(SDL_CONFIGURE_OPTIONS --enable-video-x11 --enable-x11-shared --enable-video-x11-vm)
set(SDL_IMAGE_CONFIGURE_OPTIONS "")
set(SDL_MIXER_CONFIGURE_OPTIONS "")
set(FREETYPE_CONFIGURE_OPTIONS "")
set(SDL_TTF_CONFIGURE_OPTIONS "")

set(SYSTEM_LIBRARIES libSDL.so libSDL_image.so libSDL_mixer.so libSDL_ttf.so libfreetype.so)

