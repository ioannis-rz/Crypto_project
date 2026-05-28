# Generate a self-signed certificate
import datetime
from OpenSSL import crypto

def generate_self_signed_certificate(private_key_path, certificate_request_path, output_cert_path):

    with open(private_key_path, 'rb') as f:
        key_bytes = f.read()
    with open(certificate_request_path, 'rb') as f:
        csr_bytes = f.read()

    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key_bytes)
    csr = crypto.load_certificate_request(crypto.FILETYPE_PEM, csr_bytes)

    cert = crypto.X509()
    cert.set_version(2)
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # 1 año
    cert.set_subject(csr.get_subject())
    cert.set_issuer(csr.get_subject())  # self-signed: issuer == subject
    cert.set_pubkey(csr.get_pubkey())

    cert.sign(pkey, 'sha256')

    with open(output_cert_path, 'wb') as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

generate_self_signed_certificate('private_key.pem', 'certificate_request.pem', 'self_signed_certificate.pem')