import datetime, pprint

import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient()
    collection = client["fishtest_new"]["runs_new"]
    #    pprint.pprint(list(collection.list_indexes()))
    runs = collection.find({}, {"start_time": 1}).sort("start_time", 1)
    count = 0
    t0 = datetime.datetime.utcnow()
    for run in runs:
        #        pprint.pprint(run)
        r_id = run["_id"]
        collection.update_one({"_id": r_id}, {"$set": {"count": count}})
        count += 1
    t1 = datetime.datetime.utcnow()
    total = (t1 - t0).total_seconds()
    per_run = total / count
    print(
        "{} runs updated. Total time {:.2f}s. Time per run {:.2f}ms.".format(
            count, total, 1000 * per_run
        )
    )
    runs.close()
    client.close()
