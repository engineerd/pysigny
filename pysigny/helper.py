import os
import shutil

from pathlib import Path
from typing import Dict

from securesystemslib.interface import (
    get_password,
    import_ecdsa_privatekey_from_file,
    import_ecdsa_publickey_from_file,
)

from tuf.repository_tool import (
    create_new_repository,
    generate_and_write_ecdsa_keypair,
)


DEFAULT_TRUST_DIR = Path.home().joinpath('.pysigny')
KEYSTORE_DIR = 'private'
METADATA_STAGED_DIR = 'metadata.staged'
METADATA_DIR = 'metadata'


def get_private_keypath(keystore_dir, rolename):
    return Path.joinpath(keystore_dir, rolename)


def get_public_keypath(private_keypath):
    # This is the reference implementation filename convention at the time of writing.
    return '{}.pub'.format(private_keypath)


def create_and_set_keys(keystore_dir, repo_obj):
    for rolename in ('root', 'timestamp', 'snapshot', 'targets'):
        passphrase = os.environ.get('{}_PASSPHRASE'.format(rolename.upper()))
        if not passphrase:
            passphrase = get_password(
                prompt='Enter password for {}: '.format(rolename),
                confirm=True
            )

        private_keypath = str(get_private_keypath(keystore_dir, rolename))
        public_keypath = get_public_keypath(private_keypath)

        generate_and_write_ecdsa_keypair(private_keypath, password=passphrase)

        private = import_ecdsa_privatekey_from_file(private_keypath, passphrase)
        public = import_ecdsa_publickey_from_file(public_keypath)

        role_obj = getattr(repo_obj, rolename)
        role_obj.load_signing_key(private)
        role_obj.add_verification_key(public)


def write_repo(repo_obj, metadata_staged_dir, metadata_dir):
    repo_obj.writeall()
    shutil.copytree(metadata_staged_dir, metadata_dir)


def create_subdir(repo_path, subdir):
    subdir = repo_path.joinpath(subdir)
    assert not Path.is_dir(subdir), f'{subdir} exists!'
    return subdir


def init_repo(trustdir, repo_name):
    repo_path = trustdir.joinpath(repo_name)
    keystore_dir = create_subdir(repo_path, KEYSTORE_DIR)
    # This is where the repository gets written to by default.
    metadata_staged_dir = create_subdir(repo_path, METADATA_STAGED_DIR)
    metadata_dir = create_subdir(repo_path, METADATA_DIR)

    repo_obj = create_new_repository(str(repo_path))
    create_and_set_keys(keystore_dir, repo_obj)
    
    write_repo(repo_obj, metadata_staged_dir, metadata_dir)