import sys
from io import StringIO

import html2text
from qgis.core import QgsApplication
from werkzeug.exceptions import BadRequest

# Append the path where processing plugin can be found
sys.path.append("/usr/share/qgis/python/plugins")

import processing
from curve_number_generator.processing.curve_number_generator_provider import CurveNumberGeneratorProvider
from processing.core.Processing import Processing

## Init QGIS Processing
# See https://gis.stackexchange.com/a/155852/4972 for details about the prefix
QgsApplication.setPrefixPath("/usr", True)
qgs = QgsApplication([], False)
qgs.initQgis()

Processing.initialize()
provider = CurveNumberGeneratorProvider()
QgsApplication.processingRegistry().addProvider(provider)


def list_algorithms():
    algorithms = []
    for alg in QgsApplication.processingRegistry().algorithms():
        algorithms.append(
            {
                "provider_id": alg.id().partition(":")[0],
                "algorithm_id": alg.id().partition(":")[-1],
                "algorith_name": alg.displayName(),
            }
        )
    return algorithms


def get_alg_help(provider_id, algorithm_id):
    save_stdout = sys.stdout
    result = StringIO()
    sys.stdout = result
    str(processing.algorithmHelp(f"{provider_id}:{algorithm_id}"))
    sys.stdout = save_stdout
    h = html2text.HTML2Text()
    content = result.getvalue()
    content = content.replace("</html>", "<html>")
    content = content.split("<html>")
    # because of QGIS return str format we know the str would not start and end with html
    if len(content) > 1:
        content = content[0] + h.handle("\n".join(content[1:-1])) + content[-1]
    else:
        content = content[0]
    return content


def process_alg(provider_id, algorithm_id, data):

    data_str = str(data)
    if "TEMPORARY_OUTPUT" in data_str:
        raise BadRequest("'TEMPORARY_OUTPUT' is not allowed. Please provide a filepath for the output")

    result = processing.run(f"{provider_id}:{algorithm_id}", data)
    return result
