import datetime, pprint

import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient()
    collection = client["fishtest_new"]["runs"]
    try:
        collection.drop_index([("count", 1)])
    except:
        pass
    runs=collection.find({}, {"start_time":True}).sort("start_time", 1)
    count = 0
    t0 = datetime.datetime.utcnow()
    for run in runs:
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
    collection.create_index([("count",1)], unique=True)
    counters=client["fishtest_new"]["counters"]
    counters.drop()
    counters=client["fishtest_new"]["counters"]
    counters.insert_one({'runs': count})
    client.close()
