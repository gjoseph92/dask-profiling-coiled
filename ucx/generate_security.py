import sys
import distributed


security = distributed.Security.temporary()
sys.stdout.write(security.tls_client_cert)
sys.stdout.write(security.tls_client_key)
