# Review previews

Test branch only: `main` and `oom-render.jar` are untouched.

Every push here renders short 1800 clips at the review moments in `moments.json`, once with each jar listed in
`run.json`. `before.jar` is the current live-device render and `after.jar` is the version under review.
An empty `moments` list means all of them.

To see results, open the repo's **Actions** tab and click the newest **Review previews (1800)** run.
Then download **previews_all**, a zip with every clip (.mp4) and a still (.png) of each.
