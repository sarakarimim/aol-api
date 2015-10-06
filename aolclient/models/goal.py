import json

from aolclient.models.base import Base


class Goal(Base):

    def getId(self):
        return self.get('goalId')

    def get_by_campaign(self, campaign_id, advertiser_id, organization_id):
        url = '{0}/video-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/goals'.format(Base.connection.url, organization_id, advertiser_id, campaign_id)
        method = "GET"
        
        response = self._execute(method, url, '')
        return self._get_response_objects(response)
        

    
