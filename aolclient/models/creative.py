import json

from aolclient.models.base import Base

from aolclient.service.connection import Connection


class Creative(Base):

    obj_name = "creatives"

    def get_by_id(self, creative_id, organization_id, advertiser_id):
        url = '{0}/video-management/v2/organizations/{1}/advertisers/{2}/creatives/{3}'.format(Base.connection.url, organization_id, advertiser_id, creative_id)
        method = 'GET'
        response = self._execute(method, url, '')
        json_response = json.loads(response.text)
        data = json_response['thirdPartyVideoCreative']
        new_obj = self.__class__(Base.connection)
        new_obj.import_props(data)

        return new_obj
        

    def get_create_url(self):
        return '{0}/video-management/v4/organizations/{1}/creatives'.format(Base.connection.url, self.get('organization_id'))

    def get_creatives_by_advertiser(self, organization_id, advertiser_id):
        url = '{0}/video-management/v2/organizations/{1}/advertisers/{2}/creatives'.format(Base.connection.url, organization_id, advertiser_id)
        method = 'GET'
        response = self._execute(method, url, '')
        return self._get_third_party_creative_response_objects(response)

    def get_creatives_by_tactic(self, organization_id, advertiser_id, campaign_id, tactic_id):
        url = '{0}/video-management/v3/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/creativeflights'.format(Base.connection.url, organization_id, advertiser_id, campaign_id, tactic_id)
        method = 'GET'
        response = self._execute(method, url, '')
        return self._get_third_party_creative_response_objects(response)

    # add for THIRD PARTY VIDEO CREATIVES
    def _get_third_party_creative_response_objects(self, response):
        rval = []
        json_response = None
        if response.status_code == 200:
            json_response = json.loads(response.text)
        else:
            print response.text
            raise Exception("Bad response code {0}".format(response.text))

        obj_list = []
        if 'data' in json_response:
            for key, value in json_response['data'].iteritems():
                obj_list = obj_list + value

        for obj in obj_list:
            new_obj = self.__class__(Base.connection)
            new_obj.import_props(obj)
            rval.append(new_obj)

        return rval

    def create_creatives_by_advertiser(self, organization_id, advertiser_id):
        url = '{0}/video-management/v2/organizations/{1}/advertisers/{2}/creatives'.format(Base.connection.url, organization_id, advertiser_id)
        method = 'POST'
        response = self._execute(method, url, json.dumps(self.export_props()))
        obj = self._get_response_object(response)
        self.import_props(obj)
        return self.getId()
