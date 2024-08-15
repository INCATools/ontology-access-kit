import logging
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.introspection import package_schemaview

import oaklib.datamodels.validation_datamodel as vdm
from tests import output_path


class TestValidationDatamodel(unittest.TestCase):
    def test_create(self):
        """
        Tests the creation of an example instance of reports
        """
        severity = vdm.SeverityOptions(vdm.SeverityOptions.ERROR)
        r1 = vdm.ValidationResult(subject="FOO:1", type="sh:Test", severity=severity)
        logging.info(type(r1.severity))
        vr = vdm.ValidationReport(results=[r1])
        yaml_dumper.dump(vr, output_path("validation_report.vdm.yaml"))
        op1 = vdm.RepairOperation(repairs=r1, modified=True)
        rr = vdm.RepairReport(results=[op1])
        yaml_dumper.dump(rr, output_path("repair_report.vdm.yaml"))

    def test_introspect(self):
        """
        Tests ability to introspect the schema and examine the schema elements
        """
        sv = package_schemaview(vdm.__name__)
        assert "severity" in sv.all_slots()
        assert "ValidationResult" in sv.all_classes()
