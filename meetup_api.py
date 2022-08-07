import requests
import logging

MEETUP_BASE_URL = "https://www.meetup.com"

def get_next_event(group):
    group_in_query = "-".join(group.split())
    r = requests.get(f"{MEETUP_BASE_URL}/mu_api/urlname/events", params= {
        "queries": f"(endpoint:{group_in_query}/events,list:(dynamicRef:list_events_{group_in_query}_upcoming_cancelled,merge:()),meta:(method:get),params:(desc:true,fields:'event_hosts,featured_photo,plain_text_no_images_description,series,self,rsvp_rules,rsvp_sample,venue,venue_visibility',has_ended:false,page:'1',scroll:'next_upcoming',status:'upcoming'),ref:events_{group_in_query}_upcoming_cancelled)"
    })

    if r.status_code != 200:
        return None
    json = r.json()
    responses = json.get('responses')

    # catch empty json, empty responses and unexpected lengths for the 'responses' key (it should always be 1)
    if not responses or len(responses) != 1:
        logging.error("Unexpected response from the Meetup internal API. It's possible the library needs an update.")
        return None

    # events ref is an identifier for the response type/schema (a graphql thing?)
    eventsRef = responses[0].get('ref')
    if not eventsRef == f"events_{group_in_query}_upcoming_cancelled":
        logging.warning("Response from the Meetup API does not have the expected schema ref. It's possible the library needs an update.")
        return None ## something changed in the API

    events = responses[0].get('value')
    if not events or len(events) == 0:
        return "no event"

    if isinstance(events, dict):
        logging.warning("error: unexpected response schema from meetup")
        errors = events.get('errors')
        if errors:
            logging.error(f"errors returned from meetup api: {errors}")
            return f"error: {errors[0].get('message')}"

    next_event = events[0]
    return {
        'event_name': next_event['name'],
        'event_description': next_event['plain_text_no_images_description'],
        'event_link': next_event['link'],
        'date_time': next_event['time'],
        'is_online': next_event['is_online_event'],
    }
