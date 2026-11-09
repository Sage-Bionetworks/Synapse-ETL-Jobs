import json
import unittest
import sys
from pathlib import Path
p = Path(__file__).parents[1]
sys.path.append(str(p) + "/src/scripts/glue_jobs")

from async_job_records import AsyncJobRecords


class TestAsyncJobRecords(unittest.TestCase):

    def test_transform(self):
        record = {
            "record_date": 1730851200000,
            "entity_id": "syn123",
            "query": {"sql": "select * from syn123", "limit": 10}
        }
        real_output = AsyncJobRecords.transform(record)
        self.assertEqual("2024-11-06", real_output["record_date"])
        self.assertEqual(123, real_output["entity_id"])
        self.assertEqual({"limit": 10, "sql": "select * from syn123"}, json.loads(real_output["query"]))

    def test_transform_without_entity_or_query(self):
        record = {"record_date": 1730851200000}
        real_output = AsyncJobRecords.transform(record)
        self.assertEqual({"record_date": "2024-11-06"}, real_output)

    def test_query_to_json_for_none(self):
        self.assertIsNone(AsyncJobRecords.query_to_json(None))

    def test_query_to_json_with_filters(self):
        query = {
            "sql": "select * from syn123",
            "additionalFilters": [{
                "concreteType": "org.sagebionetworks.repo.model.table.ColumnSingleValueQueryFilter",
                "columnName": "a",
                "operator": "EQUAL",
                "values": ["x"]
            }]
        }
        real_output = AsyncJobRecords.query_to_json(query)
        self.assertEqual(query, json.loads(real_output))
        # The keys are sorted so the same query always produces the same JSON
        self.assertEqual(real_output, AsyncJobRecords.query_to_json(dict(reversed(list(query.items())))))


if __name__ == '__main__':
    unittest.main()
