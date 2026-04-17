[app]
title = SEO发布工具
package.name = seopublish
package.domain = org.seopublish
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,html,csv,ttf,pyc,txt,md
source.include_patterns = *.py,*.kv,*.json,*.html,*.txt,*.md
version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
