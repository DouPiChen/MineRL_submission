"""Logging Helper"""

from contextlib import contextmanager
import os.path as osp
import json

from rlpyt.utils.logging import logger


@contextmanager
def logger_context(log_dir, run_ID, name, log_params=None, snapshot_mode="none", snapshot_gap=50):
    logger.set_snapshot_mode(snapshot_mode)
    logger.set_snapshot_gap(snapshot_gap)
    logger.set_log_tabular_only(False)
    log_dir = osp.join(log_dir, f"run_{run_ID}")
    exp_dir = osp.abspath(log_dir)
    tabular_log_file = osp.join(exp_dir, "progress.csv")
    text_log_file = osp.join(exp_dir, "debug.log")
    params_log_file = osp.join(exp_dir, "params.json")

    logger.set_snapshot_dir(exp_dir)
    logger.add_text_output(text_log_file)
    logger.add_tabular_output(tabular_log_file)
    logger.push_prefix(f"{name}_{run_ID} ")

    if log_params is None:
        log_params = dict()
    log_params["name"] = name
    log_params["run_ID"] = run_ID
    with open(params_log_file, "w") as f:
        json.dump(log_params, f)

    yield

    logger.remove_tabular_output(tabular_log_file)
    logger.remove_text_output(text_log_file)
    logger.pop_prefix()
