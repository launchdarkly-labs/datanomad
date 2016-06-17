# Datanomad
### An example app demonstrating migrating databases using feature flags

This will simulate a live, rolling migration from MongoDB to DynamoDB.  Using feature flags, you can
monitor the migration, check the data for errors, and monitor the performance as you transition more
users onto the new system.

For more information:

* [Feature flagging to mitigate risk in database migration](http://blog.launchdarkly.com/feature-flagging-to-mitigate-risk-in-database-migration/)
* [LaunchDarkly](https://launchdarkly.com)

## To run

Ensure that you have AWS credentials with dynamo access in the 
[usual places](http://boto3.readthedocs.io/en/latest/guide/configuration.html#guide-configuration) 
for boto to pick them up.

    LD_SDK_KEY=... python app.py

Send events to the app using the [jmeter](http://jmeter.apache.org/) script [events_load.jmx](events_load.jmx).

You can view the dashboard at [http://localhost:5000/](http://localhost:5000/).

## To control the migration

You will need a LaunchDarkly account. You can get a free trial at https://launchdarkly.com/#signup.

Create flags with the following keys:

- read-events-dynamo
- read-events-mongo
- write-events-dynamo
- write-events-mongo

## Simulating a migration

There are a few tags in this repo that represent the different stages of the migration:

| tag | description |
|-----|-------------|
| mongo-only | The initial state, MongoDB is the only database |
| add-dynamodb | Code to talk to DynamoDB was added, and feature flags were added to control which database is used |
| dynamo-fix-bug | A bug was fixed, which was illustrated by the integrity checking used by the approach outlined in the blog & talk |
| dynamo-only | The migration is complete, and the mongo and feature flag code is removed |

Before 'deploying' the `add-dynamodb` tag, you should set the feature flag rollout to:

| flag key | rollout % |
|----------|-----------|
| read-events-dynamo | 0% |
| read-events-mongo | 100% |
| write-events-dynamo | 0% |
| write-events-mongo | 100% |

This means that all reads and writes will continue to go to Mongo, and nothing will touch Dynamo (until you decide to start rolling it out).

Then, play with the rollouts to watch the traffic migrate.