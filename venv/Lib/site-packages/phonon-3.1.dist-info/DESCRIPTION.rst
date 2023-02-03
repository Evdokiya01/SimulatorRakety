
When your users are sending 1000s, or even 10s of 1000s of events per second, it becomes hard to keep up with realtime user behavior.

Aggregating writes, and writing them out in a smart way allows the most efficient batching possible. 

With phonon, you can join events across a cluster of worker/consumer nodes by totally abstracting away reference counting.

You can decide to collect events and aggregate across your cluster, and then write to a data backend at the time the user's session ends. You can also decide to write out based on how many events have been aggregated up to that point, for the user.

This allows your ingestion pipeline to scale to 10s of 1000s of client-facing events per second with a single redis backend. Oh, and phonon provides sharding with linear scaling.



