#! /bin/bash
OSXCROSS=$1
SDKPATH=${OSXCROSS}/SDK/MacOSX10.10.sdk
SDKVERSION=10.10
cat - mkspecs/features/mac/sdk.prf > /tmp/sdk.prf << EOF
QMAKE_MAC_SDK.macosx.Path = ${SDKPATH}
QMAKE_MAC_SDK.macosx.--show-sdk-path = ${SDKPATH}
QMAKE_MAC_SDK.macosx.SDKVersion = ${SDKVERSION}
QMAKE_MAC_SDK.macosx.--show-sdk-version = ${SDKVERSION}
QMAKE_MAC_SDK.macosx.PlatformPath = ${OSXCROSS}
QMAKE_MAC_SDK.macosx.--show-sdk-platform-path = ${OSXCROSS}

EOF
cp /tmp/sdk.prf mkspecs/features/mac/sdk.prf
