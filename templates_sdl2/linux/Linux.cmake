cmake_minimum_required(VERSION 2.6)

set(SYSTEM linux)

# External libraries configure options
set(SDL_CONFIGURE_OPTIONS --enable-video-x11 --enable-x11-shared --enable-video-x11-vm)

set(SYSTEM_LIBRARIES libSDL2.so libSDL2_image.so libSDL2_ttf.so libSDL2_mixer.so libSDL2_gfx.so libSDL2_net.so libijengine.a)
