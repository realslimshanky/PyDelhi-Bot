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


### Version 1.2 : deployed on Febriuary 4th 2017

* Following [commands](https://core.telegram.org/bots#commands) were added
  * `/nextmeetupschedule` - to get the complete schedule of next meetup
* [Enhancement]
  * Mapped location of the venue of next meetup is now send with the `/nextmeetup` command
* [BugFix]
  * Location was map is now accurate which was previously showing "Egypt" instead "JNU Delhi" for [5th February meetup](https://www.meetup.com/pydelhi/events/234562550/)


### Version 2.0 : deployed on Febriuary 13th 2017

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