import unittest
import sys
from pathlib import Path
p = Path(__file__).parents[1]
sys.path.append(str(p) + "/src/scripts/glue_jobs")

from async_job_records import AsyncJobRecords

REQUEST_BODY = ('{"concreteType":"org.sagebionetworks.repo.model.table.QueryBundleRequest",'
                '"entityId":"syn123","query":{"sql":"select * from syn123"}}')
RESPONSE_BODY = '{"concreteType":"org.sagebionetworks.repo.model.table.QueryResultBundle","queryCount":25}'


class TestAsyncJobRecords(unittest.TestCase):

    def test_transform(self):
        record = {
            "record_date": 1730851200000,
            "job_id": 8888,
            "job_state": "COMPLETE",
            "request_body": REQUEST_BODY,
            "response_body": RESPONSE_BODY
        }
        real_output = AsyncJobRecords.transform(record)
        # Only the partition date is derived; the bodies are kept as the JSON strings they arrive as.
        self.assertEqual({
            "record_date": "2024-11-06",
            "job_id": 8888,
            "job_state": "COMPLETE",
            "request_body": REQUEST_BODY,
            "response_body": RESPONSE_BODY
        }, real_output)

    def test_transform_with_failed_job(self):
        # A failed job has no response body, so the field is absent
        record = {"record_date": 1730851200000, "job_state": "FAILED", "error_message": "The query matched too few rows"}
        real_output = AsyncJobRecords.transform(record)
        self.assertEqual({
            "record_date": "2024-11-06",
            "job_state": "FAILED",
            "error_message": "The query matched too few rows"
        }, real_output)


if __name__ == '__main__':
    unittest.main()
