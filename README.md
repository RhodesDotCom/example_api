# iventis_api

# Prerequisites
Docker

# Start
To start the database and API routes navigate to the cloned directory containing docker-compose.yml and run: "docker-compose up -d --build".

# Routes
POST /venues <br/>
Host: localhost:5000 <br/>
example input:
    {
        "venue_name": "Example 1",
        "capacity": "20000", 
        "bbox": {}
    }


GET /venues/{venue_id} <br/>
Host: localhost:5000 <br/>
example response: <br/>
    {
        "bbox": "{}",
        "capacity": 100,
        "venue_id": 1,
        "venue_name": "example venue"
    }


GET /performing-artists/{event_id} <br/>
Host: localhost:5000 <br/>
example response: <br/>
    [
        {
            "artist_name": "artist 1" 
        },
        {  
            "artist_name": "artist 2"
        }
    ]