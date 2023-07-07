from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata

# Database 
from classes.database import database_engine 
import classes.models_orm # Import des ORM

# Import des routers
import routers.router_teams,routers.router_transfers, routers.router_expenses, routers.router_auth

# Créer les tables si elles ne sont pas présente dans la DB
classes.models_orm.Base.metadata.create_all(bind=database_engine)

#Lancement de l'API
app = FastAPI(
    title="Football API",
    description= api_description,
    openapi_tags= tags_metadata # Tags metadata
)

# Routers dédiés
app.include_router(routers.router_teams.router)
app.include_router(routers.router_transfers.router)
app.include_router(routers.router_expenses.router)
app.include_router(routers.router_auth.router)