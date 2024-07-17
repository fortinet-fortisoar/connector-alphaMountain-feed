"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""
import json

import requests
from connectors.core.connector import get_logger, ConnectorError

from .constants import API_VERSION, REQUEST_TYPE, DEFAULT_USER_AGENT, DEFAULT_CATEGORIES

logger = get_logger('alphamountain-feed')


class alphaMountainFeed(object):

    def __init__(self, config):
        self.server_url = config.get('server_url', '').strip()
        if not self.server_url.startswith('https://') and not self.server_url.startswith('http://'):
            self.server_url = 'https://' + self.server_url
        # need to remove
        self.server_url = 'https://batch.alphamountain.ai'
        self.verify_ssl = config.get('verify_ssl', False)
        # self.api_key = config.get('api_key')
        # need to remove
        self.api_key = '2c52b78c-626e-45e0-b263-ae6d30e8b380'
        self.headers = {'Content-Type': 'application/json'}
        self.version = API_VERSION
        self.request_type = REQUEST_TYPE

    def make_api_call(self, endpoint=None, method='POST', payload=None, params=None):
        service_endpoint = self.server_url + endpoint
        try:
            response = requests.request(method, service_endpoint, data=payload, headers=self.headers, params=params,
                                        verify=self.verify_ssl)
            logger.debug('API Payload: {0}'.format(payload))
            logger.debug('API Response Reason: {0}'.format(response.reason))
            logger.debug('API Service Endpoint: {0}'.format(service_endpoint))
            logger.debug('API Response Status code: {0}'.format(response.status_code))
            logger.debug('API Response: {0}'.format(response.text))
            if response.ok:
                return response.json()
            else:
                logger.error('Failed with response {0}'.format(response.text))
                raise ConnectorError(
                    {'status': 'Failure', 'status_code': str(response.status_code), 'response': response.text})
        except requests.exceptions.SSLError as err:
            logger.error(err)
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout as err:
            logger.error(err)
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout as err:
            logger.error(err)
            raise ConnectorError('The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError as err:
            logger.error(err)
            raise ConnectorError('Invalid endpoint or credentials')
        except Exception as err:
            logger.error(err)
            raise ConnectorError(str(err))


def get_payload(params, alpha_feed):
    payload = {'version': alpha_feed.version, 'license': alpha_feed.api_key}
    flags = params.get('flags', '')
    if flags:
        params['flags'] = [flag.lower().replace(' ', '-') for flag in flags if flags]
    params = {k: v for k, v in params.items() if v is not None and v != ''}
    payload.update(params)
    return payload


def get_available_category(config={}, params={}, response_type='dict'):
    headers = {'user-agent': DEFAULT_USER_AGENT}
    service_endpoint = 'https://www.alphamountain.ai/api/am_mapping.json'
    default_response = DEFAULT_CATEGORIES if response_type == 'dict' else list(DEFAULT_CATEGORIES.values())
    try:
        resp = requests.request('POST', service_endpoint, headers=headers)
        if resp.ok:
            json_data = resp.json()
            categories = {key: value.get('name') for key, value in json_data.items()}
            categories = categories if response_type == 'dict' else list(categories.values())
            return categories
        else:
            return default_response
    except:
        return default_response


def get_category_ids(categories):
    categories_resp = get_available_category(response_type='dict')
    return [key for key, val in categories_resp.items() if val in categories]


def get_indicator_category(params, alpha_feed):
    try:
        payload = get_payload(params, alpha_feed)
        indicator_feed_with_categories = alpha_feed.make_api_call('/category/feed/json', payload=json.dumps(payload))
        return indicator_feed_with_categories.get('feed', [])
    except Exception as err:
        logger.error("Getting error while fetching indicators categories")
        logger.error(err)


def get_indicator_popularity(params, alpha_feed):
    try:
        payload = get_payload(params, alpha_feed)
        indicator_feed_with_popularity = alpha_feed.make_api_call('/popularity/feed/json', payload=json.dumps(payload))
        return indicator_feed_with_popularity.get('feed', [])
    except Exception as err:
        logger.error("Getting error while fetching indicators popularity")
        logger.error(err)


def build_response(indicator_threat_feeds, indicator_feed_categories):
    final_response = []
    for indicator_threat in indicator_threat_feeds:
        try:
            category_entry = next(
                filter(lambda x: x['hostname'] == indicator_threat['hostname'], indicator_feed_categories))
            merged_response = {**indicator_threat, **category_entry}
            final_response.append(merged_response)
        except StopIteration:
            final_response.append(indicator_threat)
    return final_response


def get_indicators(config, params):
    alpha_feed = alphaMountainFeed(config)
    include_categories = params.pop('include_categories', '')
    include_popularity = params.pop('include_popularity', '')
    categories = params.pop('categories', '')
    payload = get_payload(params, alpha_feed)
    resp = alpha_feed.make_api_call('/threat/feed/json', payload=json.dumps(payload))
    final_response = resp.get('feed')
    risk_min = params.pop('risk_min', '')
    risk_max = params.pop('risk_max', '')
    if include_categories:
        if categories:
            categories_ids = get_category_ids(categories)
            params['categories'] = categories_ids
        indicator_feed_categories = get_indicator_category(params, alpha_feed)
        final_response = build_response(final_response, indicator_feed_categories)
    if include_popularity:
        categories = params.pop('categories', '')
        flags = params.pop('flags', '')
        feed_indicator_popularity = get_indicator_popularity(params, alpha_feed)
        final_response = build_response(final_response, feed_indicator_popularity)
    return final_response


def _check_health(config):
    am = alphaMountainFeed(config)
    payload = {'version': am.version, 'license': am.api_key, 'endpoint': 'category'}
    return am.make_api_call('/threat/feed/json', payload=json.dumps(payload))


operations = {
    'get_indicators': get_indicators
}
