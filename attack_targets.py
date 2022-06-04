import pwn
import requests
import ipaddress
from xml.etree import ElementTree
from json import loads
from enum import Enum


class Target:
    """
    Base Target. Provides the address of the target host
    """
    ipv4_addr: ipaddress.IPv4Address
    _port: int

    def __init__(self, address, port):
        self.ipv4_addr = ipaddress.ip_address(address)
        self._port = port

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_host_str(self):
        return f"{str(self.ipv4_addr)}:{self._port}"

    def address(self):
        return str(self.ipv4_addr)

    def port(self):
        return self._port


class PostTarget(Target):
    """
    provides the response from a post request to the attack function. the attack function can then extract the flag
    from the response
    """
    response: requests.Response
    request_params: tuple[dict, dict]
    url = str
    use_https: bool
    headers = {}

    class EncodingType(Enum):
        XML = 0
        JSON = 1
        URL = 2

    encoding: EncodingType

    def __init__(self, address, port):
        super().__init__(address, port)

    def __enter__(self):
        data, kwargs = self.request_params

        if self.encoding == PostTarget.EncodingType.URL:
            if "headers" in kwargs:
                kwargs["headers"]["Content-Type"] = "application/x-www-form-urlencoded"
                kwargs["headers"]["accept"] = "*/*"
            else:
                kwargs["headers"] = {"Content-Type": "application/x-www-form-urlencoded"}
                kwargs["headers"]["accept"] = "*/*"
            self.response = requests.post(f"{'https' if self.use_https else 'http'}://{self.get_host_str()}/{self.url}",
                                          data=data,
                                          verify=False, **kwargs)

        elif self.encoding == PostTarget.EncodingType.JSON:
            if "headers" in kwargs:
                kwargs["headers"]["Content-Type"] = "application/json"
                kwargs["headers"]["accept"] = "*/*"
            else:
                kwargs["headers"] = {"Content-Type": "application/json"}
                kwargs["headers"]["accept"] = "*/*"

            self.response = requests.post(f"{'https' if self.use_https else 'http'}://{self.get_host_str()}/{self.url}",
                                          json=data,
                                          verify=False, **kwargs)

        else:
            if "headers" in kwargs:
                kwargs["headers"]["Content-Type"] = "text/xml"
                kwargs["headers"]["accept"] = "*/*"
            else:
                kwargs["headers"] = {"Content-Type": "text/xml"}
                kwargs["headers"]["accept"] = "*/*"

            self.response = requests.post(f"{'https' if self.use_https else 'http'}://{self.get_host_str()}/{self.url}",
                                          data=data,
                                          verify=False, **kwargs)

        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super().__exit__(exc_type, exc_val, exc_tb)

    @staticmethod
    def url_encoded(address: str, port: int, url: str, data: dict, https=False, **kwargs):
        target = PostTarget(address, port)
        target.url = url
        target.use_https = https

        target.request_params = (data, kwargs)
        target.encoding = PostTarget.EncodingType.URL
        return target

    @staticmethod
    def many_url(port: int, url: str, data: dict, https=False, **kwargs):
        def __inner(addresses: list[str]):
            return [PostTarget.url_encoded(addr, port, url, data, https, **kwargs) for addr in addresses]

    @staticmethod
    def json_encoded(address: str, port: int, url: str, data: dict, https=False, **kwargs):
        target = PostTarget(address, port)
        target.url = url
        target.use_https = https

        target.request_params = (data, kwargs)
        target.encoding = PostTarget.EncodingType.JSON
        return target

    @staticmethod
    def many_json(port: int, url: str, data: dict, https=False, **kwargs):
        def __inner(addresses: list[str]):
            return [PostTarget.json_encoded(addr, port, url, data, https, **kwargs) for addr in addresses]

    @staticmethod
    def xml_encoded(address: str, port: int, url: str, data: dict, https=False, **kwargs):
        target = PostTarget(address, port)
        target.url = url
        target.use_https = https

        target.request_params = (data, kwargs)
        target.encoding = PostTarget.EncodingType.XML
        return target

    @staticmethod
    def many_xml(port: int, url: str, data: dict, https=False, **kwargs):
        def __inner(addresses: list[str]):
            return [PostTarget.xml_encoded(addr, port, url, data, https, **kwargs) for addr in addresses]

    def json_response(self):
        return loads(self.response.text)

    def xml_response(self):
        return ElementTree.fromstring(self.response.text)

    def text_response(self):
        return self.response.text


class GetTarget(Target):
    """
    provides the response from a get request to the attack function. the attack function can then extract the flag
    from the response
    """
    response: requests.Response
    request_params: tuple[dict, dict]
    url = str
    use_https: bool

    def __init__(self, address, port):
        super().__init__(address, port)

    @staticmethod
    def get(address: str, port: int, url: str, params: dict, https=False, **kwargs):
        target = GetTarget(address, port)
        target.url = url
        target.use_https = https

        target.request_params = (params, kwargs)
        return target

    @staticmethod
    def many(port: int, url: str, params: dict, https=False, **kwargs):
        def __inner(addresses: list[str]):
            return [GetTarget.get(addr, port, url, params, https, **kwargs) for addr in addresses]

    def __enter__(self):
        params, kwargs = self.request_params

        if params:
            self.response = requests.get(f"{'https' if self.use_https else 'http'}://{self.get_host_str()}/{self.url}",
                                         params,
                                         verify=False, **kwargs)
        else:
            self.response = requests.get(f"{'https' if self.use_https else 'http'}://{self.get_host_str()}/{self.url}",
                                         verify=False, **kwargs)

        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super().__exit__(exc_type, exc_val, exc_tb)

    def json(self):
        """
        The attacks' response body decoded as json
        :return: Json Object of the response
        """
        return self.response.json()

    def text(self):
        """
        The attacks' response body as text
        :return: Text representation of the respnse
        """
        return self.response.text

    def xml(self):
        """
        The attacks' response decoded as xml
        :return: XML Object of the response
        """
        return ElementTree.fromstring(self.response.content)

    def headers(self):
        """
        The attacks' response headers
        :return: Headers dict of the respnse
        """
        return self.response.headers


class RemoteTarget(Target):
    remote: pwn.remote

    def __init__(self, address, port):
        super().__init__(address, port)

    @staticmethod
    def remote(address, port):
        return RemoteTarget(address, port)

    @staticmethod
    def many(port):
        def __inner(addresses: list[str]):
            return [RemoteTarget.remote(addr, port) for addr in addresses]

    def __enter__(self):
        self.remote = pwn.remote(self.address(), self.port())
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remote.close()
        return super().__exit__(exc_type, exc_val, exc_tb)


def ip_range(a, b, c, lower, upper):
    if lower <= upper:
        return [f"{a}.{b}.{c}.{i}" for i in range(lower, upper + 1)]
