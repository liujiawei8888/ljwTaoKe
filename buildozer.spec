[app]
title = SEO发布工具
package.name = seopublish
package.domain = org.seopublish
source.include_exts = py,png,jpg,kv,atlas,json,html,csv,ttf
source.include_patterns = *.py,*.kv,*.json,*.html,*.txt
version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.arch = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
