# Raccourcis d'exploitation de la plateforme
# Usage : make <cible>

COMPOSE = docker compose -f docker/docker-compose.yml --env-file .env

.PHONY: core-up core-down core-logs core-ps clean

core-up:          ## Démarre le profil core
	$(COMPOSE) --profile core up -d

core-down:        ## Arrête le profil core
	$(COMPOSE) --profile core down

core-logs:        ## Affiche les journaux du profil core
	$(COMPOSE) --profile core logs -f

core-ps:          ## Liste les conteneurs en cours
	$(COMPOSE) ps

clean:            ## Arrête tout et supprime les volumes — données perdues
	$(COMPOSE) --profile core down -v
