import src.app as app_module


def test_get_activities_returns_expected_shape(client):
    # Arrange
    expected_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

    first_activity = next(iter(data.values()))
    assert expected_keys.issubset(first_activity.keys())
    assert isinstance(first_activity["participants"], list)


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    participants = app_module.activities[activity_name]["participants"]
    if email in participants:
        participants.remove(email)

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "remove.student@mergington.edu"
    participants = app_module.activities[activity_name]["participants"]
    if email not in participants:
        participants.append(email)

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]
