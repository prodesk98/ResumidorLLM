from typing import Optional

import requests
from requests import HTTPError

from config import SERPBASE_API_KEY
from exceptions import SerpbaseSearchError
from researchers.base import BaseSearchService
from schemas import SearchResult


class SerpbaseSearch(BaseSearchService):
    """SerpBase Google Search API — returns structured Google search results via REST API."""

    BASE_URL = "https://api.serpbase.dev/google/search"

    def __init__(self, **kwargs):
        self._params = kwargs
        if not SERPBASE_API_KEY:
            raise ValueError("SERPBASE_API_KEY not found in environment variables.")

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """
        Perform a Google search using the SerpBase API.

        :param query: The search query.
        :param limit: Maximum number of results to return.
        :return: A list of SearchResult objects.
        """
        try:
            response = requests.get(
                self.BASE_URL,
                params={
                    "q": query,
                    "num": min(limit, 100),
                    "api_key": SERPBASE_API_KEY,
                    **self._params,
                },
                timeout=30,
            )
            response.raise_for_status()

            data = response.json()
            organic_results = data.get("organic_results", [])

            return [
                SearchResult(
                    title=result.get("title", ""),
                    description=result.get("snippet", ""),
                    link=result.get("link", ""),
                )
                for result in organic_results[:limit]
            ]

        except HTTPError as e:
            raise SerpbaseSearchError(
                f"Failed to fetch results from SerpBase API: {e}"
            )
        except Exception as e:
            raise SerpbaseSearchError(
                f"An unexpected error occurred: {e}"
            )
