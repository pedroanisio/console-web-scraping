import uuid
from urllib.parse import urlparse

class URLBasedUUIDGenerator:
    def __init__(self, namespace=uuid.NAMESPACE_URL):
        self.namespace = namespace

    def extract_domain(self, url: str) -> str:
        """
        Extract the domain with TLD from the URL.
        
        Args:
            url (str): The URL to extract the domain from.
        
        Returns:
            str: The extracted domain with TLD.
        """
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        parts = domain.split('.')
        if len(parts) > 2:
            domain = '.'.join(parts[-2:])
        return domain

    def get_uuid(self, url: str) -> str:
        """
        Generate a UUID based on the provided URL.
        
        Args:
            url (str): The URL to generate a UUID for.
        
        Returns:
            str: The generated UUID as a string.
        """
        domain_with_tld = self.extract_domain(url)
        return str(uuid.uuid5(self.namespace, domain_with_tld))
