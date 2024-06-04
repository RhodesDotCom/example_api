from flask import Flask, jsonify, current_app, request
from sqlalchemy import create_engine, text
import geojson


DATABASE_URI = 'postgresql+psycopg2://events_user:events_password@postgres:5432/events_db'

app = Flask(__name__)


def get_conn():
    engine = create_engine(DATABASE_URI)
    connection = engine.connect()
    return connection


@app.route('/venues/', methods=['POST'])
def add_venue():
    '''
    Add new venue to venues table.
    venue name is required
    bbox and capacity are optional
    '''

    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type. Content-Type must be application/json"}), 415

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
    except Exception as e:
        current_app.logger.info({'error': f'failed to decode JSON object: {e}', 'data': request.data})
        return jsonify({"error": str(e)}), 400
    
    venue_name = data.get('venue_name')
    bbox = data.get('bbox')
    capacity = data.get('capacity')

    if not venue_name or not isinstance(venue_name, str) or not venue_name.strip():
        return jsonify({"error": "Venue name is required"}), 400
    
    if capacity:
        if isinstance(capacity, str):
            try:
                capacity = int(capacity)
            except ValueError:
                return jsonify({"error": "Capacity must be a positive integer"}), 400
        elif not isinstance(capacity, int) or capacity < 0:
            return jsonify({"error": "Capacity must be a positive integer"}), 400

    if bbox:
        if isinstance(bbox, str):
            try:
                bbox_data = geojson.loads(bbox)
                if not bbox_data or 'type' not in bbox_data or 'coordinates' not in bbox_data:
                    raise ValueError("Invalid GeoJSON geometry")
            except (ValueError, TypeError):
                return jsonify({"error": "Locational bounding box (bbox) must be a valid GeoJSON"}), 400
            
    
    try:
        conn = get_conn()
        with conn.begin() as trans:
            sql = text('''INSERT INTO events_schema.venues (venue_name, bbox, capacity)
                        VALUES (:venue_name, ST_Transform(ST_GeomFromGeoJSON(:bbox), 27700), :capacity)
                        RETURNING venue_id''')
        
            result = conn.execute(sql, {
                'venue_name': venue_name,
                'bbox': bbox if bbox else None,
                'capacity': capacity if capacity else None
            })

            venue_id = result.fetchone()[0]
            venue_dict = {
                    "venue_id": venue_id,
                    "venue_name": venue_name,
                    "bbox": bbox,
                    "capacity": capacity
                }
    except Exception as e:
        current_app.logger.error(e)
        trans.rollback()
        return jsonify({"error": 'BAD REQUEST', "details": str(e)}), 400
    finally:
        conn.close()


    return jsonify(venue_dict), 201


@app.route('/venues/<int:id>', methods=['GET'])
def get_venue(id):
    '''
    Get venue from venues table from venue_id
    Returns venue_id, venue_name, bbox, and capacity
    '''
    
    try:
        conn = get_conn()
        sql = text('''SELECT venue_id, venue_name, ST_AsGeoJSON(bbox) as bbox, capacity
                FROM events_schema.venues
                WHERE venue_id = :id''')
        result = conn.execute(sql, {'id': id})
        venue = result.fetchone()

        if not venue:
            return jsonify({"error": "Venue not found"}), 404

        venue_dict = {
            "venue_id": venue[0],
            "venue_name": venue[1],
            "bbox": venue[2],
            "capacity": venue[3]
        }
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"error": 'BAD REQUEST',
                        "requestedResource": id}), 400
    finally:
        conn.close()

    return jsonify(venue_dict), 200


@app.route('/performing-artists/<int:id>', methods=['GET'])
def get_artists_performing_at_event(id):
    '''
    Get all artists performing at an event from the event id
    '''

    try:
        conn = get_conn()
        sql = text(
            '''select a.artist_name
            from events_schema.artists a 
            join events_schema.events_artists ea
            on a.artist_id = ea.artist_id 
            where ea.event_id = :id;'''
        )

        result = conn.execute(sql, {'id': id})
        artists = result.fetchall()

        if not artists:
            return jsonify({"error": "Event not found or no artists associated with this event"}), 404

        artists_list = [{'artist_name': row[0]} for row in artists]
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"error": 'BAD REQUEST',
                        "requestedResource": name}), 400
    finally:
        conn.close()

    return jsonify(artists_list), 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
    