import pytest
import pandas as pd
from etl.extract.extract import extract_api


def test_extract_success(mocker):

    teststarttime = '2025-05-05T12:00:00'
    testendtime = '2025-05-06T12:00:00'
    mocker.patch('etl.extract.extract.requests.get',
                 side_effect=Exception(f'unable to retrieve data:{Exception}'))
    
    with pytest.raises(Exception,match=f'unable to retrieve data:{Exception}'):   
        response = extract_api(teststarttime,testendtime)
        assert response == f'unable to retrieve data:d '