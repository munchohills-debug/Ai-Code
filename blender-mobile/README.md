# Blender Mobile (Android + iOS)

A mobile-port project layout for running Blender on Android and iOS.

> **Important:** This repository contains the mobile project/build scaffolding, not a prebuilt official Blender APK/IPA. Blender is a large native application and must be built from source for each target platform.

## Project layout

```text
blender-mobile/
├── README.md
├── android/
│   └── README.md
├── ios/
│   └── README.md
└── scripts/
    └── README.md
```

## Android

The Android target should package a native Blender build into an Android application. The recommended approach is to build Blender's C/C++ dependencies with the Android NDK and provide a touch-friendly Activity/UI layer.

## iOS

The iOS target requires an Xcode project and iOS-compatible builds of Blender's native dependencies. App Store distribution also requires Apple signing and provisioning.

## Goal

- Touch-first Blender controls
- On-screen navigation/orbit/pan/zoom
- External keyboard and mouse support
- Android APK/AAB build output
- iOS IPA/Xcode build output
- Keep Blender's core 3D functionality rather than making a simplified 3D editor
