## Closets Entity

The Closets entity represents each user's unique closet, storing a JSON list of clothes IDs and linking to the user.

### Folder structure
DigitalCloset/
├── models/
│ └── Closets_Model.py
├── tests/
│ ├── sample_closet_data.py
│ └── test_closets_model.py


"""
# Outfits Model

## Project Overview
Digital Closet lets users create outfits from clothes and organize them socially.

## Folder Structure

```
DigitalCloset/
├── closetappDB.db
├── models/
│   └── Outfits_Model.py
├── tests/
│   ├── sample_outfits_data.py
│   └── test_outfits_model.py
└── README.md
```

## Outfits Class Model
```mermaid
classDiagram
    class Outfits_Model {
        +initialize_DB(DB_name: string)
        +exists(outfit_name: string | id: int) bool
        +create(outfit_info: dict) dict
        +get_outfit(outfit_name: string | id: int) dict
        +get_all() list
        +get_all_user_outfits(username: string | user_id: int) list
        +remove(id: int) dict
    }
```

## Running Unit Tests
```bash
cd DigitalCloset
pytest tests/test_outfits_model.py
```
"""
