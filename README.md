# BLANK MULTILAYERS API PROJECT  
## FASTAPI AND POSTGRESQL  

**features tags**: crud router, filters, custom response, caching, logging, serialization, configuration  

**MULTILAYERS architecture structure:**  

```
├ main
├ app/
    ├── data/
        ├── database.py  # database provider
        ├── models/    # BLANK ORM-models for database
        ├── schemas/   # BLANK Pydantic-schemes for models serialization
    ├── repositories/
        ├── interfaces/
            ├── generic_repository.py  # Base repository
        ├── item_repository.py         # BLANK repository
        ├── user_repository.py         # BLANK repository
    ├── routes/ 
        ├── item_router.py  # BLANK router
        ├── user_router.py  # BLANK router
    ├── services/ # business logic
        ├── item_service.py  # BLANK service
        ├── user_service.py  # BLANK service
    ├── utils/
        ├── logging/
            ├── logger_creator.py  # Logger creator
        ├── responding/
            ├── models/            # Response models
            ├── response_creator.py # Response creator

```

How to start:
- *Check requirements.txt to load all environment dependencies*
- *Check config.py for all .env variables needed*
