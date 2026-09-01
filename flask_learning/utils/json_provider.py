try:
    import orjson

    USE_ORJSON = True
except ModuleNotFoundError:
    USE_ORJSON = False
try:
    import ujson

    USE_UJSON = True
except ImportError:
    USE_UJSON = False

from flask.json.provider import DefaultJSONProvider, JSONProvider

if USE_ORJSON:

    class ORJSONProvider(JSONProvider):
        option = orjson.OPT_INDENT_2

        def dumps(self, obj, **kwargs):
            return orjson.dumps(obj, option=self.option).decode()

        def loads(self, s, **kwargs):
            return orjson.loads(s)

else:
    ORJSONProvider = DefaultJSONProvider

if USE_UJSON:

    class UJSONProvider(JSONProvider):
        encode_html_chars = False
        ensure_ascii = False
        indent = 4

        def dumps(self, obj, **kwargs):
            option = {
                "encode_html_chars": self.encode_html_chars,
                "ensure_ascii": self.ensure_ascii,
                "indent": self.indent,
            }
            return ujson.dumps(obj, **option)

        def loads(self, s, **kwargs):
            return ujson.loads(s)

else:
    UJSONProvider = DefaultJSONProvider
