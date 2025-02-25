include .env

# Docker

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down --rmi all --volumes

docker-exec-app:
	docker compose exec app bash

docker-exec-app-ls:
	docker compose exec app ls


# python

python-version:
	docker compose exec app python --version

pip-version:
	docker compose exec app pip --version

main:
	docker compose exec app python main.py


# gazer

gazer-install:
	brew install rbenv \
	&& rbenv install 3.1.6 \
	&& rbenv local 3.1.6 \
	&& gem install gazer

# ~/.netrc設定
# 下記でファイルを作成し、クレデンシャル情報を入力
# APIキーの取得方法: https://cloud.google.com/looker/docs/admin-panel-users-users?hl=ja#api_keys
# フォーマットは .netrc_format を参照
add-credential-netrc:
	touch ~/.netrc \
	&& chmod 600 ~/.netrc \
	&& open ~/.netrc

dir = src/json/`TZ='Asia/Tokyo' date '+%Y%m%d-%H%M'`

# スペースの情報を取得
# スペースID: 107 の情報を取得したい例: `make space-cat-107`
# 参考: https://github.com/looker-open-source/gzr#space-cat
space-cat-%:
	mkdir -p $(dir) \
	&& gzr space cat ${@:space-cat-%=%} \
	--host $(LOOKER_HOST) \
	--dir $(dir)

# スペースの情報を、配下のダッシュボード情報も含めて取得
# スペースID: 4379 の情報を取得したい例: `make space-export-4379`
# 参考: https://github.com/looker-open-source/gzr#space-export
space-export-%:
	mkdir -p $(dir) \
	&& gzr space export ${@:space-export-%=%} \
	--host $(LOOKER_HOST) \
	--dir $(dir)
	
# ダッシュボードの情報を取得
# ダッシュボードID: 138 の情報を取得したい例: `make dashboard-cat-138`
# 参考: https://github.com/looker-open-source/gzr#dashboard-cat
dashboard-cat-%:
	mkdir -p $(dir) \
	&& gzr dashboard cat ${@:dashboard-cat-%=%} \
	--host $(LOOKER_HOST) \
	--dir $(dir)

# Lookの情報を取得
# Look ID: 31079 の情報を取得したい例: `make look-cat-31079`
# 参考: https://github.com/looker-open-source/gzr#look-cat
look-cat-%:
	mkdir -p $(dir) \
	&& gzr look cat ${@:look-cat-%=%} \
	--host $(LOOKER_HOST) \
	--dir $(dir)
