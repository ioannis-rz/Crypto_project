```markdown
# Crypto Project

Proyecto de ejemplo para una aplicación Flask con estadísticas de usuario y progreso académico.

## Requisitos

- Python 3.8 o superior
- `pip` instalado
- Linux / macOS / Windows

## Instalar dependencias

```bash
pip install Flask Flask-Limiter Flask-SSLify cryptography SQLAlchemy
```

## Configuración

La aplicación requiere la variable de entorno `PASSWORD_PEPPER`:

```bash
export PASSWORD_PEPPER="tu_valor_secreto"
```

En PowerShell:

```powershell
$env:PASSWORD_PEPPER="tu_valor_secreto"
```

## Generar certificados TLS

Si no tienes private_key.pem y certificate_request.pem, puedes generar tu certificado autofirmado con:

```bash
openssl genrsa -out private_key.pem 2048
openssl req -new -key private_key.pem -out certificate_request.pem
python scripts/generate_certificates.py
```

Esto crea self_signed_certificate.pem.

## Ejecutar la aplicación

```bash
python app.py
```

La aplicación se ejecutará en HTTPS usando:

- self_signed_certificate.pem
- private_key.pem
