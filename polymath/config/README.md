# settings.toml documentation.
__ __
#### [server]
`port = "8080"`
> Sets the port this Applications is listening on, it's adviced, to use a Reverse Proxy in front of it, to gain a bit more Security depending on your Settings in the Proxy.

`url = "http://atlas.oraxen.com:8080"`
> The whole URL of your application, used so Oraxen Plugin know where to Download the Resourcepack.
__ __
#### [request]
`max_size = 100000000`
> Sets the maximum Size of Resourcepacks, you should adjust your Proxy Settings if one is used. 
__ __
#### [cleaner]
`delay = 21600`
> the delay at which the cleaner runs and trys to cleanup not used Resourcepacks, to save some space.

`pack_lifespan = 604800`
> sets how long a resourpack persists until it's going to be deleted (in sec.), the default ist 7 days.
> A Resourcepack is marked as unused when no client requests a Download of it.
__ __
#### [nginx]
`enabled = false`
> Enables the support for a reverse proxy, a bit misleading, that i named it "nginx", it can be used on other proxys as well tho.

`ip_header = "X-Real-IP"`
> which header to read the IP adress from,only needed if using a reverse Proxy, used to log some security related events.

`only_listen_nginx = true`
> Activates the Following Option below:

`nginx_location = "127.0.0.1"`
> The IP Address to listen on for request, if using reverse proxy it normally just is 127.0.0.1
__ __
#### [extra]
`debug_level = 20`
> used to set the amount of messages you want to see in the console (Same level and higher for example 10 includes all levels listed):
> 10 : Debug, See everything that's going on
> 20 : Info, Print information that could be interesting, but not everything
> 30 : Only warnings, just tell if something goes wrong

`log2file = -1`
> Set a File where to write the log into, can be set to -1 to disable saving logs to File.

`print_startup = "hello pterodactyl"`
> A little help for the Pterodactyl users out there, to let the interface know it's online, you can change this to whatever you like.

__ __
#### [security]
`block_unknown_agents = false`
> Disables / Enables User-Agent filtering at all, if this is false, the options below won't take any effect.

`reject_upload = true`
> Should uploads be rejected if the application is not known for uploads?

`reject_download = false`
> Should Downloads be rejected?

`known_agents = { upload = ["Apache-HttpClient.*"], download = ["Minecraft Java.*"] }`
> a Json that defined what Agents are known to be legid, strings in here are gonna be used as REGEX so make sure it matches the right user agent.
> Regex is used here to prevent rejection just because of a version change.
