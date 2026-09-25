.PHONY: local-up local-down dev-up dev-down prod-up prod-down ps clean

# Local окружение
local-up:
	docker compose --env-file .env -f compose.local.yaml up -d --build

local-down:
	docker compose -f compose.local.yaml down

# Dev окружение
dev-up:
	docker compose --env-file .env.dev -f compose.dev.yaml up -d --build

dev-down:
	docker compose -f compose.dev.yaml down

# Prod окружение
prod-up:
	docker compose --env-file .env.prod -f compose.prod.yaml up -d --build

prod-down:
	docker compose -f compose.prod.yaml down

# Просмотр статуса и очистка
ps:
	docker compose -f compose.local.yaml ps

clean:
	docker system prune -f