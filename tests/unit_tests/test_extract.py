import pytest
from etl.extract.extract import extract_api
import requests


def test_extract_success(mocker):
    # Arrange
    mock_requests = mocker.patch('etl.extract.extract.requests.get')
    teststarttime = '2025-05-05T12:00:00'
    testendtime = '2025-05-06T12:00:00'
    query = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'\
            f'format=geojson&starttime={teststarttime}&endtime={testendtime}'
    # Act
    extract_api(query)
    # Assert
    mock_requests.assert_called_once_with(query, timeout=60)
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
        response = extract_api('testquery')
        # Assert
        assert response == f'HTTP error: {400}'


def test_extract_failure(mocker):
    # Arrange
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
        response = extract_api("testquery")
        # Assert
        assert response == f'unable to retrieve data: {Exception}'
