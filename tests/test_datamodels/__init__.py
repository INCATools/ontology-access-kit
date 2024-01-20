import unittest
from typing import Any, List, Type, Union

from oaklib import BasicOntologyInterface
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.io.streaming_json_writer import StreamingJsonWriter
from oaklib.io.streaming_writer import StreamingWriter


class AbstractDatamodelTestCase(unittest.TestCase):
    writer_types = [StreamingJsonWriter, StreamingCsvWriter]

    def attempt_streaming_writers(
        self,
        objs: List[Any],
        writers: List[Union[StreamingWriter, Type[StreamingWriter]]] = None,
        oi: BasicOntologyInterface = None,
        **kwargs,
    ):
        """
        Run a set of streaming writers on a set of objects

        :param objs:
        :param writer_types:
        :param kwargs:
        :return:
        """
        if writers is None:
            writers = self.writer_types
        for writer in writers:
            if not isinstance(writer, StreamingWriter):
                writer = writer(**kwargs)
                writer.ontology_interface = oi
            for obj in objs:
                writer.emit(obj)
            writer.finish()
