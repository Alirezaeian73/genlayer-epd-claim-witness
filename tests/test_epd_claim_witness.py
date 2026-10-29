import json
from pathlib import Path

import pytest


CONTRACT_PATH = Path(__file__).parents[1] / "contracts" / "epd_claim_witness.py"
PAGE_URL_PATTERN = r"www\.environdec\.com/library/epd33463"
PDF_URL_PATTERN = r"api\.prod\.environdec\.com/api/v1/EPDLibrary/Files/EPDs"
PDF_URL = "https://api.prod.environdec.com/api/v1/EPDLibrary/Files/EPDs/00000000-0000-0000-0000-000000000001/Documents"

PDF_TEXT = """Environmental Product Declaration
Product name: CLS Rck35 S4 XC2 D25 CEM III 42,5 N-LH/SR CAM
Declared Unit: 1 m3
INDICATOR | UNITS | A1-A3
GWP – TOTAL | kg CO2 eq. | 1,57 E+02
"""

EXTRACTION = {
    "product_name": "CLS Rck35 S4 XC2 D25 CEM III 42,5 N-LH/SR CAM",
    "product_quote": "CLS Rck35 S4 XC2 D25 CEM III 42,5 N-LH/SR CAM",
    "declared_unit": "1 m3",
    "declared_unit_quote": "Declared Unit: 1 m3",
    "indicator": "GWP – TOTAL",
    "indicator_quote": "GWP – TOTAL",
    "module": "A1-A3",
    "module_quote": "A1-A3",
    "raw_value": "1,57 E+02",
    "value_quote": "1,57 E+02",
}


@pytest.fixture
def contract(direct_vm, direct_deploy):
    direct_vm.mock_web(
        PAGE_URL_PATTERN,
        {
            "status": 200,
            "body": 'EPD-IES-0033463:001 <a href="' + PDF_URL + '">Download EPD</a>',
        },
    )
    direct_vm.mock_web(
        PDF_URL_PATTERN,
        {"status": 200, "body": PDF_TEXT},
    )
    direct_vm.mock_llm(
        r"Extract facts from the Environmental Product Declaration text below",
        json.dumps(EXTRACTION),
    )
    return direct_deploy(str(CONTRACT_PATH))


def read_assessment(contract, assessment_id):
    return json.loads(contract.get_assessment(assessment_id))


def test_exact_epd_claim_is_supported(contract):
    assessment_id = contract.assess(
        "EPD-IES-0033463:001",
        "CLS Rck35 S4 XC2 D25 CEM III 42,5 N-LH/SR CAM",
        "1 m3",
        "157",
    )

    record = read_assessment(contract, assessment_id)
    assert record["status"] == "SUPPORTED"
    assert record["source_value"] == "1,57 E+02"
    assert record["source_pdf_url"] == PDF_URL
    assert len(record["rendered_text_sha256"]) == 64
    assert contract.get_assessment_count() == 1


def test_different_value_is_contradicted_only_for_matching_scope(contract):
    assessment_id = contract.assess(
        "EPD-IES-0033463:001",
        "CLS Rck35 S4 XC2 D25 CEM III 42,5 N-LH/SR CAM",
        "1 m3",
        "158",
    )

    assert read_assessment(contract, assessment_id)["status"] == "CONTRADICTED"


def test_wrong_product_is_unclear_not_a_false_claim(contract):
    assessment_id = contract.assess(
        "EPD-IES-0033463:001",
        "A different concrete product",
        "1 m3",
        "157",
    )

    assert read_assessment(contract, assessment_id)["status"] == "UNCLEAR"


def test_invalid_registration_number_reverts_before_web_access(direct_vm, direct_deploy):
    contract = direct_deploy(str(CONTRACT_PATH))

    with direct_vm.expect_revert():
        contract.assess("not-an-epd-id", "Product", "1 m3", "157")

    assert contract.get_assessment_count() == 0


def test_requested_version_must_match_the_published_version(contract):
    assessment_id = contract.assess(
        "EPD-IES-0033463:002",
        "CLS Rck35 S4 XC2 D25 CEM III 42,5 N-LH/SR CAM",
        "1 m3",
        "157",
    )

    record = read_assessment(contract, assessment_id)
    assert record["status"] == "UNCLEAR"
    assert record["source_pdf_url"] == ""


def test_wrong_declared_unit_is_unclear(contract):
    assessment_id = contract.assess(
        "EPD-IES-0033463:001",
        "CLS Rck35 S4 XC2 D25 CEM III 42,5 N-LH/SR CAM",
        "1 kg",
        "157",
    )

    assert read_assessment(contract, assessment_id)["status"] == "UNCLEAR"


def test_missing_official_page_is_source_unavailable(direct_vm, direct_deploy):
    direct_vm.mock_web(PAGE_URL_PATTERN, {"status": 404, "body": ""})
    contract = direct_deploy(str(CONTRACT_PATH))

    assessment_id = contract.assess(
        "EPD-IES-0033463:001",
        "CLS Rck35 S4 XC2 D25 CEM III 42,5 N-LH/SR CAM",
        "1 m3",
        "157",
    )

    record = read_assessment(contract, assessment_id)
    assert record["status"] == "SOURCE_UNAVAILABLE"
    assert record["source_pdf_url"] == ""


def test_malformed_extraction_is_unclear_not_source_unavailable(direct_vm, direct_deploy):
    direct_vm.mock_web(
        PAGE_URL_PATTERN,
        {"status": 200, "body": 'EPD-IES-0033463:001 <a href="' + PDF_URL + '">Download EPD</a>'},
    )
    direct_vm.mock_web(PDF_URL_PATTERN, {"status": 200, "body": PDF_TEXT})
    direct_vm.mock_llm(
        r"Extract facts from the Environmental Product Declaration text below",
        "not-json",
    )
    contract = direct_deploy(str(CONTRACT_PATH))

    assessment_id = contract.assess(
        "EPD-IES-0033463:001",
        "CLS Rck35 S4 XC2 D25 CEM III 42,5 N-LH/SR CAM",
        "1 m3",
        "157",
    )

    assert read_assessment(contract, assessment_id)["status"] == "UNCLEAR"
