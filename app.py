import redis
from flask import jsonify

from entrypoint import app


@app.route('/collect', methods=['GET'])
def collect_engine_temperature():
    # Connect to the Redis database (ensure that Redis is running in a separate container, usually with 'redis' as the hostname)
    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

    # Retrieve the engine temperature list from Redis
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)

    # Check if there are any values in the list
    if not engine_temperature_values:
        return {"error": "No engine temperature data available."}, 404

    # Convert the values to float for numerical calculations
    engine_temperature_values = [float(temp) for temp in engine_temperature_values]

    # Get the current engine temperature (most recent reading)
    current_engine_temperature = engine_temperature_values[0]

    # Calculate the average engine temperature
    average_engine_temperature = sum(engine_temperature_values) / len(engine_temperature_values)

    # Return the results
    return jsonify({
        "current_engine_temperature": current_engine_temperature,
        "average_engine_temperature": average_engine_temperature
    }), 200
