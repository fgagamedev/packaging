cmake_minimum_required(VERSION 2.6)

set(SYSTEM linux)

# External libraries configure options
set(SDL_CONFIGURE_OPTIONS --enable-video-x11 --enable-x11-shared --enable-video-x11-vm)
# set(SDL_IMAGE_CONFIGURE_OPTIONS "")
# set(SDL_NET_CONFIGURE_OPTIONS "")
# set(SDL_MIXER_CONFIGURE_OPTIONS "")
# set(FREETYPE_CONFIGURE_OPTIONS "")
# set(SDL_TTF_CONFIGURE_OPTIONS "")

set(SYSTEM_LIBRARIES libSDL2.so libSDL2_image.so libSDL2_ttf.so libSDL2_mixer.so libSDL2_gfx.so libSDL2_net.so)
