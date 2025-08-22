#!/bin/sh
# 一鍵初始化腳本

if [ ! -f .env ]; then
  cp .env.example .env
  echo ".env 已自動產生"
else
  echo ".env 已存在，略過自動產生"
fi