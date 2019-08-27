## PyDelhi Bot - Change Logs
Simple Python based bot for telegram to fetch links.

### Version 1.0 : deployed on January 21th 2017

* Following [commands](https://core.telegram.org/bots#commands) were added
  * `/mailinglist` - to get PyDelhi Mailing List link
  * `/irc` - to get a link to Pydelhi IRC channel
  * `/twitter` - to get Pydelhi Twitter link
  * `/meetuppage` - to get a link to PyDelhi Meetup page
  * `/nextmeetup` - to get info about next Meetup
  * `/facebook` - to get a link to PyDelhi Facebook page
  * `/help` - to get help
* Works with [inline-queries](https://core.telegram.org/bots/inline)
* deployed on [AWS EC2 instance of Ubuntu](https://help.ubuntu.com/community/EC2StartersGuide)


### Version 1.1 : deployed on January 22nd 2017

* Following [commands](https://core.telegram.org/bots#commands) were added
  * `/invitelink` - to get an invite link for PyDelhi Telegram Group of Volunteers
* [BugFix]
  * Timezone changed from UTC to IST


### Version 1.2 : deployed on February 4th 2017

* Following [commands](https://core.telegram.org/bots#commands) were added
  * `/nextmeetupschedule` - to get the complete schedule of next meetup
* [Enhancement]
  * Mapped location of the venue of next meetup is now send with the `/nextmeetup` command
* [BugFix]
  * Location was map is now accurate which was previously showing "Egypt" instead "JNU Delhi" for [5th February meetup](https://www.meetup.com/pydelhi/events/234562550/)


### Version 2.0 : deployed on February 12th 2017

* New Feature added to handle different teams for events like PyDelhi Conference.
* Supported teams are 
  * Sponsorship - `/sponsorshipteam`
  * Design - `/designteam`
  * Website - `/websiteteam`
  * Vendor - `/vendorteam`
  * Logistics - `/logisticsteam`
  * Social Media - `/socialmediateam`
* Teams can modified by using `/modifyteam` with a operation (add or remove), a team name (one from the above) and a set of usernames. For example, `/modifyteam add website @realslimshanky`
* Only specific people(admins) can make above commands.


### Version 2.1 : deployed on February 13th 2017

* Visibility of team members is made accessible to public now.
* '@' is removed from team member's name to manually ping them when needed.


### Version 2.2 : deployed on February 14th 2017

* Support for descriptions containing `<a>` tag. In the /nextmeetupschedule use of `<a>` tag was prohibitted since Telegram HTML parser does not support that. So, I analysed the input json from meetup.com and substituted `<a>` tag out of it.

### Version 3 : deployed on November 26th 2017

* Telegram and Meetup token/key has now been segregated from the main script i.e. `pydelhi.py` inside `config.txt`.
* `config.txt` is checked for existance and token/key validation everytime the `pydelhi.py` runs.
* `virtualenv` has been replaced with `pipenv` which is easy to use and leaves lesser footprint on the project repository.
* `pid` has been added to store the process id of the running python instance for `pydelhi.py` in order to easily terminate the process before running a new instance.
* `pydelhi.py` now has inline documentation explaining how Process ID and Token/Key Management code works.
