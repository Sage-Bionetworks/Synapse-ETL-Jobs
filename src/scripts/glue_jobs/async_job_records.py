"""
The job processes the asynchronous job records.
"""

import json

from awsglue.transforms import *
from utils import Utils
from glue_job import GlueJob

PARTITION_KEY = "record_date"
ENTITY_ID = "entity_id"
QUERY = "query"


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
        # Only some request types name an entity, so the field can be absent
        if ENTITY_ID in dynamic_record.keys():
            # The records come in with the syn prefix, we need to remove that
            dynamic_record[ENTITY_ID] = Utils.syn_id_string_to_int(dynamic_record[ENTITY_ID])
        # Only requests that carry a table query have one, so the field can be absent
        if QUERY in dynamic_record.keys():
            dynamic_record[QUERY] = AsyncJobRecords.query_to_json(dynamic_record[QUERY])
        return dynamic_record

    # The filters and cohorts of a query take many shapes, so the query is stored as its JSON, which
    # Athena reads with json_extract.
    @staticmethod
    def query_to_json(query):
        if query is None:
            return None
        return json.dumps(query, sort_keys=True)


if __name__ == "__main__":
    mapping_list = [
        ("timestamp", "bigint", "timestamp", "timestamp"),
        # we need to map the same timestamp into a bigint so that we can extract the partition date
        ("timestamp", "bigint", "record_date", "bigint"),
        ("payload.jobId", "string", "job_id", "bigint"),
        ("payload.jobType", "string", "job_type", "string"),
        ("payload.requestConcreteType", "string", "request_concrete_type", "string"),
        ("payload.userId", "bigint", "user_id", "bigint"),
        ("payload.sessionId", "string", "session_id", "string"),
        ("payload.entityId", "string", "entity_id", "string"),
        ("payload.startedOn", "bigint", "started_on", "timestamp"),
        ("payload.runtimeMs", "bigint", "runtime_ms", "bigint"),
        ("payload.outcome", "string", "outcome", "string"),
        ("payload.exceptionClass", "string", "exception_class", "string"),
        ("payload.query", "struct", "query", "struct"),
        ("payload.resultCount", "bigint", "result_count", "bigint"),
        ("payload.facetPostProcessingApplied", "boolean", "facet_post_processing_applied", "boolean"),
        ("payload.truncated", "boolean", "truncated", "boolean"),
        ("stack", "string", "stack", "string"),
        ("instance", "string", "instance", "string")
    ]
    async_job_records = AsyncJobRecords(mapping_list, PARTITION_KEY)
