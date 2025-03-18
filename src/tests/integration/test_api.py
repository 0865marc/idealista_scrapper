from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_read_root(mocker):
    mock_task = mocker.patch("src.tasks.tasks.get_properties_from_list_page.delay")
    task_result = mocker.Mock()
    task_result.id = "task-id-123"
    mock_task.return_value = task_result

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "task-id-123"}
    mock_task.assert_called_once()
