async def test_root_returns_200(client):
    response = await client.get("/")
    assert response.status_code == 200


async def test_root_returns_message(client):
    response = await client.get("/")
    assert response.json() == {"message": "SpaceX Launch Tracker API"}
