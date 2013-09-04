Command line tools for generating Dependency Graphs in Gus.

There are two command lines:
 - team_dependencies.py: Graph dependencies for a team
 - release_dependencies.py: Graph dependencies for a team within a release
 
Installing this package with pip or easy_install will put both commands in your path.
If you execute the scripts, you will be prompted to login to GUS and then it will
graph dependencies for all teams in which you are a member with an allocation > 0%.

Optionally, you can specify a Team object id to graph dependencies for a specific team
even if you are not a member.  The Team Id is the id in the URL on the team page in Gus.

The release_dependencies.py script requires a Build Name and requires that all dependencies
are in gus and have a target release specified with the Build name you specify.  The tool
will help you identify dependencies that aren't completed properly and help you track
progress and dependency chains.

Graphs are color coded by status:

Red: Item is not being looked at (ie New, Deferred)
Green: Item is completed or closed
Yellow: Item is code complete or committed but not verified yet
Orange: All other statuses (ie In progress, Prioritized)