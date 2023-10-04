import requests
import attr
from typing import Dict, Union
import ssl
import httpx
import urllib.parse
from PIL import Image
import io

@attr.s(auto_attribs=True)
class MinimalWrapper:
    """Minimalistic reference implementation for wrapping the SimpleSlideInterface of 3DHISTECH Ltd."""

    base_url: str
    raise_for_status: bool = attr.ib(False, kw_only=True)
    cookies: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    headers: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    timeout: float = attr.ib(5.0, kw_only=True)
    verify_ssl: Union[str, bool, ssl.SSLContext] = attr.ib(True, kw_only=True)
    session: requests.session = attr.field(init=False, default=requests.session())

    def get_headers(self) -> Dict[str, str]:
        """Gets headers to be used in all endpoints."""
        return {**self.headers}

    def with_headers(self, headers: Dict[str, str]) -> "MinimalWrapper":
        """Gets a new client matching this one with additional headers."""
        return attr.evolve(self, headers={**self.headers, **headers})

    def get_cookies(self) -> Dict[str, str]:
        return {**self.cookies}

    def with_cookies(self, cookies: Dict[str, str]) -> "MinimalWrapper":
        """Gets a new client matching this one with additional cookies."""
        return attr.evolve(self, cookies={**self.cookies, **cookies})

    def get_timeout(self) -> float:
        return self.timeout

    def with_timeout(self, timeout: float) -> "MinimalWrapper":
        """Gets a new client matching this one with a new timeout (in seconds)."""
        return attr.evolve(self, timeout=timeout)

    def check_status(self, resp):
        """Checks the status of a response and raises exception in case of error.
        It can be switched on with the raise_for_status parameter.
        """
        if self.raise_for_status:
            try:
                resp.raise_for_status()
            except requests.exceptions.HTTPError as err:
                raise requests.exceptions.HTTPError(str(err) + '\n' + 'Response: ' + resp.text, response=resp) from None

    def generate_url(self, url_path: str, *args):
        """Generates a formatted URL from a template and arguments."""
        args_enc = [urllib.parse.quote(a) for a in args]
        url_path = url_path.format(*args_enc)
        return self.base_url.rstrip('/') + '/api/simpleslideinterface/v1/' + url_path

    def get(self, url_path: str, *args, **kwargs):
        """Makes a GET request to Simple Slide Interface and returns the response."""
        resp = self.session.get(self.generate_url(url_path, *args), params=kwargs, verify=self.verify_ssl)
        self.check_status(resp)
        return resp

    def get_stream(self, url_path: str, *args, **kwargs):
        """Makes a GET request to Simple Slide Interface and returns the response in a stream."""
        resp = self.session.get(self.generate_url(url_path, *args), params=kwargs, verify=self.verify_ssl, stream=True)
        self.check_status(resp)
        return resp

    def get_image(self, url_path: str, *args, **kwargs):
        """Makes a GET request to Simple Slide Interface and returns the response in an image."""
        raw = self.get_stream(url_path, *args, **kwargs).raw.read()
        return Image.open(io.BytesIO(raw))
    
    def post(self, url_path: str, *args, json_body="", **kwargs):
        """Makes a POST request to Simple Slide Interface and returns the response."""
        resp = self.session.post(self.generate_url(url_path, *args), params=kwargs, json=json_body, verify=self.verify_ssl)
        self.check_status(resp)
        return resp
    
    def delete(self, url_path: str, *args, json_body="", **kwargs):
        """Makes a DELETE request to Simple Slide Interface and returns the response."""
        resp = self.session.delete(self.generate_url(url_path, *args), params=kwargs, json=json_body, verify=self.verify_ssl)
        self.check_status(resp)
        return resp
