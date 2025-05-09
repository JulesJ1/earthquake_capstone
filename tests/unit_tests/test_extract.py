import pytest
from etl.extract.extract import extract_api
import requests


def test_extract_success(mocker):
    # Arrange
    mock_requests = mocker.patch('etl.extract.extract.requests.get')
    teststarttime = '2025-05-05T12:00:00'
    testendtime = '2025-05-06T12:00:00'
    query = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={teststarttime}&endtime={testendtime}'
    # Act
    extract_api(teststarttime, testendtime)
    # Assert
    mock_requests.assert_called_once_with(query, timeout=5)
    mock_requests = mocker.patch('etl.extract.extract.requests.get')


def test_extract_bad_request(mocker):
    # Arrange
    mocker.patch(
        'etl.extract.extract.requests.get',
        side_effect=requests.exceptions.HTTPError('400')
    )
    # Act
    with pytest.raises(
                    Exception, 
                    match=f'HTTP error: {400}'
                    ):
        response = extract_api('teststarttime', 'testendtime')
        # Assert
        assert response == f'HTTP error: {400}'


def test_extract_failure(mocker):
    # ArraNGE
    teststarttime = '2025-05-05T12:00:00'
    testendtime = '2025-05-06T12:00:00'
    mocker.patch(
                    'etl.extract.extract.requests.get',
                    side_effect=Exception(
                        f'unable to retrieve data: {Exception}'
                    )
                )

    with pytest.raises(
                        Exception, 
                        match=f'unable to retrieve data: {Exception}'
                       ):
        # Act
        response = extract_api(teststarttime, testendtime)
        # Assert
        assert response == f'unable to retrieve data: {Exception}'
