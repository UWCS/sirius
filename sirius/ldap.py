import ldap3
import hashlib
import os
import base64

LDAP_URL = ""
LDAP_PORT = 12
LDAP_USER = ""
LDAP_PASSWORD = ""


def connect() -> ldap3.Connection:
    """
    Create a connection to the LDAP server
    """
    ldap_server = ldap3.Server(LDAP_URL, LDAP_PORT)

    conn = ldap3.Connection(
        ldap_server,
        user=LDAP_USER,
        password=LDAP_PASSWORD,
        client_strategy=ldap3.SYNC,
        authentication=ldap3.SIMPLE,
    )
    conn.bind()

    return conn


def check_password(tagged_digest_salt: bytes, password: str):
    """
    Checks the OpenLDAP tagged digest against the given password
    """
    # the entire payload is base64-encoded

    # strip off the hash label
    digest_salt_b64 = tagged_digest_salt[6:]

    # the password+salt buffer is also base64-encoded.  decode and split the
    # digest and salt
    digest_salt = base64.decodebytes(digest_salt_b64)
    digest = digest_salt[:20]
    salt = digest_salt[20:]

    sha = hashlib.sha1(password.encode())
    sha.update(salt)

    return digest == sha.digest()


def make_secret(password: str):
    """
    Encodes the given password as a base64 SSHA hash+salt buffer
    """
    salt = os.urandom(4)

    # hash the password and append the salt
    sha = hashlib.sha1(password.encode())
    sha.update(salt)

    # create a base64 encoded string of the concatenated digest + salt
    digest_salt_b64 = "{}{}".format(sha.digest(), salt).encode("base64").strip()

    # now tag the digest above with the {SSHA} tag
    tagged_digest_salt = "{{SSHA}}{}".format(digest_salt_b64)

    return tagged_digest_salt


def get_uid_number(conn: ldap3.Connection) -> int:
    conn.search(
        "ou=people,dc=internal,dc=uwcs,dc=co,dc=uk",
        "(&(objectClass=posixAccount)(uidNumber>=10000))",
    )
    return 100001 + 1 + len(conn.entries())


def create_ldap_user(
    username: str,
    password: str,
    email: str,
    first_name: str,
    last_name: str,
    is_member: bool,
) -> bool:

    conn = connect()

    # Search for the user on LDAP
    search_string_user = f"uid={username},ou=people,dc=internal,dc=uwcs,dc=co,dc=uk"
    conn.search(
        search_string_user, "(objectClass=posixUser)", attributes=ldap3.ALL_ATTRIBUTES
    )
    user_search = conn.response

    if user_search:
        # user already exists
        return False

    # create user
    password_hashed = make_secret(password)

    id_number = get_uid_number(conn)

    group_add_dn = f"cn={username},ou=groups,dc=internal,dc=uwcs,dc=co,dc=uk"

    group_attributes_dict = {
        "objectClass": ["posixGroup"],
        "cn": [username],
        "gidNumber": [id_number],
    }

    conn.add(group_add_dn, attributes=group_attributes_dict)

    user_add_dn = f"uid={username},ou=people,dc=uwcs,dc=co,dc=uk"

    user_attributes_dict = {
        "objectClass": ["posixAccount", "organizationalPerson", "inetOrgPerson"],
        "cn": [first_name],
        "gidNumber": [id_number],
        "uid": [username],
        "uidNumber": [id_number],
        "homeDirectory": [f"/home/{username}"],
        "loginShell": ["/bin/bash"],
        "userPassword": [password_hashed],
    }

    conn.add(user_add_dn, attributes=user_attributes_dict)

    return True
