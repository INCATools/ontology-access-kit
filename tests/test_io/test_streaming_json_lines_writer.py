import io
import json
import unittest

from oaklib.datamodels.obograph import Node
from oaklib.io.streaming_json_lines_writer import StreamingJsonLinesWriter


class TestStreamingJsonLinesWriter(unittest.TestCase):
    def setUp(self):
        self.file = io.StringIO()
        self.writer = StreamingJsonLinesWriter(file=self.file)

    def lines(self):
        return self.file.getvalue().splitlines()

    def test_emit_dict(self):
        self.writer.emit({"id": "X:1", "label": "héllo"})
        self.writer.emit_dict({"id": "X:2"})
        self.assertEqual(['{"id": "X:1", "label": "héllo"}', '{"id": "X:2"}'], self.lines())

    def test_emit_object(self):
        self.writer.emit(Node(id="X:1", lbl="héllo"))
        self.writer.emit(Node(id="X:2"))
        lines = self.lines()
        self.assertEqual(2, len(lines))
        self.assertEqual("X:1", json.loads(lines[0])["id"])
        self.assertEqual("héllo", json.loads(lines[0])["lbl"])
        self.assertEqual("X:2", json.loads(lines[1])["id"])
