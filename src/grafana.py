from influx import DBHTTPSetup


class GrafanaWrapper(DBHTTPSetup):
    """This class helpfs for the interaction with grafana"""

    def __init__(self):
        super().__init__(db='grafana')

    def register_datasource(self, uuid, password):
        parser = self.__get_parser__()
        ssl = 'http'
        if parser.get('influxdb', 'ssl') == 'True':
            ssl = 'https'
        body = "{\"name\":\"" + uuid + "\",\"type\":\"influxdb\",\"url\":\"" + ssl +"://" + \
               parser.get('grafana','influxdomain') + ":80"  +\
                "\",\"access\":\"direct\",\"isDefault\":true,\"database\":\"" + uuid + \
               "\",\"user\":\"" + uuid + "\",\"password\":\"" + password + "\"}"
        resp = self.__send_post_request__(body, 'datasources')
        return resp < 300

    def check_datasource(self, uuid):
        self.log.info('Check if datasource ' + uuid + ' exists')
        resp = self.__send_get_request__('datasources')
        body = str(resp)
        if body.find(uuid) >= 0:
            self.log.debug('Found database with uuid ' + uuid)
            return True
        self.log.debug('Did not find database with uuid ' + uuid)
        return False

    def __send_post_request__(self, body, endpoint):
        """This method sends a post request to the grafana instance"""
        self.log.info('Start post request for grafana with body ' + body)
        client = self.__conn_setup__()
        try:
            client.request("POST", "/api/" + endpoint, body, headers=self.__get_header__(content_type="application/json"))
            resp = client.getresponse()
            self.log.info('Post response is: ' + str(resp.status))

            iserror = str(resp.read().decode('utf-8'))
            self.log.debug(iserror)
            if resp.status >= 400:
                raise Exception
            if iserror.find('error') >= 0:
                raise Exception
            return resp.status
        except Exception as e :
            self.log.error('The POST Request did not succeed, Status: ')
            return 400


    def __send_get_request__(self,  endpoint):
        """This method sends a post request to the grafana instance"""
        self.log.info('Start get request for grafana on endpoint ' + endpoint)
        client = self.__conn_setup__()
        try:
            client.request("GET", "/api/" + endpoint,  headers=self.__get_header__(content_type="application/json"))
            resp = client.getresponse()
            self.log.info('Get response is: ' + str(resp.status))
            if resp.status >= 400:
                raise Exception
            iserror = str(resp.read().decode('utf-8'))
            self.log.debug(iserror)
            if iserror.find('error') >= 0:
                raise Exception
            return iserror
        except Exception as e:
            self.log.error('The GET Request did not succeed, Status: ')
            return 400
