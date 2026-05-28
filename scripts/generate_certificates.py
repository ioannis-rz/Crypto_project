from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
import datetime

# private_key.pem & certificate_request.pem can be generated with 
# openssl genrsa -out private_key.pem 
# openssl req -new -key private_key.pem -out certificate_request.pem
# on the terminal

def generate_self_signed_certificate(private_key_path, certificate_request_path, output_cert_path):
    with open(private_key_path, 'rb') as f:
        key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())
    with open(certificate_request_path, 'rb') as f:
        csr = x509.load_pem_x509_csr(f.read(), default_backend())

    builder = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(csr.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.UTC))
        .not_valid_after(datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=365))
    )

    for ext in csr.extensions:
        builder = builder.add_extension(ext.value, ext.critical)

    cert = builder.sign(private_key=key, algorithm=hashes.SHA3_256(), backend=default_backend())

    with open(output_cert_path, 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

generate_self_signed_certificate(
    './private_key.pem',
    './certificate_request.pem',
    './self_signed_certificate.pem'
)