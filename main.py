from fastapi import  FastAPI

import models_orm
from database import database_engine

import router_teams

# Créer les tables si elles ne sont pas presesntes dans la DB
models_orm.Base.metadata.create_all(bind=database_engine)


# Description
api_description = description = """
Football API help you to find players and teams.

## Players
You will be able to : 
* Create New Players
* Get Players by id
"""
# Liste des tags utilises dans la doc

tags_metadata = [{
    "name" : "Players",
    "description" : " Manage Players. So _Fancy_ they have their own docs",
    "externalDocs" : {
        "description" : "Items external docs",
        "url":"https://fastapi.taingolo.com/",
    },
    },
]

app = FastAPI(
    title="Football API",
    description= api_description,
    openapi_tags= tags_metadata # Tags metadata
)

app.include_router(router_teams.router)