"""
The job processes the asynchronous job records.
"""

from awsglue.transforms import *
from utils import Utils
from glue_job import GlueJob

PARTITION_KEY = "record_date"


class AsyncJobRecords(GlueJob):

    def __init__(self, mapping_list, partition_key):
        super().__init__(mapping_list, partition_key)

    def execute(self, dynamic_frame):
        return dynamic_frame.map(f=AsyncJobRecords.transform)

    # Process the asynchronous job record
    @staticmethod
    def transform(dynamic_record):
        # This is the partition date
        dynamic_record[PARTITION_KEY] = Utils.ms_to_partition_date(dynamic_record[PARTITION_KEY])
        return dynamic_record


if __name__ == "__main__":
    mapping_list = [
        # The record is dated by when the job ended, so we map that timestamp into a bigint to extract the partition date
        ("timestamp", "bigint", "record_date", "bigint"),
        ("payload.jobId", "string", "job_id", "bigint"),
        ("payload.jobType", "string", "job_type", "string"),
        ("payload.jobState", "string", "job_state", "string"),
        ("payload.startedBy", "bigint", "started_by", "bigint"),
        ("payload.startedOn", "bigint", "started_on", "timestamp"),
        ("payload.changedOn", "bigint", "changed_on", "timestamp"),
        ("payload.runtimeMs", "bigint", "runtime_ms", "bigint"),
        ("payload.exception", "string", "exception", "string"),
        ("payload.errorMessage", "string", "error_message", "string"),
        ("payload.sessionId", "string", "session_id", "string"),
        # The bodies arrive as JSON strings, because their shape differs for every job type, and are read with json_extract
        ("payload.requestBody", "string", "request_body", "string"),
        ("payload.responseBody", "string", "response_body", "string"),
        ("stack", "string", "stack", "string"),
        ("instance", "string", "instance", "string")
    ]
    async_job_records = AsyncJobRecords(mapping_list, PARTITION_KEY)
