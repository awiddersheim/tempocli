def test_tempo_client(tempo_client, tempo_request):
    request = tempo_request.get('/foo')
    response = tempo_client.get('/foo')

    assert response.status_code == 200
    assert request.called_once
    assert request.last_request.headers['User-Agent'].startswith('tempocli python-requests')
    assert request.last_request.headers['Authorization'] == 'Bearer {}'.format(tempo_client.token)
