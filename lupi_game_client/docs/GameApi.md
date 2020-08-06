# lupi_game_client.GameApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_vote**](GameApi.md#add_vote) | **POST** /votes | 
[**create_round**](GameApi.md#create_round) | **POST** /rounds | 
[**get_current_round_id**](GameApi.md#get_current_round_id) | **GET** /rounds/current/id | 
[**get_round_result**](GameApi.md#get_round_result) | **GET** /rounds/{round}/result | 
[**set_round_completed**](GameApi.md#set_round_completed) | **PUT** /rounds/{round}/is_completed | 


# **add_vote**
> add_vote(vote)



Register a user vote

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
    api_instance = lupi_game_client.GameApi(api_client)
    vote = lupi_game_client.Vote() # Vote | 

    try:
        api_instance.add_vote(vote)
    except ApiException as e:
        print("Exception when calling GameApi->add_vote: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **vote** | [**Vote**](Vote.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Vote accepted |  -  |
**409** | Already voted or the round is already closed |  -  |
**404** | Round is not available |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_round**
> int create_round()



Creates a new game round

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
    api_instance = lupi_game_client.GameApi(api_client)
    
    try:
        api_response = api_instance.create_round()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GameApi->create_round: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**int**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | A new game round was created |  -  |
**409** | An active game round already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_current_round_id**
> int get_current_round_id()



Return the current round id

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
    api_instance = lupi_game_client.GameApi(api_client)
    
    try:
        api_response = api_instance.get_current_round_id()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GameApi->get_current_round_id: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**int**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Current round id |  -  |
**404** | Not started a round yet |  -  |

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
    api_instance = lupi_game_client.GameApi(api_client)
    round = 'current' # str |  (default to 'current')

    try:
        api_response = api_instance.get_round_result(round)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GameApi->get_round_result: %s\n" % e)
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

# **set_round_completed**
> set_round_completed(round, body=body)



Completes a round, calculates winner

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
    api_instance = lupi_game_client.GameApi(api_client)
    round = 'current' # str |  (default to 'current')
body = True # bool |  (optional)

    try:
        api_instance.set_round_completed(round, body=body)
    except ApiException as e:
        print("Exception when calling GameApi->set_round_completed: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **round** | **str**|  | [default to &#39;current&#39;]
 **body** | **bool**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Either of - game round was completed - no change  |  -  |
**409** | When value is false and the round is already completed.  Reopening a round is not supported because completed rounds make information public which would allow one to win - it is a possible cheating vector.  |  -  |
**404** | Round is not available |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

