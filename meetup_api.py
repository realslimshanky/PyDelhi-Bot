import logging

import requests

MEETUP_BASE_URL = 'https://www.meetup.com'


def get_next_event(group):  # NOQA: CFQ004 CCR001
    group_in_query = '-'.join(group.split())
    url = f'{MEETUP_BASE_URL}/mu_api/urlname/events'
    params = {
        'queries': (
            f'(endpoint:{group_in_query}/events,list:(dynamicRef:list_events_{group_in_query}_'
            "upcoming_cancelled,merge:()),meta:(method:get),params:(desc:true,fields:'event_hosts,"
            'featured_photo,plain_text_no_images_description,series,self,rsvp_rules,rsvp_sample,'
            "venue,venue_visibility',has_ended:false,page:'1',scroll:'next_upcoming',status:"
            f"'upcoming'),ref:events_{group_in_query}_upcoming_cancelled)"
        ),
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None
    json = response.json()
    responses = json.get('responses')

    # catch empty json, empty responses and unexpected lengths for the 'responses' key
    # (it should always be 1)
    if not responses or len(responses) != 1:
        logging.error((
            "Unexpected response from the Meetup internal API. It's possible the library needs an "
            'update.'
        ))
        return None

    # events ref is an identifier for the response type/schema (a graphql thing?)
    eventsRef = responses[0].get('ref')
    if eventsRef != f'events_{group_in_query}_upcoming_cancelled':
        logging.warning((
            "Response from the Meetup API does not have the expected schema ref. It's possible the "
            'library needs an update.'
        ))
        return None  # something changed in the API

    events = responses[0].get('value')
    if not events or len(events) == 0:
        return 'no event'

    if isinstance(events, dict):
        logging.warning('error: unexpected response schema from meetup')
        errors = events.get('errors')
        if errors:
            logging.error(f'errors returned from meetup api: {errors}')
            return f"error: {errors[0].get('message')}"

    return events[0]
