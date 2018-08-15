from pb.slack.api.calls import APICall


def test_success():
    response = APICall('api.test')()
    assert response['ok']
