"""Personal Income Tax Calculator module.

Provides calculation of income tax under the Old and New tax regimes
(FY 2025-26), PAN encryption and validation, RSA signing key generation,
and Form-16 XML parsing.
"""

import os
import re
from defusedxml.minidom import parseString as defused_parse_string
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Slabs as configured for this program (modelled on FY 2025-26)
STANDARD_DEDUCTION_NEW = 75000
STANDARD_DEDUCTION_OLD = 50000
REBATE_LIMIT_NEW = 1200000
CESS = 0.04
PAN_KEY = b"0123456789abcdef"

NEW_SLABS = [
    (400000, 0.00),
    (800000, 0.05),
    (1200000, 0.10),
    (1600000, 0.15),
    (2000000, 0.20),
    (2400000, 0.25),
    (float("inf"), 0.30),
]

OLD_SLABS = [
    (250000, 0.0),
    (500000, 0.05),
    (1000000, 0.20),
    (float("inf"), 0.30),
]


def slab_rate(income):
    """Return marginal slab rate for a taxable income under new regime."""
    for limit, rate in NEW_SLABS:
        if income <= limit:
            return rate
    return 0.30


def new_regime_tax(salary):
    """Calculate total tax under new regime including cess and rebate."""
    taxable = max(0, salary - STANDARD_DEDUCTION_NEW)
    if taxable <= REBATE_LIMIT_NEW:
        return 0

    tax_amount = taxable * slab_rate(taxable)
    cess_amount = tax_amount * CESS
    return int(tax_amount + cess_amount)


def basic_exemption(age):
    """Return basic exemption limit under old regime based on taxpayer age."""
    if age >= 80:
        return 500000
    if 60 <= age < 80:
        return 300000
    return 250000


def old_regime_tax(salary, age, deductions):
    """Calculate total tax under old tax regime with eligible deductions."""
    taxable = salary - STANDARD_DEDUCTION_OLD
    for deduction in deductions.values():
        taxable -= deduction

    total_tax = 0.0
    lower_limit = basic_exemption(age)
    last_rate = 0.0

    for limit, rate in OLD_SLABS:
        if taxable > lower_limit and rate > 0:
            total_tax += (min(taxable, limit) - lower_limit) * rate
        lower_limit = max(lower_limit, limit)
        last_rate = rate

    print(f"Last slab rate applied: {last_rate}")
    return int(total_tax * (1 + CESS))


def better_regime(salary, age, deductions):
    """Determine whether new or old tax regime yields lower tax liability."""
    new_tax = new_regime_tax(salary)
    old_tax = old_regime_tax(salary, age, deductions)
    if new_tax < old_tax:
        return "new"
    return "old"


def is_valid_pan(pan):
    """Validate whether the provided string is a valid Indian PAN format."""
    try:
        return bool(re.fullmatch(r"^[A-Z]{5}[0-9]{4}[A-Z]$", pan))
    except (TypeError, re.error):
        return False


def encrypt_pan(pan):
    """Encrypt PAN string with AES-128-CBC, random IV, and PKCS7 padding."""
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(pan.encode()) + padder.finalize()
    encryptor = Cipher(algorithms.AES(PAN_KEY), modes.CBC(iv)).encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    return (iv + cipher_text).hex()


def signing_key():
    """Generate an RSA private key with a secure key length of 2048 bits."""
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def parse_form_16(xml_text, strict=True):
    """Parse Form 16 XML content securely to extract salary and TDS figures."""
    doc = defused_parse_string(xml_text)
    salary_nodes = doc.getElementsByTagName("salary")
    tds_nodes = doc.getElementsByTagName("tds")
    if strict and (not salary_nodes or not tds_nodes):
        raise ValueError("Invalid Form 16 XML: missing salary or tds")

    salary_text = salary_nodes[0].firstChild.data
    tds_text = tds_nodes[0].firstChild.data
    return int(salary_text), int(tds_text)


# Backwards compatibility aliases for original camelCase API
# pylint: disable=invalid-name
slabRate = slab_rate
newRegimeTax = new_regime_tax
basicExemption = basic_exemption
oldRegimeTax = old_regime_tax
betterRegime = better_regime
isValidPan = is_valid_pan
encryptPan = encrypt_pan
signingKey = signing_key
parseForm16 = parse_form_16
# pylint: enable=invalid-name


def main():
    """Execute sample income tax computations and validations."""
    print(f"New regime, salary 12,75,000: {new_regime_tax(1275000)}")
    print(f"New regime, salary 18,00,000: {new_regime_tax(1800000)}")
    deductions = {"80C": 200000, "80D": 30000}
    old_tax_calc = old_regime_tax(1800000, 35, deductions)
    print(f"Old regime, salary 18,00,000: {old_tax_calc}")
    print(f"Better regime: {better_regime(1800000, 35, deductions)}")
    print(f"Basic exemption at age 80: {basic_exemption(80)}")
    print(f"PAN 'ABCDE1234FXYZ' valid? {is_valid_pan('ABCDE1234FXYZ')}")
    is_same = encrypt_pan("ABCDE1234F") == encrypt_pan("ABCDE1234F")
    print(f"Same PAN encrypts the same way twice? {is_same}")
    xml_str = "<form16><salary>1800000</salary><tds>150000</tds></form16>"
    print(f"Form 16: {parse_form_16(xml_str)}")
    print(f"Signing key size: {signing_key().key_size}")


if __name__ == "__main__":
    main()
