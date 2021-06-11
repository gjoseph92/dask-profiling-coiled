import sys
import distributed


def write_cert_key(path: str):
    security = distributed.Security.temporary()
    with open(path, "w") as f:
        f.write(security.tls_client_cert)
        f.write(security.tls_client_key)


if __name__ == "__main__":
    write_cert_key(sys.argv[1])
