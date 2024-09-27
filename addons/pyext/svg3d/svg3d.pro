CONFIG -= qt
CONFIG += c++2b
TEMPLATE = lib
DEFINES += SVG3D_LIBRARY

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    svg3d.cpp

HEADERS += \
    svg3d_global.h \
    svg3d.h

# Default rules for deployment.
unix {
    target.path = /usr/lib
}
!isEmpty(target.path): INSTALLS += target
