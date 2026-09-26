[app]

# 1. 应用名称 (在安卓手机桌面上显示的名字)
title = HS编码

# 2. 应用包名 (安卓系统用来识别应用的唯一ID，必须全小写)
package.name = myapp

# 3. 应用域名 (一般写 com 或 org 开头)
package.domain = org.test

# 4. 源代码目录 (. 代表当前仓库的根目录)
source.dir = .

# 5. 需要包含的文件后缀 (你的项目里用到了 .kv 文件一定要在这里加上！)
source.include_exts = py,png,jpg,kv,atlas,json,ttf,mp3,ogg

# 6. 应用依赖库 (这里只写了 python3 和 kivy，如果你用了其他的如 requests, plyer，请加在这里，用逗号隔开)
requirements = python3,kivy

# 7. Kivy 应用的主文件名 (比如你入口文件是 main.py，这里就写 main)
# 如果你有 .kv 文件，并且文件名和 main.py 一样（main.kv），这里可以不写
source.main = main

# 8. 应用版本号
version = 0.1

# 9. 应用启动的 orientation (竖屏 portrait / 横屏 landscape)
orientation = portrait

# ------------------------------------------------
# Android 专用配置 (以下代码是解决你 GitHub Actions 报错的关键)
# ------------------------------------------------

# 10. 安卓最低支持版本
android.api = 27

# 11. 安卓构建目标版本
android.ndk_api = 21

# 12. 【核心修复 1】让 Buildozer 自动接受 SDK 许可协议，防止 CI 卡死
android.accept_sdk_license = True

# 13. 【核心修复 2】安卓应用图标 (你的仓库里已上传 icon.png)
icon.filename = icon.png

# 14. 安卓启动画面 (你的仓库里已上传 presplash.png)
presplash.filename = presplash.png

# 15. 安卓打包使用的 keystore (可选，不填会默认生成 debug 包)
# android.keystore =
# android.storepass =

[buildozer]

# 16. 构建过程中的详细日志级别 (0, 1, 2; 2代表输出最全，方便排查问题)
log_level = 2
