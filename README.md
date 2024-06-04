# iventis_api

# Prerequisites
Docker

# Start
To start database and API routes navigate to directory containing docker-compose.yml and run: "docker-compose up -d --build"

# Routes
POST /venues
Host: localhost:5000
example input:
    {
        "venue_name": "Example 1",
        "capacity": "20000", 
        "bbox": {}
    }

venue_name is mandatory
capacity and bbox are optional


GET /venues/{venue_id}
Host: localhost:5000
example response:
    {
        "bbox": "{}",
        "capacity": 100,
        "venue_id": 1,
        "venue_name": "example venue"
    }


GET /performing-artists/{event_id}
Host: localhost:5000
example response:
    [
        {
            "artist_name": "artist 1"
        },
        {
            "artist_name": "artist 2"
        }
    ]