import logging
import traceback

from opencensus.trace import attributes_helper, integrations, utils
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.types import ASGIApp

HTTP_HOST = attributes_helper.COMMON_ATTRIBUTES["HTTP_HOST"]
HTTP_METHOD = attributes_helper.COMMON_ATTRIBUTES["HTTP_METHOD"]
HTTP_PATH = attributes_helper.COMMON_ATTRIBUTES["HTTP_PATH"]
HTTP_ROUTE = attributes_helper.COMMON_ATTRIBUTES["HTTP_ROUTE"]
HTTP_URL = attributes_helper.COMMON_ATTRIBUTES["HTTP_URL"]
HTTP_STATUS_CODE = attributes_helper.COMMON_ATTRIBUTES["HTTP_STATUS_CODE"]
ERROR_MESSAGE = attributes_helper.COMMON_ATTRIBUTES["ERROR_MESSAGE"]
ERROR_NAME = attributes_helper.COMMON_ATTRIBUTES["ERROR_NAME"]
STACKTRACE = attributes_helper.COMMON_ATTRIBUTES["STACKTRACE"]


class AppInsightsMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp, excludelist_paths=None, excludelist_hostnames=None
    ) -> None:
        super().__init__(app)
        self.excludelist_paths = excludelist_paths
        self.excludelist_hostnames = excludelist_hostnames
        integrations.add_integration(integrations._Integrations.FASTAPI)

    def _before_request(self, span: dict, request: Request):
        span["name"] = f"[{request.method}] {request.url.path}"
        span["properties"] = {}
        span["properties"][HTTP_HOST] = request.url.hostname
        span["properties"][HTTP_METHOD] = request.method
        span["properties"][HTTP_PATH] = request.url.path
        span["properties"][HTTP_URL] = str(request.url)
        span["properties"][HTTP_ROUTE] = request.url.path

    def _after_request(self, span: dict, response: Response):
        span["properties"][HTTP_STATUS_CODE] = response.status_code

    def _handle_exception(self, span: dict, exception: Exception):
        span["properties"][HTTP_STATUS_CODE] = exception.__class__.__name__
        span["properties"][ERROR_MESSAGE] = str(exception)
        span["properties"][STACKTRACE] = "\n".join(
            traceback.format_tb(exception.__traceback__)
        )
        span["properties"][HTTP_STATUS_CODE] = HTTP_500_INTERNAL_SERVER_ERROR

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Do not trace if the url is in the exclude list
        if utils.disable_tracing_url(str(request.url), self.excludelist_paths):
            return await call_next(request)

        span = {}

        try:
            self._before_request(span, request)
        except Exception:  # pragma: NO COVER
            logging.error("Failed to trace request", exc_info=True)

        try:
            response = await call_next(request)
        except Exception as err:  # pragma: NO COVER
            try:
                self._handle_exception(span, err)
            except Exception:  # pragma: NO COVER
                logging.error("Failed to trace response", exc_info=True)
            raise err

        try:
            self._after_request(span, response)
        except Exception:  # pragma: NO COVER
            logging.error("Failed to trace response", exc_info=True)

        logging.info(span["name"], extra={"custom_dimensions": span["properties"]})

        return response
