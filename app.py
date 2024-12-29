from flask import Flask, render_template, request
from datetime import datetime
import pytz

app = Flask(__name__)

def convert_hours_to_discord_timestamp(date, hours, timezone="UTC"):
    try:
        # Combine the date and time into a single datetime object
        datetime_str = f"{date} {hours}"
        combined_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

        # Set the time zone (use the user's time zone)
        local_tz = pytz.timezone(timezone)
        local_time = local_tz.localize(combined_datetime)

        # Convert to Unix timestamp (in UTC)
        unix_timestamp = int(local_time.astimezone(pytz.utc).timestamp())

        # Generate the Discord timestamp format
        discord_timestamp = f"<t:{unix_timestamp}:t>"
        return discord_timestamp
    except ValueError as e:
        return f"Error: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    discord_code = ""
    if request.method == "POST":
        date_input = request.form.get("date")
        hours_input = request.form.get("hours")
        timezone_input = request.form.get("timezone", "UTC")  # Default to UTC if no timezone is selected
        discord_code = convert_hours_to_discord_timestamp(date_input, hours_input, timezone=timezone_input)
    return render_template("index.html", discord_code=discord_code)

if __name__ == "__main__":
    app.run(debug=True)