from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

MICROSERVICE_LINK = "https://appbox.qatar.cmu.edu/313-teams/team_name/"

# Mentor list: each mentor has 2 teams
MENTORS = ["Seckhen", "Aadi", "Steve", "Seckhen", "Aadi", "Steve"]

@app.get("/team_info/{team_id}")
def get_team_info(team_id: str):
    if not team_id:
        raise HTTPException(status_code=404, detail="Missing team id")

    # Converting team_id to integer for indexing
    try:
        team_index = int(team_id) - 1 
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid team id")

    # Calling existing microservice to get team name
    response = requests.get(MICROSERVICE_LINK + team_id)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Team not found in microservice")

    data = response.json()
    team_name = data.get("team_name")
    if not team_name:
        raise HTTPException(status_code=404, detail="Team name missing in microservice response")

    # Assigning mentor based on team_index
    if team_index < len(MENTORS):
        mentor_name = MENTORS[team_index]
    else:
        mentor_name = "Unknown"
    return {
        "team_id": team_id,
        "team_name": team_name,
        "mentor": mentor_name
    }
