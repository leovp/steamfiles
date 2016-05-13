File name is typically `appmanifest_<app_id>.acf`, e.g. `appmanifest_202970.acf`

The content is in plain text form. The file consists of multiple key-value pairs; the value can be a section or a string. The first key-value pair of an ACF file is "AppState", which has the root section as a value.

Let's have a look at the example:
::

    "AppState"
    {
        "appid"		"730"
        "Universe"		"1"
        "name"		"Counter-Strike: Global Offensive"
        "StateFlags"		"4"
        "installdir"		"Counter-Strike Global Offensive"
        "LastUpdated"		"1462547468"
        "UpdateResult"		"0"
        "SizeOnDisk"		"14990577143"
        "buildid"		"1110931"
        "LastOwner"		"76561198013962068"
        "BytesToDownload"		"8768"
        "BytesDownloaded"		"8768"
        "AutoUpdateBehavior"		"1"
        "AllowOtherDownloadsWhileRunning"		"0"
        "UserConfig"
        {
                "Language"		"english"
        }
        "MountedDepots"
        {
                "731"		"205709710082221598"
                "734"		"5169984513691014102"
        }
    }

As you can see, sections are inside the curly brackets and are separated by a new-line character, whereas string values are separated by two TAB characters.

After you ``load()`` the ACF data, the resulting multi-level dictionary (actually an Ordered Dictionary) will look like this:
::

    OrderedDict([
        ('AppState', OrderedDict([
            ('appid', '730'),
            ('Universe', '1'),
            ('name', 'Counter-Strike: Global Offensive'),
            ('StateFlags', '4'),
            ('installdir', 'Counter-Strike Global Offensive'),
            ('LastUpdated', '1463143781'),
            ('UpdateResult', '0'),
            ('SizeOnDisk', '14990577143'),
            ('buildid', '1110931'),
            ('LastOwner', '76561198013962068'),
            ('BytesToDownload', '7214047920'),
            ('BytesDownloaded', '7214047920'),
            ('AutoUpdateBehavior', '0'),
            ('AllowOtherDownloadsWhileRunning', '0'),
            ('UserConfig', OrderedDict([
                ('Language', 'english')
            ])),
            ('MountedDepots', OrderedDict([
                ('731', '205709710082221598'),
                ('734', '5169984513691014102')
            ]))
        ]))
    ])

