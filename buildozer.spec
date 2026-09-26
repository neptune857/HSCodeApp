name: Build APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    name: Build Android APK
    runs-on: ubuntu-latest

    steps:
    # 1. 检出代码
    - name: Checkout code
      uses: actions/checkout@v3

    # 2. 设置 Python 环境
    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    # 3. 安装 Python 依赖
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer cython

    # 4. 安装系统级依赖库
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y \
          build-essential \
          git \
          curl \
          flex \
          bison \
          gperf \
          libffi-dev \
          libssl-dev \
          libxml2-dev \
          libxslt1-dev \
          zlib1g-dev \
          libncurses5-dev \
          libnss3-dev \
          libudev-dev \
          libinput-dev \
          libwayland-dev \
          libxkbcommon-dev \
          libegl1-mesa-dev \
          libsdl2-dev \
          libsdl2-image-dev \
          libsdl2-mixer-dev \
          libsdl2-ttf-dev \
          libportmidi-dev \
          libswscale-dev \
          libavformat-dev \
          libavcodec-dev \
          libgstreamer1.0-dev \
          libgstreamer-plugins-base1.0-dev \
          android-sdk-command-line-tools

    # 5. 自动修正 buildozer.spec 配置错误（防止 Actions 打包失败）
    - name: Auto-Fix buildozer.spec
      run: |
        # 1. 如果文件里没有开启自动接受 SDK 许可，就强制在末尾追加一行
        if ! grep -q "android.accept_sdk_license = True" buildozer.spec; then
          echo "android.accept_sdk_license = True" >> buildozer.spec
          echo "[FIX] 已追加: android.accept_sdk_license = True"
        fi

        # 2. 将指向本地路径的 p4a.source_dir 注释掉
        sed -i 's/^p4a.source_dir/#p4a.source_dir/' buildozer.spec
        echo "[FIX] 已注释掉本地 p4a.source_dir 路径"

    # 6. 自动接受 Android SDK 许可协议
    - name: Accept Android SDK licenses
      run: |
        export ANDROID_HOME=${ANDROID_HOME:-$HOME/Android/Sdk}
        if [ -d "$ANDROID_HOME/cmdline-tools/latest/bin/" ]; then
          yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses
        else
          echo "WARNING: 未能找到 sdkmanager，将依赖 buildozer 内部处理"
        fi

    # 7. 使用 Buildozer 构建 APK
    - name: Build APK with Buildozer
      env:
        ANDROID_SDK_ROOT: ${{ env.ANDROID_HOME }}
      run: buildozer -v android debug

    # 8. 上传构建产物
    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: my-kivy-app-apk
        path: bin/*.apk
