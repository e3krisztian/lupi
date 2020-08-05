# lupi_game_client.StatsApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_round**](StatsApi.md#get_round) | **GET** /rounds/{round} | 
[**get_round_result**](StatsApi.md#get_round_result) | **GET** /rounds/{round}/result | 
[**get_rounds**](StatsApi.md#get_rounds) | **GET** /rounds | 


# **get_round**
> Round get_round(round)



Get round details

### Example

```python
from __future__ import print_function
import time
import lupi_game_client
from lupi_game_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = lupi_game_client.Configuration(
    host = "http://localhost/v1"
)


# Enter a context with an instance of the API client
with lupi_game_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = lupi_game_client.StatsApi(api_client)
    round = 'current' # str |  (default to 'current')

    try:
        api_response = api_instance.get_round(round)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatsApi->get_round: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **round** | **str**|  | [default to &#39;current&#39;]

### Return type

[**Round**](Round.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Details of round |  -  |
**404** | Round is not available |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_round_result**
> RoundResult get_round_result(round)



Get round result

### Example

```python
from __future__ import print_function
import time
import lupi_game_client
from lupi_game_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = lupi_game_client.Configuration(
    host = "http://localhost/v1"
)


# Enter a context with an instance of the API client
with lupi_game_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = lupi_game_client.StatsApi(api_client)
    round = 'current' # str |  (default to 'current')

    try:
        api_response = api_instance.get_round_result(round)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatsApi->get_round_result: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **round** | **str**|  | [default to &#39;current&#39;]

### Return type

[**RoundResult**](RoundResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | results |  -  |
**404** | Round/its result is not available |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_rounds**
> ListOfRounds get_rounds(before=before, limit=limit)



List completed rounds, most recent first, paged

### Example

```python
from __future__ import print_function
import time
import lupi_game_client
from lupi_game_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = lupi_game_client.Configuration(
    host = "http://localhost/v1"
)


# Enter a context with an instance of the API client
with lupi_game_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = lupi_game_client.StatsApi(api_client)
    before = 4 # int | (Paging) Return rounds before this round id (optional)
limit = 25 # int | (Paging) Return at most this many rounds at once (optional)

    try:
        api_response = api_instance.get_rounds(before=before, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatsApi->get_rounds: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **before** | **int**| (Paging) Return rounds before this round id | [optional] 
 **limit** | **int**| (Paging) Return at most this many rounds at once | [optional] 

### Return type

[**ListOfRounds**](ListOfRounds.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Limited list of rounds - round data (IDs and start date, end date, number of participants) - and paging link  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
