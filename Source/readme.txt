Find enclosed a new version of Syringe modified to work specifically with
Command & Conquer Red Alert 2: Yuri's Revenge v1.001.

This version is required for Ares versions less than or equal to 3.0p1 to accept
the March 2024 releases on EA app and Steam, if supported.

# For Players

This version of Syringe might make a mod run that currently uses an Ares version
that does not support the newly released editions on EA app and Steam.

But be aware that the mod might not be intended to run with these editions
(yet). Before you apply this version of Syringe as a fix yourself, please check
the respective mod's support websites and channels on whether there is an
official solution.

# For Modders

## Changes in this version

### Ares related
This version will inject Ares if a supported version of an edition from EA app
or Steam is detected. If an edition is detected that is impossible to inject
into, a new error will be shown, directing users to check for updates of the
game or to visit the usual support channels.

This feature applies only to the library file called Ares.dll when being
injected into Yuri's Revenge.

### CnCNet related
Furthermore, the widely used cncnet5.dll is handled specifically to not inject
into Syringe itself while trying to figure out whether the library should be
injected into the game.

This feature applies to all files called cncnet5.dll, no matter which executable
is the injection target.

## Compatibility
This version of Syringe can replace all previously released official versions of
Syringe. It will be identifed as "0.7.3.0 yr" in the log file.

## Stay tuned
Since the releases are relatively new, and in merely a week the backwards
compatibiliy has been torn down and also partially rebuilt, expect more updates
once it is clear in what direction the releases are moving.

More data will needed to create a future proof solution.

AlexB, Pi day of 2024
