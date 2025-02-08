from packages.restclient.client import RestClient


class MailhogApi(RestClient):

    def get_v2_messages(
            self,
            limit=50
    ):
        """
        GET /api/v2/messages Retrieve users emails
        :param limit:
        :return:
        """
        params = {
            "limit": limit
        }
        response = self.get(
            path="/api/v2/messages",
            params=params
        )
        return response
