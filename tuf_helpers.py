
import os
import pathlib
import shutil
from typing import Dict

import securesystemslib as sslib
import tuf.scripts.repo as tuf_repo
import tuf.repository_tool as repo_tool


default_trust_dir = pathlib.Path.joinpath(pathlib.Path.home(), '.pysigny')
keystore_dir = 'private'
root_key_name = 'root_key'
targets_key_name = 'targets_key'
snapshot_key_name = 'snapshot_key'
timestamp_key_name = 'timestamp_key'
metadata_staged_dir = 'metadata.staged'
metadata_dir = 'metadata'


class TUFKey:
    private: None
    public: None
    passphrase: None


keys: Dict[str, TUFKey] = {
    root_key_name: TUFKey,
    targets_key_name: TUFKey,
    snapshot_key_name: TUFKey,
    timestamp_key_name: TUFKey
}


def init_repo(target, name, trustdir):
    repo_path = pathlib.Path.joinpath(trustdir, name)
    repository = repo_tool.create_new_repository(str(repo_path))
    create_and_set_keys(repository, name, trustdir)
    write_repo(name, trustdir)


def create_and_set_keys(repository, name, trustdir):
    for k in keys:
        p = os.environ.get(k.upper() + '_PASSPHRASE')
        if p == None:
            keys[k].passphrase = sslib.interface.get_password(
                prompt='Enter password for {0}: '.format(k), confirm=True)
        else:
            keys[k].passphrase = p

        repo_tool.generate_and_write_ecdsa_keypair(os.path.join(
            trustdir, name, keystore_dir, k), password=keys[k].passphrase)

        keys[k].private = tuf_repo.import_privatekey_from_file(
            os.path.join(trustdir, name, keystore_dir, k), keys[k].passphrase)

        print('trying to load public key from {0}'.format(
            os.path.join(trustdir, name, keystore_dir, k) + '.pub'))
        keys[k].public = tuf_repo.import_publickey_from_file(
            os.path.join(trustdir, name, keystore_dir, k) + '.pub')

    repository.root.add_verification_key(keys[root_key_name].public)
    repository.targets.add_verification_key(keys[targets_key_name].public)
    repository.snapshot.add_verification_key(keys[snapshot_key_name].public)
    repository.timestamp.add_verification_key(keys[timestamp_key_name].public)

    repository.root.load_signing_key(keys[root_key_name].private)
    repository.targets.load_signing_key(keys[targets_key_name].private)
    repository.snapshot.load_signing_key(keys[snapshot_key_name].private)
    repository.timestamp.load_signing_key(keys[timestamp_key_name].private)


def write_repo(name, trustdir):
    staged_meta = os.path.join(trustdir, name, metadata_staged_dir)
    meta = os.path.join(trustdir, name, metadata_dir)
    shutil.rmtree(meta, ignore_errors=True)
    shutil.copytree(staged_meta, meta)
