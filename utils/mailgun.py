import requests
from icalendar import Calendar, Event

from .exceptions import MailgunResponseException
from .abstract_mail_client import AbstractMailClient


class MailgunAPIClient(AbstractMailClient):
    """
    Class to implement requests to Mailgun service
    """

    version = "v3"
    api_url = "api.mailgun.net"
    messages_uri = "messages"

    mailgun_valid_response_type = 3

    def __init__(self, api_key, domain):
        self.api_key = api_key
        self.domain = domain

    def _build_url(self, uri):
        """ Creates URL by passed parameters """

        return f"{self.api_url}/{self.version}/{self.domain}/{uri}"

    def _make_request(self, url, data=None, files=None):
        """ Sending POST request to Mailgun API with errors processing """

        request_data = data or {}
        attachments = {"attachment": ("event.ics", files)} if files else {}
        response = requests.post(
            f"https://{url}",
            auth=("api", self.api_key),
            data=request_data,
            files=attachments,
        )

        if response.status_code != requests.codes.OK:
            raise MailgunResponseException()
        return response.text

    def send_message(self, message, event=None):
        """ Calls Mailgun API to send message """
        url = self._build_url(self.messages_uri)
        response = self._make_request(url, message, event)

        return response

    def generate_message(self, sender, receivers, subject, text):
        """
        parameters: 
            sender - string
            receivers - list of strings
            subject - string
            text - string
        """
        return {
            "from": f"{sender} <mailgun@{self.domain}>",
            "to": receivers,
            "subject": subject,
            "text": text,
        }

    def generate_event(self, start_date, end_date, subject, description):
        """
        parameters: 
            start_date - datetime()
            end_date - datetime()
            subject - string
            description - string
        """

        calendar = Calendar()
        event = Event()

        calendar.add("version", "2.0")
        event.add("summary", subject)
        event.add("dtstart", start_date)
        event.add("dtend", end_date)

        calendar.add_component(event)

        return calendar.to_ical()
